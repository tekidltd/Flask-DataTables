# -*- coding: utf-8 -*-
"""Database Connection
=========================

We made some monkeypatch for :mod:`peewee` and :mod:`playhouse.flask_utils`
in order to better support the integration with :mod:`Flask`.

"""

import contextlib

import peewee
import playhouse.flask_utils

__all__ = ['Database']


class Database(playhouse.flask_utils.FlaskDB):
    """Monkeypatch for :class:`playhouse.flask_utils.FlaskDB`."""

    def connect_db(self) -> None:
        """Connect to database before handling request.

        We monkeypatched the original :meth:`playhouse.flask_utils.FlaskDB.connect_db`
        to make sure that it shall never fail in case of :exc:`peewee.OperationalError`
        and :exc:`peewee.InterfaceError` being raised.

        """
        with contextlib.suppress(peewee.OperationalError, peewee.InterfaceError):
            return super().connect_db()
