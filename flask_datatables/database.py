# -*- coding: utf-8 -*-
# pylint: disable=unsubscriptable-object
"""Database Connection
=========================

We made some monkeypatch for :mod:`peewee` and :mod:`playhouse.flask_utils`
in order to better support the integration with :mod:`Flask`.

.. _DataTables: https://datatables.net/

"""

from typing import TYPE_CHECKING

import playhouse.flask_utils

from .model import Model

if TYPE_CHECKING:
    from typing import Any, Dict, Optional, Type, Union

    from flask import Flask
    from playhouse.flask_utils import FlaskDB as Database

    # ``database`` parameter acceptable types
    DBConfig = Union[Dict[str, Any], str, Database]

__all__ = ['DataTable']


class DataTable(playhouse.flask_utils.FlaskDB):
    """Server-side processing integration with `DataTables`_.

    Args:
        app: :class:`flask.Flask` instance to integrate `DataTables`_.
        database: Database connection configurations.
        model_class: :class:`flask_datatables.model.Model` class to create
            data models.

    """

    #: Database connection instance.
    database: 'Database'
    #: Base class for data models.
    base_model_class: 'Model'
    #: :class:`flask.Flask` instance to integrate `DataTables`_.
    _app: 'Flask'
    #: Database connection configurations.
    _db: 'DBConfig'

    def __init__(self, app: 'Optional[Flask]' = None,
                 database: 'Optional[DBConfig]' = None,
                 model_class: 'Optional[Type[Model]]' = None):
        if model_class is None:
            model_class = Model
        super().__init__(app, database, model_class)

    def init_app(self, app: 'Flask') -> None:
        """Initialise the :class:`~flask_datatables.app.DataTables` with the :class:`~flask.Flask` application.

        Args:
            app: :class:`flask.Flask` instance to integrate `DataTables`_.

        """
        super().init_app(app)
        app.extensions['datatables'] = self
