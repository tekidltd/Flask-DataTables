# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Base Model
================

We extends the :class:`peewee.Model` class to integrate with the
server-side processing logic of `DataTables`_. Some monkeypathes
were made as certain functionalities with :mod:`peewee` are not
correctly implemented.

.. _DataTables: https://datatables.net/

"""

import functools
import traceback
from typing import Callable, Dict, List, Optional, Union

import flask
import peewee

from .typing import ArrayData, ObjectData, Query, Response
from .utils import parse_request

__all__ = ['Model', 'Metadata']

# factory function to convert records
Factory = Callable[[peewee.Model], Union[ArrayData, ObjectData]]


class Metadata(peewee.Metadata):
    """Basic metadata for data models.

    ``Flask-DataTables`` extends the original metadata record from :mod:`peewee`
    with a :attr:`~flask_datatables.model.Metadata.datatables` switch to indicate
    if current data model supports and/or enables `DataTables`_ server-side
    processing integration.

    """

    #: `DataTables`_ integration indicator flag.
    datatables: bool = False


class Model(peewee.Model):
    """Extends :class:`peewee.Model` with `DataTables`_ support."""

    id: peewee.AutoField
    _meta: Metadata

    #: `DataTables`_ orderable fields.
    dt_orderable: Dict[str, peewee.Field]

    #: `DataTables`_ searchable fields.
    dt_searchable: Dict[str, peewee.Field]

    @classmethod
    def validate_model(cls) -> None:
        """Validates data model and dynamically insert fields.

        If `DataTables`_ integration is enabled for the data model, this method
        will insert fields (database columns) for both *order* and *search*
        operations respectively on each defined fields according to the original
        field type definition.

        By default, each field is *orderable* and/or *searchable* as long as the
        :attr:`~flask_datatables.model.Metadata.datatables` switch is enabled.
        When the :attr:`~flask_datatables.fields.Field.orderable` and/or
        :attr:`~flask_datatables.fields.Field.searchable` attributes are set to
        an instance of a :class:`~peewee.Field`, ``Flask-DataTables`` will insert
        additional fields of such type with ``_dt_order`` and/or ``_dt_search``
        suffix as the field names accordingly.

        """
        cls.dt_orderable = dict()
        cls.dt_searchable = dict()

        metaclass = cls._meta
        if getattr(metaclass, 'datatables', False):
            for key, value in metaclass.fields.copy().items():
                orderable = getattr(value, 'orderable', True)
                if orderable:
                    target = value
                    if isinstance(orderable, peewee.Field):
                        metaclass.add_field(f'{key}_dt_order', orderable)
                        target = metaclass.fields[f'{key}_dt_order']
                        setattr(cls, f'{key}_dt_order', target)
                    cls.dt_orderable[key] = target

                searchable = getattr(value, 'searchable', True)
                if searchable:
                    target = value
                    if isinstance(searchable, peewee.Field):
                        metaclass.add_field(f'{key}_dt_search', searchable)
                        target = metaclass.fields[f'{key}_dt_search']
                        setattr(cls, f'{key}_dt_order', target)
                    cls.dt_searchable[key] = target

        return super().validate_model()

    def save(self, force_insert: bool = False, only: Optional[List[peewee.Field]] = None) -> int:
        """Save the data in the model instance.

        The method extends the original :meth:`peewee.Model.save` method by automatically
        update the *searching* and *ordering* field data with the actual data.

        Args:
            force_insert: Force ``INSERT`` query.
            only: Only save the given :class:`~peewee.Field` instances.

        Returns:
            Number of rows modified.

        """
        metaclass = self._meta

        for key, target in self.dt_orderable.items():
            if key == target.name:
                continue
            value = getattr(self, key)
            source = metaclass.fields[key]
            if hasattr(source, 'dt_order'):
                value = source.dt_order(value)
            setattr(self, target.name, value)

        for key, target in self.dt_searchable.items():
            if key == target.name:
                continue
            value = getattr(self, key)
            source = metaclass.fields[key]
            if hasattr(source, 'dt_search'):
                value = source.dt_search(value)
            setattr(self, target.name, value)

        return super().save(force_insert, only)

    @classmethod
    def search(cls: peewee.Model, query: Optional[Query] = None,
               factory: Optional[Factory] = None) -> Response:
        """Server-side processing integration with `DataTables`_.

        Args:
            query: Query parameters sent from the client-side.
            factory: Factory function to prepare the server-side data.

        Returns:
            Selected information from the database in format to
            be sent to `DataTables`_.

        See Also:
            The ``factory`` function takes exactly one parameter, the data
            record returned from :mod:`peewee` selection, and returns
            the converted data of fields. See
            :func:`flask_datatables.utils.prepare_response` for an example.

        """
        if query is None:
            query = parse_request(flask.request.args)
        errors: List[BaseException] = list()

        try:
            draw = int(query['draw'])
        except ValueError as error:
            draw = query['draw']
            errors.append(error)

        global_search_info = query['search']
        global_search_value = global_search_info['value']
        global_search_regex = global_search_info['regex']

        field_list: List[peewee.Field] = []
        extra_field_list: List[peewee.Field] = [cls.id]
        where_query_list: List[peewee.Expression] = list()
        for column in query['columns']:
            field_name = column['data']
            try:
                source_field: peewee.Field = cls._meta.fields[field_name]
            except KeyError as error:
                errors.append(error)
                continue
            field_list.append(source_field)

            if not column['searchable']:
                continue

            try:
                field = cls._meta.fields[f'{source_field.name}_dt_search']
                extra_field_list.append(field)
            except KeyError:
                field = source_field

            search_info = column['search']
            search_value = search_info['value']
            if search_value:
                search_regex = search_info['regex']
            else:
                search_value = global_search_value
                search_regex = global_search_regex

            if not search_value:
                continue

            #field = field.collate('utf8mb4_unicode_ci')  # case-insensitive search
            if search_regex:
                where_query = field.iregexp(search_value)
            else:
                where_query = field.contains(search_value)
            where_query_list.append(where_query)

        order_by_list: List[peewee.Ordering] = list()
        for order_info in query['order']:
            try:
                column_index = int(order_info['column'])
                source_field = field_list[column_index]
            except IndexError as error:
                errors.append(error)
                continue

            try:
                field = cls._meta.fields[f'{source_field.name}_dt_order']
                extra_field_list.append(field)
            except KeyError:
                field = source_field

            order_dir = order_info['dir'].casefold()
            if order_dir == 'asc':
                order_by_list.append(field.asc())
            elif order_dir == 'desc':
                order_by_list.append(field.desc())
            else:
                errors.append(ValueError(f'unknown ordering direction: {order_dir}'))

        select_query: peewee.ModelSelect = cls.select(*field_list, *extra_field_list)
        if where_query_list:
            select_query = select_query.where(functools.reduce(
                lambda p0, p1: p0 | p1, where_query_list,
            ))
        select_query = select_query.order_by(*order_by_list)

        records_total = cls.select().count()
        records_filtered = select_query.count()

        start = query['start']
        length = query['length']

        data: List[Union[ArrayData, ObjectData]] = list()
        for record in select_query.offset(start).limit(length).objects():
            if factory is not None:
                row = factory(record)
            else:
                row = [record.__data__[field.name] for field in field_list]
            data.append(row)

        error_msg = None
        if flask.current_app.debug and errors:
            error_msg = 'Error processing query...\n'
            for exc in errors:
                error_msg += '-' * 80 + '\n'
                error_msg += ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))

        return dict(
            draw=draw,
            recordsTotal=records_total,
            recordsFiltered=records_filtered,
            data=data,
            error=error_msg,
        )
