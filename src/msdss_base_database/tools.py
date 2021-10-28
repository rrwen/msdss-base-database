import os
import sqlalchemy

from msdss_base_dotenv import env_exists, load_env_file

def get_database_url(
    driver,
    user=None,
    password=None,
    host=None,
    port=None,
    database=None,
    load_env=True,
    env_file='./.env',
    key_path=None,
    driver_key='MSDSS_DATABASE_DRIVER',
    user_key='MSDSS_DATABASE_USER',
    password_key='MSDSS_DATABASE_PASSWORD',
    host_key='MSDSS_DATABASE_HOST',
    port_key='MSDSS_DATABASE_PORT',
    database_key='MSDSS_DATABASE_NAME',
    *args, **kwargs):
    """
    Form database connection url from parameters or an environmental variables file.
    
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
    load_env : bool
        Whether to load variables for connecting from a file with environmental variables at ``env_file`` or not.
    env_file : str
        The path of the file with environmental variables.
    key_path : str
        The path of the key file for the ``env_file``.
    driver_key : str
        The environmental variable name for ``driver``.
    user_key : str
        The environmental variable name for ``user``.
    password_key : str
        The environmental variable name for ``password``.
    host_key : str
        The environmental variable name for ``key``.
    port_key : str
        The environmental variable name for ``port``.
    database_key : str
        The environmental variable name for ``database``.
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
    
    # (get_database_url_env) Load env if it exists
    has_env = env_exists(file_path=env_file, key_path=key_path)
    if load_env and has_env:
        load_env_file(file_path=env_file, key_path=key_path)
        driver = os.getenv(driver_key, driver)
        user = os.getenv(user_key, user)
        password = os.getenv(password_key, password)
        host = os.getenv(host_key, host)
        port = os.getenv(port_key, port)
        database = os.getenv(database_key, database)
    
    # (get_database_url_return) Get a str of the database url
    out = str(sqlalchemy.engine.URL.create(drivername=driver, username=user, password=password, host=host, port=port, database=database, *args, **kwargs))
    return out