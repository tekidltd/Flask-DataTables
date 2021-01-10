.. automodule:: flask_datatables.model
   :no-members:

.. autoclass:: flask_datatables.model.Model
   :no-members:
   :show-inheritance:

   To ease the :class:`~flask_datatables.model.Model` class from recursively
   processing its field data, we added the following two attributes to save
   the `DataTables`_ integrated fields data.

   .. autoattribute:: dt_orderable
   .. autoattribute:: dt_searchable

   .. automethod:: validate_model
   .. automethod:: save
   .. automethod:: search

.. autoclass:: flask_datatables.model.Metadata
   :members:
   :show-inheritance:
   :private-members:
