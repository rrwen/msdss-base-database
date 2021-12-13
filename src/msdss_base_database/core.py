import pandas
import sqlalchemy

from .defaults import *
from .env import *
from .tools import *

class Database:
    """
    Class for MSDSS database management.

    Parameters
    ----------
    driver : str
        The driver name of the database connection, which are commonly ``postgresql``, ``sqlite``, ``mysql``, ``oracle`` or ``mssql`` (see `SQLAlchemy supported databases <https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases>`_).
    user : str
        User name for the connection.
    password : str
        Password for the user.
    host : str
        Host address of the connection.
    port : str
        Port number of the connection.
    database : str
        Database name of the connection.
    load_env : bool
        Whether to load the environmental variables using parameter ``env`` or not.  The environment will only be loaded if the ``env_file`` exists.
    env : :class:`msdss_base_database.env.DatabaseDotEnv` or bool
        An object to set environment variables related to database configuration.
        These environment variables will overwrite the parameters above if they exist.

        By default, the parameters above are assigned to each of the environment variables below:

        .. jupyter-execute::
            :hide-code:

            from msdss_base_database.defaults import DEFAULT_DOTENV_KWARGS
            defaults = {k:v for k, v in DEFAULT_DOTENV_KWARGS.items() if k not in ['defaults', 'env_file', 'key_path']}
            print('<parameter> = <environment variable>\\n')
            for k, v in defaults.items():
                print(k + ' = ' + v)

    *args, **kwargs
        Additional arguments passed to :func:`sqlalchemy:sqlalchemy.create_engine`.

    Attributes
    ----------
    _connection : :class:`sqlalchemy.engine.base.Engine`
        The database engine object from `sqlalchemy <https://www.sqlalchemy.org/>`_.
    _inspector: :class:`sqlalchemy.engine.reflection.Inspector`
        The database inspector object from `sqlalchemy <https://www.sqlalchemy.org/>`_.
    _metadata : :class:`sqlalchemy.schema.MetaData`
        The metadata object from `sqlalchemy <https://www.sqlalchemy.org/>`_.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_database import Database

        # Initiate a connection with the default test user and database
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

        # Skip a row
        df_skip = db.select('test_table', offset=1)

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
        print('df:\\n')
        print(df)
        print('\\ndf_skip:\\n')
        print(df_skip)
        print('\\ndf_insert:\\n')
        print(df_insert)
        print('\\ndf_delete:\\n')
        print(df_delete)
        print('\\ndf_update:\\n')
        print(df_update)
    """
    def __init__(
        self,
        driver=DEFAULT_DOTENV_KWARGS['defaults']['driver'],
        user=DEFAULT_DOTENV_KWARGS['defaults']['user'],
        password=DEFAULT_DOTENV_KWARGS['defaults']['password'],
        host=DEFAULT_DOTENV_KWARGS['defaults']['host'],
        port=DEFAULT_DOTENV_KWARGS['defaults']['port'],
        database=DEFAULT_DOTENV_KWARGS['defaults']['database'],
        load_env=True,
        env=DatabaseDotEnv(),
        *args, **kwargs):
        
        # (Database_connect_str) Build connection str from parameters
        connection_str = get_database_url(
            driver=driver,
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            load_env=load_env,
            env=env
        )

        # (Database_attr) Create attributes for database obj
        self._connection = sqlalchemy.create_engine(connection_str, *args, **kwargs)
        self._inspector = sqlalchemy.inspect(self._connection)
        self._metadata = sqlalchemy.MetaData(bind=self._connection)
    
    def _build_query(
        self,
        table,
        select=None,
        where=None,
        group_by=None,
        aggregate=None,
        aggregate_func='count',
        order_by=None,
        order_by_sort='asc',
        limit=None,
        offset=None,
        where_boolean='AND',
        update=False,
        delete=False,
        values=None,
        *args, **kwargs):
        """
        Get a SQL select statement using sqlalchemy functions.
        
        Parameters
        ----------
        table : str
            Name of the database table.
        select : str or list(str) or list(:class:`sqlalchemy:sqlalchemy.schema.Column`) or None
            List of column names or a single column name to filter or select from the table. If ``None`` then all columns will be selected.
        where : list of list or list of tuple or None
            list of where statements the form of ``['column_name', 'operator', value]`` to further filter individual values or rows.

            * Operators are one of:

                .. jupyter-execute::
                    :hide-code:

                    from msdss_base_database.defaults import DEFAULT_SUPPORTED_OPERATORS
                    for operator in DEFAULT_SUPPORTED_OPERATORS:
                        print(operator)
                        
            * Values can be any single value such as ``int`` or ``str``
            * Examples: ``['column_two', '>', 2]``, ``['column_one', 'LIKE', 'a']``, ``[['column_two', '>', 2], ['column_one', 'LIKE', 'a']]``
        
        group_by : str or list(str) or None
            Single or list of column names to group by. This should be used with ``aggregate`` and ``aggregate_func``.
        aggregate : str or list(str) or None
            Single or list of column names to aggregate using the ``aggregate_func``. This should be used with ``group_by`` and ``aggregate_func``.
        aggregate_func : str or list(str)
            Function name (such as 'count' or 'sum') from :class:`sqlalchemy:sqlalchemy.sql.functions.Function` for aggregating records from each ``aggregate`` column.
            If a list of str, then it must have the same number of elements as ``aggregate`` or else only the shortest length list will be used.
        order_by : str or list(str) or None
            Single or list of column names to order or sort by.
        order_by_sort : str or list(str)
            Sort the records in increasing or decreasing order by each column in ``order_by``, where the value can be one of 'asc' for ascending or 'desc' for descending'.
            If a list of str, then it must have the same number of elements as ``order_by`` or else only the shortest length list will be used.
        limit : int or None
            Integer number to limit the number of rows returned.
        offset : int or None
            Number of rows to skip for the query.
        where_boolean : str
            One of ``AND`` or ``OR`` to combine ``where`` statements with. Defaults to ``AND`` if not one of ``AND`` or ``OR``.
        update : bool
            Whether to update rows from the table matching the query or not. Overrides the ``select`` parameter.
        delete : bool
            Whether to delete rows from the table matching the query or not. Overrides the ``select`` and ``update`` parameters.
        values : dict
            A dictionary of values to use for update if the ``update`` parameter is ``True`` and not overridden.
        *args, **kwargs
            Additional arguments to accept any extra parameters passed through.
        
        Returns
        -------
        :class:`sqlalchemy:sqlalchemy.sql.expression.Select`
            sqlalchemy object that represents a table in the database.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
            
            # Setup database
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
            
            # Select columns and limit to 6 rows
            sql_limit = db._build_query(
                'test_table',
                select = ['column_one', 'column_two'],
                limit=6
            )

            # Select columns with where statement
            sql_where = db._build_query(
                'test_table',
                select='column_one',
                where=[('column_two', '<', 3), ('column_one', '=', 'b')],
                where_boolean='AND'
            )

            # Select columns and order each column
            sql_order = db._build_query(
                'test_table',
                select=['column_one', 'column_two'],
                order_by=['column_one', 'column_two'],
                order_by_sort=['asc', 'desc']
            )
            
            # Select columns, group, and aggregate data
            sql_agg = db._build_query(
                'test_table',
                select='column_one',
                group_by='column_one',
                aggregate=['column_two', 'column_one'],
                aggregate_func=['sum', 'count']
            )

            # Update rows
            sql_update = db._build_query(
                'test_table',
                where=[('id', '=', 1)],
                values=dict(column_one='A'),
                update=True
            )

            # Delete rows
            sql_delete = db._build_query(
                'test_table',
                where=[('column_two', '<', 2), ('column_one', '=', 'a')],
                where_boolean='OR',
                delete=True
            )

            # Display gen statements
            print('sql_limit:\\n\\n' + str(sql_limit))
            print('\\nsql_where:\\n\\n' + str(sql_where))
            print('\\nsql_order:\\n\\n' + str(sql_order))
            print('\\nsql_agg:\\n\\n' + str(sql_agg))
            print('\\nsql_update:\\n\\n' + str(sql_update))
            print('\\nsql_delete:\\n\\n' + str(sql_delete))
        """
        
        # (Database_build_query_var_list) Format single variables into lists
        select = [select] if isinstance(select, str) else select
        group_by = [group_by] if isinstance(group_by, str) else group_by
        aggregate = [aggregate] if isinstance(aggregate, str) else aggregate
        order_by = [order_by] if isinstance(order_by, str) else order_by
                
        # (Database_build_query_table) Get the table object
        target = self._get_table(table)
        
        # (Database_build_query_select) Gather columns to select
        select_columns =  [target] if select is None else [target.c[c] for c in select]
        
        # (Database_build_query_aggregate) Gather aggregation columns to select
        if aggregate is not None:
            aggregate_columns = [target.c[c] for c in aggregate]
            if isinstance(aggregate_func, list):
                aggregate_labels = [a + '_' + f for a, f in zip(aggregate, aggregate_func)]
                aggregate_columns = [getattr(sqlalchemy.func, f.lower())(c).label(l) for c, f, l in zip(aggregate_columns, aggregate_func, aggregate_labels)]
            else:
                aggregate_labels = [a + '_' + aggregate_func for a in aggregate]
                aggregate_columns = [getattr(sqlalchemy.func, aggregate_func)(c).label(l) for c, l in zip(aggregate_columns, aggregate_labels)]
            select_columns = select_columns + aggregate_columns
            
        # (Database_build_query_operation) Add select, update, or delete statement
        if delete:
            out = target.delete()
        elif update:
            out = target.update()
        else:
            out = sqlalchemy.select(select_columns)
        
        # (Database_build_query_where) Add where statement
        if where is not None:

            # (Database_build_query_where_format) Get where boolean operator and ensure two-dimensional list
            where = [where] if not any(isinstance(w, list) or isinstance(w, tuple) for w in where) else where
            where_boolean = sqlalchemy.or_ if where_boolean.lower() == 'or' else sqlalchemy.and_
            
            # (Database_build_query_where_convert) Convert list to where clauses
            where_clauses = []
            for clause_list in where:

                # (Database_build_query_where_convert_vars) Get clause parts from list
                clause_col = clause_list[0]
                clause_op = clause_list[1]
                clause_val = clause_list[2]

                # (Database_build_query_where_convert_op) Convert to clause based on operator
                if clause_op in ('=', '=='):
                    clause = target.c[clause_col] == clause_val
                elif clause_op in ('!=', '!=='):
                    clause = target.c[clause_col] != clause_val
                elif clause_op == '>':
                    clause = target.c[clause_col] > clause_val
                elif clause_op == '>=':
                    clause = target.c[clause_col] >= clause_val
                elif clause_op == '<':
                    clause = target.c[clause_col] < clause_val
                elif clause_op == '<=':
                    clause = target.c[clause_col] <= clause_val
                elif clause_op.lower() == 'like':
                    clause = target.c[clause_col].like(clause_val)
                elif clause_op.lower() == 'notlike':
                    clause = target.c[clause_col].notlike(clause_val)
                elif clause_op.lower() == 'ilike':
                    clause = target.c[clause_col].ilike(clause_val)
                elif clause_op.lower() == 'notilike':
                    clause = target.c[clause_col].notilike(clause_val)
                elif clause_op.lower() == 'contains':
                    clause = target.c[clause_col].contains(clause_val)
                elif clause_op.lower() == 'startswith':
                    clause = target.c[clause_col].startswith(clause_val)
                elif clause_op.lower() == 'endswith':
                    clause = target.c[clause_col].endswith(clause_val)
                else:
                    raise ValueError(clause_op + ' is not supported')
                where_clauses.append(clause)

            # (Database_build_query_where_add) Add where clauses to select query
            out = out.where(where_boolean(*where_clauses))
            
        # (Database_build_query_group) Add group by statement
        if group_by is not None:
            group_by_columns = [target.c[c] for c in group_by]
            out = out.group_by(*group_by_columns)
            
        # (Database_build_query_order) Add order by statement
        if order_by is not None:
            order_by_columns = [target.c[c] for c in order_by]
            if isinstance(order_by_sort, list):
                order_by_columns = [getattr(c, s.lower())() for c, s in zip(order_by_columns, order_by_sort)]
            else:
                order_by_columns = [getattr(c, order_by_sort)() for c in order_by_columns]
            out = out.order_by(*order_by_columns)

        # (Database_build_query_offset) Add offset statement
        if offset is not None:
            out = out.offset(offset)
            
        # (Database_build_query_limit) Add limit statement
        if limit is not None:
            out = out.limit(limit)

        # (Database_build_query_values) Add values statement
        if values is not None and update:
            out = out.values(**values)
            
        # (Database_build_query_return) Return the sqlalchemy query
        return out

    def _execute_query(self, sql, *args, **kwargs):
        """
        Executes a query statement.
        
        Parameters
        ----------
        sql : str
            SQL str representing the query statement to execute.
        *args, **kwargs
            Additional parameters passed to :func:`sqlalchemy:sqlalchemy.engine.Connection.execute`.
        
        Returns
        -------
        :class:`sqlalchemy:sqlalchemy.engine.CursorResult`
            Cursor result from query.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
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
            
            # Get data from query
            cursor = db._execute_query('SELECT * FROM test_table LIMIT 5;')
            cursor = db._execute_query('SELECT column_one, column_two FROM test_table WHERE column_two > 3;')
        """
        with self._connection.connect() as connection:
            out = connection.execute(sql, *args, **kwargs)
            return out

    def _get_table(self, table, *args, **kwargs):
        """
        Get a table object from the database.

        Parameters
        ----------
        table : str
            Name of the table to remove.
        *args, **kwargs
            Additional arguments passed to :class:`sqlalchemy.schema.Table`.

        Return
        ------
        :class:`sqlalchemy.schema.Table`
            A ``Table`` object from ``sqlalchemy``.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
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

            # Get the table object
            tb = db._get_table('test_table')
            print(str(tb))
        """
        out = sqlalchemy.Table(table, self._metadata, autoload_with=self._connection, *args, **kwargs)
        return out

    def _list_to_columns(self, clist):
        """
        Converts a list of dict or list to ``sqlalchemy`` columns.

        Parameters
        ----------
        clist : list(dict) or list(list)
            List of dict (kwargs) or lists (positional args) that are passed to :class:`sqlalchemy.schema.Column`. Data types can also be specified as str.
            
            * Example list(dict): ``[dict(name='id', type_='Integer', autoincrement=True, primary_key=True), dict(name='col', type='String')]``
            * Example list(list): ``[('id', 'Integer'), ('col', 'String')]``
        *args, **kwargs
            Additional arguments passed to :class:`sqlalchemy.schema.Table`.

        Return
        ------
        list(:class:`sqlalchemy.schema.Column`)
            A list of ``Column`` objects from ``sqlalchemy``.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
            db = Database()

            # Create column definitions
            clist = [
                dict(name='id', type_='Integer', primary_key=True),
                dict(name='column_one', type_='String'),
                dict(name='column_two', type_='Integer')
            ]

            # Convert to sqlalchemy column objects
            columns = db._list_to_columns(clist)
            print(str(columns))
        """

        # (Database_list_to_columns_convert) Convert data types from str
        clist = [list(c) if isinstance(c, tuple) else c for c in clist] # conv tuples to list
        for i, c in enumerate(clist):

            # (Database_list_to_columns_convert_type) Get data type depending on list or dict
            if isinstance(c, dict):
                cidx = 'type_'
            elif isinstance(c, list):
                cidx = 1
            ctype = c[cidx]
            
            # (Databse_list_columns_convert_str) Convert to column if str
            if isinstance(ctype, str):
                clist[i][cidx] = getattr(sqlalchemy, ctype)

        # (Database_list_to_columns_return) Return the list of sqlalchemy columns
        out = [sqlalchemy.Column(*c) if isinstance(c, list) else sqlalchemy.Column(**c) for c in clist]
        return out

    def _write_data(self, table, data, schema=None, if_exists='append', index=False, *args, **kwargs):
        """
        Write data to the database.
        
        Parameters
        ----------
        table : str
            Name of the table to write to.
        data : dict or list or :class:`pandas:pandas.DataFrame`
            Dataframe with the data to write to the database. If ``dict`` or ``list`` see :class:`pandas:pandas.DataFrame`.
        schema : str
            Name of the schema to for the table.
        if_exists : 'fail' or 'replace' or 'append'
            String indicating whether to throw an error (fail), replace the data, or append the data to the table if it already exists.
        index : bool
            Set to True to include the row indices as a column and False to omit them.
        *args, **kwargs
            Additional arguments passed to :class:`pandas:pandas.DataFrame` if parameter ``data`` is ``dict`` or ``list``.
        
        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>
        
        Example
        -------
        .. jupyter-execute::

            from msdss_base_database import Database
            
            # Setup database
            db = Database()

            # Check if the table exists and drop if it does
            if db.has_table("test_table"):
                db.drop_table("test_table")
            
            # Write data to table
            data = {
                'id': [1, 2, 3],
                'column_one': ['a', 'b', 'c'],
                'column_two': [2, 4, 6]
            }
            db._write_data('test_table', data, if_exists = 'replace')
        """
        data = pandas.DataFrame(data, *args, **kwargs) if not isinstance(data, pandas.DataFrame) else data
        data.to_sql(table, con = self._connection, schema = schema, if_exists = if_exists, index = index)
    
    def create_table(self, table, columns, *args, **kwargs):
        """
        Create a table in the database.
        
        Parameters
        ----------
        table : str
            Name of the table to create.
        columns : list(dict) or list(list)
            List of dict (kwargs) or lists (positional args) that are passed to :class:`sqlalchemy.schema.Column`. Data types can also be specified as str.
            
            * Example list(dict): ``[dict(name='id', type_='Integer', autoincrement=True, primary_key=True), dict(name='col', type='String')]``
            * Example list(list): ``[('id', 'Integer'), ('col', 'String')]``

        *args, **kwargs
            Additional arguments passed to :class:`msdss_base_database.core.Database._write` except that parameter ``if_exists`` is set to ``fail`` or ``replace`` only.
        
        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>
        
        Example
        -------
        .. jupyter-execute::

            from msdss_base_database import Database
            
            # Setup database
            db = Database()

            # Drop table if exists
            if db.has_table('test_table'):
                db.drop_table('test_table')

            # Create column definitions
            columns = [
                dict(name='id', type_='Integer', primary_key=True),
                dict(name='column_one', type_='String'),
                dict(name='column_two', type_='Integer')
            ]
            
            # Create the table
            db.create_table('test_table', columns)

            # View the table
            df = db.select('test_table')
            print(df)
        """
        columns = self._list_to_columns(columns)
        tb = sqlalchemy.Table(table, self._metadata, *columns, extend_existing=True)
        tb.create(self._connection)

    def delete(self, table, where, where_boolean='AND', *args, **kwargs):
        """
        Remove rows from a table in the database.

        Parameters
        ----------
        table : str
            Name of the table to remove rows from.
        where : list of list or list of tuple or None
            list of where statements the form of ``['column_name', 'operator', value]`` to further filter individual values or rows. 
            See parameter ``where`` in :meth:`msdss_base_database.core.Database._build_query`.
        where_boolean : str
            One of ``AND`` or ``OR`` to combine ``where`` statements with. Defaults to ``AND`` if not one of ``AND`` or ``OR``.
            
            * Operators are one of:

                .. jupyter-execute::
                    :hide-code:

                    from msdss_base_database.defaults import DEFAULT_SUPPORTED_OPERATORS
                    for operator in DEFAULT_SUPPORTED_OPERATORS:
                        print(operator)
                        
            * Values can be any single value such as ``int`` or ``str``
            * Examples: ``['column_two', '>', 2]``, ``['column_one', 'LIKE', 'a']``, ``[['column_two', '>', 2], ['column_one', 'LIKE', 'a']]``

        *args, **kwargs
            Additional arguments passed to :meth:`msdss_base_database.core.Database._execute_query`.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
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
            df = db.select('test_table')

            # Delete a row with matching id
            db.delete(
                'test_table',
                where=('id', '=', 1)
            )
            df_delete_id = db.select('test_table')

            # Delete a row with matching query
            db.delete(
                'test_table',
                where=[('id', '<', 3), ('column_one', '=', 'c')],
                where_boolean='OR'
            )
            df_delete_where = db.select('test_table')

            # Print results
            print('df:\\n')
            print(df)
            print('\\ndf_delete_id:\\n')
            print(df_delete_id)
            print('\\ndf_delete_where:\\n')
            print(df_delete_where)
        """
        sql = self._build_query(table=table, where=where, where_boolean=where_boolean, delete=True)
        cursor = self._execute_query(sql, *args, **kwargs)

    def drop_table(self, table, *args, **kwargs):
        """
        Remove a table from the database.

        Parameters
        ----------
        table : str
            Name of the table to remove.
        *args, **kwargs
            Additional arguments passed to :meth:`sqlalchemy.schema.Table.drop`.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
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
            before_drop = db.has_table('test_table')

            # Drop the table
            db.drop_table('test_table')
            after_drop = db.has_table('test_table')

            # Print results
            print('before_drop: ' + str(before_drop))
            print('after_drop: ' + str(after_drop))
        """
        tb = self._get_table(table)
        tb.drop(*args, **kwargs)

    def has_table(self, table, *args, **kwargs):
        """
        Check if a table exists.

        Parameters
        ----------
        table : str
            Name of the table to check.
        *args, **kwargs
            Additional arguments passed to :meth:`sqlalchemy.engine.reflection.Inspector.has_table`.

        Return
        ------
        bool
            Returns ``True`` if the table exists and ``False`` otherwise.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
            db = Database()

            # Drop the table if it exists
            if db.has_table('test_table'):
                db.drop_table('test_table')
            before_create = db.has_table('test_table') # False
            
            # Create sample table
            columns = [
                dict(name='id', type_='Integer', primary_key=True),
                ('column_one', 'String'),
                ('column_two', 'Integer')
            ]
            db.create_table('test_table', columns)

            # Check if table exists again
            after_create = db.has_table('test_table') # True

            # Print results
            print('before_create: ' + str(before_create))
            print('after_create: ' + str(after_create))
        """
        out = self._inspector.has_table(table, *args, **kwargs)
        return out

    def insert(self, table, data, *args, **kwargs):
        """
        Insert additional data to the database.
        
        Parameters
        ----------
        table : str
            Name of the table to insert additional data to.
        data : dict or list or :class:`pandas:pandas.DataFrame`
            Dataframe with the data to write to the database. If ``dict`` or ``list`` see :class:`pandas:pandas.DataFrame`.
        *args, **kwargs
            Additional arguments passed to :meth:`msdss_base_database.core.Database._write`. Except that ``if_exists`` is always set to ``append``.
        
        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>
        
        Example
        -------
        .. jupyter-execute::

            from msdss_base_database import Database
            
            # Setup database
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
            df = db.select('test_table')
            
            # Write data to table
            data = {
                'id': [1, 2, 3],
                'column_one': ['a', 'b', 'c'],
                'column_two': [2, 4, 6]
            }
            db.insert('test_table', data)
            df_insert = db.select('test_table')

            # Insert more new values to table
            more_new = {
                'id': [5, 6, 7],
                'column_one': ['e', 'f', 'g'],
                'column_two': [10, 12, 14]
            }
            db.insert('test_table', more_new)
            df_insert_more = db.select('test_table')

            # Display results
            print('df:\\n')
            print(df)
            print('\\ndf_insert:\\n')
            print(df_insert)
            print('\\ndf_insert_more:\\n')
            print(df_insert_more)
        """
        self._write_data(table=table, data=data, if_exists='append', *args, **kwargs)
    
    def select(
        self,
        table,
        select = None,
        where = None,
        group_by = None,
        aggregate = None,
        aggregate_func = 'count',
        order_by = None,
        order_by_sort = 'asc',
        limit = None,
        offset = None,
        where_boolean = 'AND',
        *args, **kwargs):
        """
        Query data from a table in the database.
        
        Parameters
        ----------
        table : str
            Name of the database table to query from.
        select : str or list(str or list:class:`sqlalchemy:sqlalchemy.schema.Column`) or None
            List of column names or a single column name to filter or select from the table. If ``None`` then all columns will be selected.
        where : list of list or list of tuple or None
            list of where statements the form of ``['column_name', 'operator', value]`` to further filter individual values or rows.
            
            * Operators are one of:

                .. jupyter-execute::
                    :hide-code:

                    from msdss_base_database.defaults import DEFAULT_SUPPORTED_OPERATORS
                    for operator in DEFAULT_SUPPORTED_OPERATORS:
                        print(operator)
                        
            * Values can be any single value such as ``int`` or ``str``
            * Examples: ``['column_two', '>', 2]``, ``['column_one', 'LIKE', 'a']``, ``[['column_two', '>', 2], ['column_one', 'LIKE', 'a']]``            

        group_by : str or list(str) or None
            Single or list of column names to group by. This should be used with ``aggregate`` and ``aggregate_func``.
        aggregate : str or list(str) or None
            Single or list of column names to aggregate using the ``aggregate_func``. This should be used with ``group_by`` and ``aggregate_func``.
        aggregate_func : str or list(str)
            Function name (such as 'count' or 'sum') from :class:`sqlalchemy:sqlalchemy.sql.functions.Function` for aggregating records from each ``aggregate`` column.
            If a list of str, then it must have the same number of elements as ``aggregate`` or else only the shortest length list will be used.
        order_by : str or list(str) or None
            Single or list of column names to order or sort by.
        order_by_sort : str or list(str)
            Sort the records in increasing or decreasing order by each column in ``order_by``, where the value can be one of 'asc' for ascending or 'desc' for descending'.
            If a list of str, then it must have the same number of elements as ``order_by`` or else only the shortest length list will be used.
        limit : int or None
            Integer number to limit the number of rows returned.
        offset : int or None
            Number of rows to skip for the query.
        where_boolean : str
            One of ``AND`` or ``OR`` to combine ``where`` statements with. Defaults to ``AND`` if not one of ``AND`` or ``OR``.
        *args, **kwargs
            Additional parameters passed to :meth:`pandas:pandas.read_sql`.
        
        Returns
        -------
        :class:`pandas:pandas.DataFrame`
            pandas dataframe containing the queried data.

        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>

        Example
        -------
        .. jupyter-execute::

            from msdss_base_database.core import Database
            
            # Setup database
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
            df = db.select('test_table')
            
            # Read data from table using select and limit
            data = db.select(
                'test_table',
                select = ['column_one', 'column_two'],
                limit = 5
            )
            df_select = db.select('test_table')

            # Use where statements
            data = db.select(
                'test_table',
                select = 'column_one',
                where = [('column_two', '<', '15'), ('column_one', '=', 'b')],
                where_boolean = 'AND'
            )
            df_where = db.select('test_table')

            # Order results
            data = db.select(
                'test_table',
                select = ['column_one', 'column_two'],
                order_by = ['column_one', 'column_two'],
                order_by_sort = ['asc', 'desc']
            )
            df_order = db.select('test_table')

            # Aggregate read
            data = db.select(
                'test_table',
                select = 'column_one',
                group_by = 'column_one',
                aggregate = 'column_two',
                aggregate_func = ['count', 'sum']
            )
            df_agg = db.select('test_table')

            # Display results
            print('df:\\n')
            print(df)
            print('\\ndf_select:\\n')
            print(df_select)
            print('\\ndf_where:\\n')
            print(df_where)
            print('\\ndf_order:\\n')
            print(df_order)
            print('\\ndf_agg:\\n')
            print(df_agg)
        """
        sql = self._build_query(
            table,
            select=select,
            where=where,
            group_by=group_by,
            aggregate=aggregate,
            aggregate_func=aggregate_func,
            order_by=order_by,
            order_by_sort=order_by_sort,
            limit=limit,
            offset=offset,
            where_boolean=where_boolean
        )
        out = pandas.read_sql(sql = sql, con = self._connection, *args, **kwargs)
        return out

    def update(self, table, where, values, *args, **kwargs):
        """
        Update a table from the database.
        
        Parameters
        ----------
        table : str
            Name of the table to update.
        where : list of list or list of tuple or None
            list of where statements the form of ``['column_name', 'operator', value]`` to update individual values or rows.
            
            * Operators are one of:

                .. jupyter-execute::
                    :hide-code:

                    from msdss_base_database.defaults import DEFAULT_SUPPORTED_OPERATORS
                    for operator in DEFAULT_SUPPORTED_OPERATORS:
                        print(operator)
                        
            * Values can be any single value such as ``int`` or ``str``
            * Examples: ``['column_two', '>', 2]``, ``['column_one', 'LIKE', 'a']``, ``[['column_two', '>', 2], ['column_one', 'LIKE', 'a']]``

        values : dict
            Dictionary representing values to update if they match the ``where`` parameter requirements.
        *args, **kwargs
            Additional arguments passed to :meth:`msdss_base_database.core.Database._execute_query`.
        
        Author
        ------
        Richard Wen <rrwen.dev@gmail.com>
        
        Example
        -------
        .. jupyter-execute::

            from msdss_base_database import Database
            
            # Setup database
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
            df = db.select('test_table')

            # Update values in table
            db.update(
                'test_table',
                where=('id', '>', 1),
                values={'column_one': 'AA'})
            df_update = db.select('test_table')
            
            # Print results
            print('df:\\n')
            print(df)
            print('\\ndf_update:\\n')
            print(df_update)
        """
        sql = self._build_query(table=table, where=where, values=values, update=True)
        cursor = self._execute_query(sql, *args, **kwargs)
