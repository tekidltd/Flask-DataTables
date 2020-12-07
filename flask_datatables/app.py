# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Core Application
======================


.. _DataTables: https://datatables.net/

"""

from typing import Any, Dict, Optional, Union

import flask
import peewee

from .database import Database
from .model import Model

__all__ = ['DataTables']

# ``database`` parameter acceptable types
DBConfig = Union[Dict[str, Any], str, peewee.Database]


class DataTables:
    """Server-side processing integration with `DataTables`_.

    Args:
        app: :class:`flask.Flask` instance to integrate `DataTables`_.

    """

    def __init__(self, app: Optional[flask.Flask] = None,
                 database: Optional[DBConfig] = None,
                 model_class: peewee.Model = Model):
        #: flask.Flask: :class:`flask.Flask` instance to integrate `DataTables`_.
        self.app = app
        #: peewee.Database: Database connection instance.
        self.database = None
        #: peewee.Model: Base class for data models.
        self.base_model_class = model_class

        self._db_config = database
        self._db_wrapper = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app: flask.Flask) -> None:
        """Initialise the :class:`~flask_datatables.app.DataTables` with the :class:`~flask.Flask` application.

        Args:
            app: :class:`flask.Flask` instance to integrate `DataTables`_.

        """
        self.db_wrapper = Database(
            app=app,
            database=self._db_config,
            model_class=self.base_model_class
        )
        self.database = self.db_wrapper.database

        app.extensions['datatables'] = self
        self.app = app
