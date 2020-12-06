# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Type Hints
================

As described in the `DataTables documentation`_, the client side sends
specific format of query parameters to the server side.

When making a request to the server using server-side processing, DataTables
will send data as described in :class:`~flask_datatables.typing.Query` in order
to let the server know what data is required.

Once DataTables has made a request for data, with the above parameters sent to
the server, it expects JSON data to be returned to it, with the parameters set
as described in :class:`~flask_datatables.typing.Response`.

.. _DataTables documentation: https://datatables.net/manual/server-side

"""

from typing import Any, Dict, List, Optional, Union

from typing_extensions import Literal, TypedDict

__all__ = ['Query', 'Response']


class Search(TypedDict):
    """Search information."""

    #: Global search value. To be applied to all columns
    #: which have ``searchable`` as :data:`True`.
    value: str

    #: :data:`True` if the global filter should be treated
    #: as a regular expression for advanced searching,
    #: :data:`False` otherwise. Note that normally server-side
    #: processing scripts will not perform regular expression
    #: searching for performance reasons on large data sets,
    #: but it is technically possible and at the discretion of
    #: your script.
    regex: bool


class Order(TypedDict):
    """Ordering information."""

    #: Column to which ordering should be applied. This is an
    #: index reference to the :attr:`~tekid.ext.datatables.Query.columns`
    #: array of information that is also submitted to the server.
    column: int

    #: Ordering direction for this column. It will be ``asc`` or
    #: ``desc`` to indicate ascending ordering or descending ordering,
    #: respectively.
    dir: Literal['asc', 'desc']


class Column(TypedDict):
    """Column data."""

    #: Column's data source, as defined by :js:attr:`columns.data`.
    data: str

    #: Column's name, as defined by :js:attr:`columns.name`.
    name: str

    #: Flag to indicate if this column is searchable (:data:`True`) or
    #: not (:data:`False`). This is controlled by :js:attr:`columns.searchable`.
    searchable: bool

    #: Flag to indicate if this column is orderable (:data:`True`) or
    #: not (:data:`False`). This is controlled by :js:attr:`columns.orderable`.
    orderable: bool

    #: Search information.
    search: Search


class Query(TypedDict):
    """Sent parameters.

    When making a request to the server using server-side processing,
    DataTables will send the following data in order to let the server
    know what data is required.

    """

    _: int

    #: Draw counter. This is used by DataTables to ensure
    #: that the Ajax returns from server-side processing
    #: requests are drawn in sequence by DataTables (Ajax
    #: requests are asynchronous and thus can return out
    #: of sequence). This is used as part of the ``draw``
    #: return parameter (see below).
    draw: int

    #: Paging first record indicator. This is the start
    #: point in the current data set (0 index based - i.e.
    #: 0 is the first record).
    start: int

    #: Number of records that the table can display in the
    #: current draw. It is expected that the number of records
    #: returned will be equal to this number, unless the server
    #: has fewer records to return. Note that this can be -1 to
    #: indicate that all records should be returned (although
    #: that negates any benefits of server-side processing!)
    length: int

    #: Search information.
    search: Search

    #: Ordering information.
    order: List[Order]

    #: Column data.
    columns: List[Column]


#: Server-side processing return using arrays as the data source for the table.
ArrayData = List[Any]


class ObjectData(TypedDict, total=False):
    """Server-side processing return using objects."""

    #: Set the ID property of the ``tr`` node to this value.
    DT_RowId: str

    #: Add this class to the ``tr`` node.
    DT_RowClass: str

    #: Add the data contained in the object to the row using the `jQuery`_
    #: :js:func:`data()` method to set the data, which can also then be used
    #: for later retrieval (for example on a click event).
    DT_RowData: Dict[str, Any]

    #: Add the data contained in the object to the row ``tr`` node as attributes.
    #: The object keys are used as the attribute keys and the values as the
    #: corresponding attribute values. This is performed using using the `jQuery`_
    #: :js:func:`param()` method. Please note that this option requires **DataTables
    #: 1.10.5** or newer.
    DT_RowAttr: Dict[str, Any]


class Response(TypedDict):
    """Returned data.

    Once DataTables has made a request for data, with the above
    parameters sent to the server, it expects JSON data to be
    returned to it, with the following parameters set.

    """

    #: The draw counter that this object is a response to - from
    #: the :attr:`~tekid.ext.datatables.Query.draw` parameter sent
    #: as part of the data request. Note that it is **strongly
    #: recommended for security reasons** that you cast this parameter
    #: to an integer, rather than simply echoing back to the client
    #: what it sent in the ``draw`` parameter, in order to prevent
    #: Cross Site Scripting (XSS) attacks.
    draw: int

    #: Total records, before filtering (i.e. the total number of
    #: records in the database)
    recordsTotal: int

    #: Total records, after filtering (i.e. the total number of records
    #: after filtering has been applied - not just the number of records
    #: being returned for this page of data).
    recordsFiltered: int

    #: The data to be displayed in the table. This is an array of data
    #: source objects, one for each row, which will be used by DataTables.
    #: Note that this parameter's name can be changed using the
    #: :js:data:`ajax` option's ``dataSrc`` property.
    data: List[Union[ArrayData, ObjectData]]

    #: *Optional*: If an error occurs during the running of the server-side
    #: processing script, you can inform the user of this error by passing
    #: back the error message to be displayed using this parameter. Do not
    #: include if there is no error.
    error: Optional[str]
