import sqlalchemy

from .defaults import *
from .env import DatabaseDotEnv


def get_database_url(
    driver=DEFAULT_DOTENV_KWARGS['defaults']['driver'],
    user=DEFAULT_DOTENV_KWARGS['defaults']['user'],
    password=DEFAULT_DOTENV_KWARGS['defaults']['password'],
    host=DEFAULT_DOTENV_KWARGS['defaults']['host'],
    port=DEFAULT_DOTENV_KWARGS['defaults']['port'],
    database=DEFAULT_DOTENV_KWARGS['defaults']['database'],
    load_env=False,
    env=DatabaseDotEnv(),
    *args, **kwargs):
    """
    Form database connection url from parameters or an environmental variables file.
    
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
        Whether to load the environmental variables using parameter ``env`` or not. The environment will only be loaded if the ``env_file`` exists.
    env : :class:`msdss_base_database.env.DatabaseDotEnv`
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
    if env.exists() and load_env:
        env.load()
        driver = env.get('driver', driver)
        user = env.get('user', user)
        password = env.get('password', password)
        host = env.get('host', host)
        port = env.get('port', port)
        database =  env.get('database', database)
    
    # (get_database_url_return) Get a str of the database url
    out = str(sqlalchemy.engine.URL.create(drivername=driver, username=user, password=password, host=host, port=port, database=database, *args, **kwargs))
    return out