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