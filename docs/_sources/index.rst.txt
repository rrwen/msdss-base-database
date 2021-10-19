msdss-base-database
===================

Base database for the Modular Spatial Decision Support Systems (MSDSS) framework.

* `PyPi <https://pypi.org/project/msdss-base-database>`_
* `Github <https://www.github.com/rrwen/msdss-base-database>`_
* `License <https://github.com/rrwen/msdss-base-database/blob/main/LICENSE>`_

Install
=======

1. Install `Anaconda 3 <https://www.anaconda.com/>`_ for Python
2. Install ``msdss-base-database`` via pip or through a conda environment

.. code::

   conda create -n msdss-base-database python=3.8
   conda activate msdss-base-database
   pip install msdss-base-database

Quick Start
===========

After installing the package, use in Python via methods:

.. jupyter-execute::
   :hide-output:

   from msdss_base_database import Database

   # Initiate a connection with the default test user and database
   db = Database(
      driver="postgresql",
      user="msdss",
      password="msdss123",
      host="localhost",
      port="5432",
      database="msdss"
   )

   # Create sample table
   data = {
      'id': [1, 2, 3],
      'column_one': ['a', 'b', 'c'],
      'column_two': [2, 4, 6]
   }
   db.create_table('test_table', data, replace=True)

   # Read the table to a pandas dataframe
   df = db.select('test_table')

   # Insert values into the table
   new = {
      'id': [5, 6, 7],
      'column_one': ['e', 'f', 'g'],
      'column_two': [10, 12, 14]
   }
   db.insert('test_table', new)

   # Delete rows from the table
   db.delete(
      'test_table',
      where=('id', '=', 5)
   )

   # Update values in table
   db.update(
      'test_table',
      where=('id', '>', 3),
      values={'column_one': 'AA'})

   # Check if the table exists and drop if it does
   if db.has_table("test_table"):
      db.drop_table("test_table")

How it Works
============

The :class:`msdss_base_database.core.Database` class wraps around `sqlalchemy <https://www.sqlalchemy.org/>`_ for managing databases and `pandas <https://pandas.pydata.org/>`_ for convenient data processing.

``sqlalchemy`` is used for creating connections, building query statements, and executing queries, while ``pandas`` is used for bulk reading and writing data from and to databases.

.. digraph:: methods

   rankdir=TB;

   sqlalchemy[label="SQLAlchemy" URL="https://www.sqlalchemy.org/" style=filled];
   
   select[label=".select()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=select#sqlalchemy.schema.Table.select"];
   insert[label=".insert()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=insert#sqlalchemy.schema.Table.insert"];
   update[label=".update()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=update#sqlalchemy.schema.Table.update"];
   drop[label=".drop()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=drop#sqlalchemy.schema.Table.drop"];
   delete[label=".delete()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=delete#sqlalchemy.schema.Table.delete"];
   hastable[label=".has_table()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/internals.html?highlight=has_table#sqlalchemy.engine.default.DefaultDialect.has_table"];
   execute[label=".execute()" shape=rect style=rounded URL="https://docs.sqlalchemy.org/en/14/core/connections.html?highlight=execute#sqlalchemy.engine.Connection.execute"];
   
   engine[label=".Engine" shape=rect URL="https://docs.sqlalchemy.org/en/14/core/connections.html?highlight=engine#sqlalchemy.engine.Engine"];
   inspector[label=".Inspector" shape=rect URL="https://docs.sqlalchemy.org/en/14/core/reflection.html?highlight=inspector#sqlalchemy.engine.reflection.Inspector"];
   connection[label=".Connection" shape=rect URL="https://docs.sqlalchemy.org/en/14/core/connections.html?highlight=connection#sqlalchemy.engine.Connection"];
   table[label=".Table" shape=rect URL="https://docs.sqlalchemy.org/en/14/core/metadata.html?highlight=table#sqlalchemy.schema.Table"];

   pandas[label="pandas" URL="https://pandas.pydata.org/" style=filled];
   
   readsql[label=".read_sql()" shape=rect style=rounded URL="https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html"];
   tosql[label=".to_sql()" shape=rect style=rounded URL="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html?highlight=to_sql"];

   dataframe[label=".DataFrame" shape=rect URL="https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html?highlight=dataframe#pandas.DataFrame"];

   subgraph cluster {
      label=< <B>msdss_base_database.core.Database</B> >;

      style=rounded;
      {rank=min; sqlalchemy -> pandas;}

      engine -> sqlalchemy[arrowhead=none];
      engine -> table -> {select;insert;update;drop;delete} -> connection -> execute;
      engine -> inspector -> hastable;

      dataframe -> pandas[arrowhead=none];
      dataframe -> {readsql;tosql};
   }

API Reference
=============

.. autoclass:: msdss_base_database.core.Database
    :members:

Contact
=======

Richard Wen <rrwen.dev@gmail.com>

.. toctree:: 
   :maxdepth: 2
   :hidden:

   index