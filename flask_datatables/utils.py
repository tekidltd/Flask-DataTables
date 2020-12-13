# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Utilities & Auxiliaries
=============================

We provided some auxiliary functions for ``Flask-DataTables``.

* :func:`~flask_datatables.utils.render_macro` renders a given
  ``macro`` from the Jinja templates
* :func:`~flask_datatables.utils.prepare_response` is the default
  built-in method for ``factory`` parameter of
  :meth:`Model.search <flask_datatables.model.Model.search>`
* :func:`~flask_datatables.utils.parse_request` is the utility
  function to parse `DataTables`_ client-side query parameters
  from the URL

.. _DataTables: https://datatables.net/

"""

import contextlib
import urllib.parse
from typing import Callable, List, Optional, Union

import flask
import peewee
import werkzeug.datastructures
import werkzeug.exceptions

from .typing import ObjectData, Query

__all__ = [
    'render_macro',
    'prepare_response',
    'parse_request',
]


def render_macro(template_name_or_list: Union[str, List[str]], macro: str, **context) -> str:  # type: ignore[no-untyped-def]
    """Evaluates and renders a **macro** from the template.

    Args:
        template_name_or_list: The name of the template to be rendered, or an iterable with template names
            the first one existing will be rendered.
        macro: The name of macro to be called.

    Keyword Args:
        **context: The variables that should be available in the context of the template.

    Returns:
        The rendered macro.

    """
    template = flask.current_app.jinja_env.get_or_select_template(template_name_or_list)  # pylint: disable=no-member
    macro_func = getattr(template.module, macro)
    return macro_func(**context)


def prepare_response(template: Union[str, List[str]]) -> Callable[[peewee.Model], ObjectData]:
    """Prepare response object data.

    The function returns a wrapper function to use the ``template`` as a factory to
    render HTML response blocks. The Jinja templates should have **macro** blocks
    for each target field named after ``render_{field_name}`` and takes only one
    argument ``record`` as the selected data model record.

    Args:
        template: Path to the macro template.

    Returns:
        Prepared response object data.

    See Also:
        See :func:`flask_datatables.utils.render_macro` for more information.

    """
    def wrapper(record: peewee.Model) -> ObjectData:
        data = dict()
        for field in record.__data__.keys():
            try:
                data[field] = render_macro(template, f'render_{field}', record=record)
            except Exception:
                data[field] = getattr(record, field)
        return data  # type: ignore[return-value]
    return wrapper


def _parse_int(arg: Optional[str]) -> int:
    """Parse argument as :obj:`int`.

    Args:
        arg: Original request argument.

    Returns:
        Parsed query argument.

    """
    with contextlib.suppress(Exception):
        return int(arg)  # type: ignore[arg-type]
    return -1


def _parse_bool(arg: Optional[str]) -> bool:
    """Parse argument as :obj:`bool`.

    Args:
        arg: Original request argument.

    Returns:
        Parsed query argument.

    """
    if isinstance(arg, str):
        arg = arg.casefold()
        if arg == 'true':
            return True
        if arg == 'false':
            return False
    return False


def _parse_str(arg: Optional[str]) -> str:
    """Parse argument as :obj:`str`.

    Args:
        arg: Original request argument.

    Returns:
        Parsed query argument.

    """
    if arg is None:
        return ''
    return arg


def parse_request(args: Optional[werkzeug.datastructures.ImmutableMultiDict] = None) -> Query:
    """Parse :attr:`flask.request.args <flask.Request.args>` as :class:`~tekid.ext.datatables.Query`.

    Args:
        args: Original request arguments. The default value is inferred from
            :attr:`request.args <flask.Request.args>`.

    Returns:
        Parsed query dictionary.

    """
    if args is None:
        args = flask.request.args

    query: Query = {
        'draw': _parse_int(args.get('draw')),
        'columns': [],
        'order': [],
        'start': _parse_int(args.get('start')),
        'length': _parse_int(args.get('length')),
        'search': {
            'value': _parse_str(args.get('search[value]')),
            'regex': _parse_bool(args.get('search[regex]')),
        },
        '_': _parse_int(args.get('_')),
    }

    index = 0
    while True:
        try:
            data = args[f'columns[{index}][data]']
        except werkzeug.exceptions.BadRequestKeyError:
            break

        query['columns'].append({
            'data': _parse_str(data),
            'name': _parse_str(args.get(f'columns[{index}][data]')),
            'searchable': _parse_bool(args.get(f'columns[{index}][searchable]')),
            'orderable': _parse_bool(args.get(f'columns[{index}][orderable]')),
            'search': {
                'value': _parse_str(args.get(f'columns[{index}][search][value]')),
                'regex': _parse_bool(args.get(f'columns[{index}][search][regex]')),
            },
        })
        index += 1

    index = 0
    while True:
        try:
            column = args[f'order[{index}][column]']
        except werkzeug.exceptions.BadRequestKeyError:
            break

        query['order'].append({
            'column': _parse_int(column),
            'dir': _parse_str(args.get(f'order[{index}][dir]')),  # type: ignore[typeddict-item]
        })
        index += 1

    return query


def build_cache(query_string: Optional[str] = None) -> str:
    """Build a key to cache the query parameters.

    Args:
        query_string: Query parameters in string form. The default value is inferred
            from :attr:`request.query_string <flask.Request.query_string>`.

    Returns:
        A string literal representing the query parameters.

    """
    if query_string is None:
        query_string = flask.request.query_string.decode()

    query_parsed = urllib.parse.parse_qsl(query_string)
    query = werkzeug.datastructures.MultiDict(query_parsed).to_dict()

    if 'draw' in  query:
        del query['draw']

    query_sorted = sorted(query.items(), key=lambda kv: kv[0])
    return urllib.parse.urlencode(query_sorted)
