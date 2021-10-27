import sqlalchemy

def get_database_url(driver, user=None, password=None, host=None, port=None, database=None, *args, **kwargs):
    """
    Form database 
    
    Parameters
    ----------
    driver : str or None
        The driver name of the database connection, which are commonly ``postgresql``, ``sqlite``, ``mysql``, ``oracle`` or ``mssql``.  (see `SQLAlchemy supported databases <https://docs.sqlalchemy.org/en/14/core/engines.html#supported-databases>`_).
    user : str or None
        User name for the connection.
    password : str or None
        Password for the user.
    host : str or None
        Host address of the connection.
    port : str or None
        Port number of the connection.
    database : str or None
        Database name of the connection.
    *args, **kwargs
        Additional arguments passed to :class:`sqlalchemy:sqlalchemy.engine.URL.create`.
    
    Returns
    -------
    str
        String representing the database connection url.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_database.tools import get_database_url
        
        url = get_database_url(
            driver='postgresql',
            user='msdss',
            password='msdss12',
            port='5432',
            database='msdss'
        )

        print(url)
    """
    out = str(sqlalchemy.engine.URL.create(drivername=driver, username=user, password=password, host=host, port=port, database=database, *args, **kwargs))
    return out