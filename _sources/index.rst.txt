.. Flask-DataTables documentation master file, created by
   sphinx-quickstart on Thu Dec 10 21:53:00 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask & peewee integration with DataTables server-side processing
=================================================================

.. toctree::
   :maxdepth: 2

   database
   model
   fields
   utils
   typing

As `DataTables`_ is a quite power and useful JavaScript library for manipulating
and displaying data, we intended to make integration of the client-side DataTables
scripts with the server-side processing based on ``Flask`` and ``peewee``.

Installation
------------

.. note::

   As we have noticed, there's already a ``Flask-DataTables`` library available
   on `PyPI`_. However, this package was intended for integration with ``SQLAlchemy``
   instead of ``peewee``.

   .. _PyPI: https://pypi.org/project/Flask-DataTables/

To start with, simply install the ``Flask-DataTables`` package from
`PyPI <https://pypi.org/project/Flask-DataTables-peewee>`__:

.. code-block:: shell

   pip install Flask-DataTables-peewee

or should you prefer the bleeding edge version:

.. code-block:: shell

   git clone https://github.com/JarryShaw/Flask-DataTables.git
   cd Flask-DataTables
   pip install .

Usage
-----

``Flask-DataTables`` is quite simple to use, just declare your data model in
the preferable way from ``peewee`` and voilà, that's it.

Taking examples from the ``peewee`` `documentation <http://docs.peewee-orm.com/en/latest/peewee/playhouse.html>`__,
we can have a `DataTables`_ integrated data model just as below:

.. code-block:: python

   from flask import Flask
   from flask_datatables import (CharField, DataTable, DateTimeField,
                                 ForeignKeyField, Metadata, TextField)

   DATABASE = 'postgresql://postgres:password@localhost:5432/my_database'

   app = Flask(__name__)
   app.config.from_object(__name__)

   db_wrapper = DataTable(app)


   class User(db_wrapper.Model):
       username = CharField(unique=True)

       class Meta(Metadata):
           datatables = True


   class Tweet(db_wrapper.Model):
       user = ForeignKeyField(User, backref='tweets')
       content = TextField()
       timestamp = DateTimeField(default=datetime.datetime.now)

       class Meta(Metadata):
           datatables = True

And now, you may simply call :meth:`Tweet.search <flask_datatables.model.Model.search>`
to perform the server-side processing queries.

.. seealso::

   It is also possible to customise the orderable and/or searchable
   fields through :class:`~flask_datatables.fields.Field` parameters,
   and their corresponding behaviours by subclassing the
   :class:`~flask_datatables.fields.Field` classes.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _DataTables: https://datatables.net/
