Quick Start
===========

After installing the package, set up environment variables using ``msdss-dotenv`` in a command line terminal:

.. code::
   
   msdss-dotenv init
   msdss-dotenv set MSDSS_DATABASE_DRIVER postgresql
   msdss-dotenv set MSDSS_DATABASE_USER msdss
   msdss-dotenv set MSDSS_DATABASE_PASSWORD msdss123
   msdss-dotenv set MSDSS_DATABASE_HOST localhost
   msdss-dotenv set MSDSS_DATABASE_PORT 5432
   msdss-dotenv set MSDSS_DATABASE_NAME msdss

In Python, use the package via :class:`msdss_base_database.core.Database` methods:

.. jupyter-execute::
   :hide-code:

   from msdss_base_dotenv.tools import clear_env_file
   clear_env_file()

.. jupyter-execute::

   from msdss_base_database import Database

   # Initiate a connection, assuming env vars set
   db = Database()

   # Check if the table exists and drop if it does
   if db.has_table("test_table"):
         db.drop_table("test_table")

   # Create sample table
   columns = [
      dict(name='id', type_='Integer', primary_key=True),
      ('column_one', 'String'),
      ('column_two', 'Integer')
   ]
   db.create_table('test_table', columns)

   # Write sample data
   data = {
         'id': [1, 2, 3],
         'column_one': ['a', 'b', 'c'],
         'column_two': [2, 4, 6]
   }
   db.insert('test_table', data)

   # Read the table to a pandas dataframe
   df = db.select('test_table')

   # Insert values into the table
   new = {
      'id': [5, 6, 7],
      'column_one': ['e', 'f', 'g'],
      'column_two': [10, 12, 14]
   }
   db.insert('test_table', new)
   df_insert = db.select('test_table')

   # Delete rows from the table
   db.delete(
      'test_table',
      where=('id', '=', 5)
   )
   df_delete = db.select('test_table')

   # Update values in table
   db.update(
      'test_table',
      where=('id', '>', 3),
      values={'column_one': 'AA'})
   df_update = db.select('test_table')

   # Display results
   print('df:')
   print(df)
   print('\ndf_insert:')
   print(df_insert)
   print('\ndf_delete:')
   print(df_delete)
   print('\ndf_update:')
   print(df_update)

.. jupyter-execute::
   :hide-code:

   from msdss_base_dotenv.tools import clear_env_file
   clear_env_file()
