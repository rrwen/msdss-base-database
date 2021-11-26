from msdss_base_dotenv import DotEnv

from .defaults import DEFAULT_DOTENV_KWARGS

class DatabaseDotEnv(DotEnv):
    """
    Class to manage database environment variables.

    * Extends :class:`msdss_base_dotenv:msdss_base_dotenv.core.DotEnv`

    Parameters
    ----------
    env_file : str
        The path of the file with environmental variables.
    key_path : str
        The path of the key file for the ``env_file``.
    defaults : dict
        Default values for below parameters if they are not set:

        .. jupyter-execute::
            :hide-code:

            from msdss_base_database.defaults import DEFAULT_DOTENV_KWARGS
            defaults = DEFAULT_DOTENV_KWARGS['defaults']
            print('<parameter> = <default>\\n')
            for k, v in defaults.items():
                print(k + ' = ' + v)

    driver : str
        The environmental variable name for ``driver``.
    user : str
        The environmental variable name for ``user``.
    password : str
        The environmental variable name for ``password``.
    host : str
        The environmental variable name for ``key``.
    port : str
        The environmental variable name for ``port``.
    database : str
        The environmental variable name for ``database``.

    Author
    ------
    Richard Wen <rrwen.dev@gmail.com>

    Example
    -------
    .. jupyter-execute::

        from msdss_base_database.env import DatabaseDotEnv

        # Create the default database env
        dbenv = DatabaseDotEnv()
        dbenv.clear()

        # Create database env with diff host, port, and database var names
        # Also set defaults
        dbenv2 = DatabaseDotEnv(
            host='MSDSS_DATABASE_HOST_B',
            port='MSDSS_DATABASE_PORT_B',
            database='MSDSS_DATABASE_DATABASE_B',
            defaults = dict(
                host='localhost',
                database='msdss'
            )
        )

        # Set MSDSS_DATABASE_PORT_B
        dbenv2.set('port', '5432')

        # Get the value for MSDSS_DATABASE_PORT_B env var
        port = dbenv2.get('port')
        print(port)

        # Delete the value at MSDSS_DATABASE_PORT_B
        dbenv2.delete('port')

        # Clear the database env files
        dbenv2.clear()
    """
    def __init__(
        self,
        driver=DEFAULT_DOTENV_KWARGS['driver'],
        user=DEFAULT_DOTENV_KWARGS['user'],
        password=DEFAULT_DOTENV_KWARGS['password'],
        host=DEFAULT_DOTENV_KWARGS['host'],
        port=DEFAULT_DOTENV_KWARGS['port'],
        database=DEFAULT_DOTENV_KWARGS['database'],
        env_file=DEFAULT_DOTENV_KWARGS['env_file'],
        key_path=DEFAULT_DOTENV_KWARGS['key_path'],
        defaults=DEFAULT_DOTENV_KWARGS['defaults']):
        kwargs = locals()
        del kwargs['self']
        super().__init__(**kwargs)