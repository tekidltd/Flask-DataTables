# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Database Connection
=========================

We made some monkeypatch for :mod:`peewee` and :mod:`playhouse.flask_utils`
in order to better support the integration with :mod:`Flask`.

.. _DataTables: https://datatables.net/

"""

import contextlib
from typing import Any, Dict, Optional, Union

import flask
import peewee
import playhouse.flask_utils

from .model import Model

__all__ = ['Database']

# ``database`` parameter acceptable types
DBConfig = Union[Dict[str, Any], str, peewee.Database]


class Database(playhouse.flask_utils.FlaskDB):
    """Server-side processing integration with `DataTables`_.

    Args:
        app: :class:`flask.Flask` instance to integrate `DataTables`_.
        database: Database connection configurations.
        model_class: :class:`flask_datatables.model.Model` class to create
            data models.

    """

    #: Database connection instance.
    database: peewee.Database
    #: Base class for data models.
    base_model_class: Model
    #: :class:`flask.Flask` instance to integrate `DataTables`_.
    _app: flask.Flask
    #: Database connection configurations.
    _db: DBConfig

    def __init__(self, app: Optional[flask.Flask] = None,
                 database: Optional[DBConfig] = None,
                 model_class: Optional[peewee.Model] = None):
        if model_class is None:
            model_class = Model
        super().__init__(app, database, model_class)

    def init_app(self, app: flask.Flask) -> None:
        """Initialise the :class:`~flask_datatables.app.DataTables` with the :class:`~flask.Flask` application.

        Args:
            app: :class:`flask.Flask` instance to integrate `DataTables`_.

        """
        super().init_app(app)
        app.extensions['datatables'] = self

    def connect_db(self) -> None:
        """Connect to database before handling request.

        We monkeypatched the original :meth:`playhouse.flask_utils.FlaskDB.connect_db`
        to make sure that it shall never fail in case of :exc:`peewee.OperationalError`
        and :exc:`peewee.InterfaceError` being raised.

        """
        with contextlib.suppress(peewee.OperationalError, peewee.InterfaceError):
            return super().connect_db()
