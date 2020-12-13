# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Data Fields
=================

We extends the field classes from :mod:`peewee` with two properties
(:attr:`~flask_datatables.fields.Field.dt_orderable` and
:attr:`~flask_datatables.fields.Field.dt_searchable`) and two
conversion methods (:meth:`~flask_datatables.fields.Field.dt_order`
and :meth:`~flask_datatables.fields.Field.dt_search`) for the integration
with `DataTables`_ server-side processing.

.. _DataTables: https://datatables.net/

"""

import datetime
import decimal
import uuid
from typing import Any, Optional, Union

import peewee

__all__ = [
    'Field',

    'AutoField',
    'BareField',
    'BigAutoField',
    'BigBitField',
    'BigIntegerField',
    'BinaryUUIDField',
    'BitField',
    'BlobField',
    'BooleanField',
    'CharField',
    'DateField',
    'DateTimeField',
    'DecimalField',
    'DoubleField',
    'FixedCharField',
    'FloatField',
    'ForeignKeyField',
    'IdentityField',
    'IntegerField',
    'IPField',
    'ManyToManyField',
    'PrimaryKeyField',
    'SmallIntegerField',
    'TextField',
    'TimeField',
    'TimestampField',
    'UUIDField',
]


class Field(peewee.Field):
    """Extending :class:`peewee.Field`.

    Args:
        orderable: Optional[Union[bool, peewee.Field]]: `DataTables`_ orderable field.
        searchable: Optional[Union[bool, peewee.Field]]: `DataTables`_ searchable field.
        **kwargs: Arbitrary arguments accepted by :class:`peewee.Field`.

    If ``orderable`` and/or ``searchable`` is a :obj:`bool` value, it indicates if the
    field supports `DataTables`_ ordering and/or searching:

    * :data:`True` means the field is orderable and/or searchable, and it will refer to
      its properties :attr:`~flask_datatables.fields.Field.dt_orderable` and/or
      :attr:`~flask_datatables.fields.Field.dt_searchable` as its default field instance;

      .. note::

         If the property returns :data:`None`, then the field is orderable and/or searchable
         by itself with its own values.

    * :data:`False` disables ordering and searching on the field;
    * an instance of :class:`peewee.Field` indicates that the current field is orderable
      and/or searchable through the given field instance.

    Important:
        If ``orderable`` and/or ``searchable`` is an instance of :class:`peewee.Field`, then
        its attributes :attr:`~flask_datatables.fields.Field.orderable` and/or
        :attr:`~flask_datatables.fields.Field.searchable` will be the corresponding instance.

        If ``orderable`` and/or ``searchable`` is :data:`True`, then it refers to its properties
        :attr:`~flask_datatables.fields.Field.dt_orderable` and/or
        :attr:`~flask_datatables.fields.Field.dt_searchable` as the actual value:

        * if the properties return an instance of :class:`peewee.Field`, then the attributes will
          be the returned instance; i.e. the field is orderable and/or searchable by converting to
          the target field instead of itself;
        * if the properties return :data:`None`, then the attributes will be :data:`True`; i.e.
          the field is orderable and/or searchable by itself with its value.

        If ``orderable`` and/or ``searchable`` is :data:`False`, then the attributes will be
        :data:`False` as well.

    """

    @property
    def dt_orderable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default orderable field."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""

    def __init__(self, orderable=None, searchable=None,  # type: ignore
                 null=False, index=False, unique=False, column_name=None,
                 default=None, primary_key=False, constraints=None,
                 sequence=None, collation=None, unindexed=False, choices=None,
                 help_text=None, verbose_name=None, index_type=None,
                 db_column=None, _hidden=False):
        super().__init__(null=null, index=index, unique=unique, column_name=column_name,
                         default=default, primary_key=primary_key, constraints=constraints,
                         sequence=sequence, collation=collation, unindexed=unindexed, choices=choices,
                         help_text=help_text, verbose_name=verbose_name, index_type=index_type,
                         db_column=db_column, _hidden=_hidden)

        if orderable is None:
            orderable = self.dt_orderable or True
        if searchable is None:
            searchable = self.dt_searchable or True

        #: `DataTables`_ integration orderable flag.
        self.orderable: Union[bool, peewee.Field] = orderable
        #: `DataTables`_ integration searchable flag.
        self.searchable: Union[bool, peewee.Field] = searchable

    @staticmethod
    def dt_order(value: Any) -> Any:
        """Convert value for `DataTables`_ ordering operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return value

    @staticmethod
    def dt_search(value: Any) -> Any:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return value


class IntegerField(peewee.IntegerField, Field):
    """Extending :class:`peewee.IntegerField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.TextField(null=True)

    @staticmethod
    def dt_search(value: int) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return str(value)


class BigIntegerField(peewee.BigIntegerField, IntegerField):
    """Extending :class:`peewee.BigIntegerField`."""


class SmallIntegerField(peewee.SmallIntegerField, IntegerField):
    """Extending :class:`peewee.SmallIntegerField`."""


class AutoField(peewee.AutoField, IntegerField):
    """Extending :class:`peewee.AutoField`."""


class BigAutoField(peewee.BigAutoField, AutoField):
    """Extending :class:`peewee.BigAutoField`."""


class IdentityField(peewee.IdentityField, AutoField):
    """Extending :class:`peewee.IdentityField`."""


class PrimaryKeyField(peewee.PrimaryKeyField, AutoField):
    """Extending :class:`peewee.PrimaryKeyField`."""


class FloatField(peewee.FloatField, Field):
    """Extending :class:`peewee.FloatField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.TextField(null=True)

    @staticmethod
    def dt_search(value: float) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return str(value)


class DoubleField(peewee.DoubleField, FloatField):
    """Extending :class:`peewee.DoubleField`."""


class DecimalField(peewee.DecimalField, Field):
    """Extending :class:`peewee.DecimalField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.TextField(null=True)

    @staticmethod
    def dt_search(value: decimal.Decimal) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return str(value)


class _StringField(peewee._StringField, Field):  # pylint: disable=protected-access
    """Extending :class:`peewee._StringField`."""


class CharField(peewee.CharField, _StringField):
    """Extending :class:`peewee.CharField`."""


class FixedCharField(peewee.FixedCharField, CharField):
    """Extending :class:`peewee.FixedCharField`."""


class TextField(peewee.TextField, _StringField):
    """Extending :class:`peewee.TextField`."""


class BlobField(peewee.BlobField, Field):
    """Extending :class:`peewee.BlobField`."""


class BitField(peewee.BitField, BigIntegerField):
    """Extending :class:`peewee.BitField`."""


class BigBitField(peewee.BigBitField, BlobField):
    """Extending :class:`peewee.BigBitField`."""


class UUIDField(peewee.UUIDField, Field):
    """Extending :class:`peewee.UUIDField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.CharField(max_length=40, null=True)

    @staticmethod
    def dt_search(value: uuid.UUID) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return str(value)


class BinaryUUIDField(peewee.BinaryUUIDField, Field):
    """Extending :class:`peewee.BinaryUUIDField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.CharField(max_length=16, null=True)

    @staticmethod
    def dt_search(value: uuid.UUID) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return str(value)


class _BaseFormattedField(peewee._BaseFormattedField, Field):  # pylint: disable=protected-access
    """Extending :class:`peewee._BaseFormattedField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.TextField(null=True)

    @staticmethod
    def dt_search(value: Union[datetime.datetime, datetime.date, datetime.time]) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return value.isoformat()


class DateTimeField(peewee.DateTimeField, _BaseFormattedField):
    """Extending :class:`peewee.DateTimeField`."""


class DateField(peewee.DateField, _BaseFormattedField):
    """Extending :class:`peewee.DateField`."""


class TimeField(peewee.TimeField, _BaseFormattedField):
    """Extending :class:`peewee.TimeField`."""


class TimestampField(peewee.TimestampField, BigIntegerField):
    """Extending :class:`peewee.TimestampField`."""

    @staticmethod
    def dt_search(value: datetime.datetime) -> str:  # type: ignore[override]
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return value.isoformat()


class IPField(peewee.IPField, BigIntegerField):
    """Extending :class:`peewee.IPField`."""

    @staticmethod
    def dt_search(value: str) -> str:  # type: ignore[override]
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return value


class BooleanField(peewee.BooleanField, Field):
    """Extending :class:`peewee.BooleanField`."""

    @property
    def dt_searchable(self) -> Optional[peewee.Field]:
        """`DataTables`_ default searchable field."""
        return peewee.CharField(max_length=5, null=True)

    @staticmethod
    def dt_search(value: bool) -> str:
        """Convert value for `DataTables`_ searching operation.

        Args:
            value: Source value.

        Returns:
            Converted value.

        """
        return 'true' if value else 'false'


class BareField(peewee.BareField, Field):
    """Extending :class:`peewee.BareField`."""


class ForeignKeyField(peewee.ForeignKeyField, Field):
    """Extending :class:`peewee.ForeignKeyField`."""


class DeferredForeignKey(peewee.DeferredForeignKey, Field):
    """Extending :class:`peewee.DeferredForeignKey`."""


class ManyToManyField(peewee.ManyToManyField, Field):
    """Extending :class:`peewee.ManyToManyField`."""


class VirtualField(peewee.VirtualField, Field):
    """Extending :class:`peewee.VirtualField`."""
