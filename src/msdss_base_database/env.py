from msdss_base_dotenv import DotEnv

from .defaults import *

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
        env = DatabaseDotEnv(env_file='./.env', key_path='./.env.key')

        # Save default database env
        env.save()

        # Load default database env
        env.load()

        # See defaults
        print('default_env:\\n')
        for k, name in env.mappings.items():
            value = str(env.get(k))
            print(f'{name}: {value}')

        # Remove all env files
        env.clear()

        # Create database env with diff host, port, and database var names
        # Also set diff defaults
        new_env = DatabaseDotEnv(
            host='MSDSS_DATABASE_HOST_B',
            port='MSDSS_DATABASE_PORT_B',
            database='MSDSS_DATABASE_DATABASE_B',
            defaults = dict(
                host='localhost',
                database='msdss2'
            )
        )

        # Set MSDSS_DATABASE_PORT_B
        new_env.set('port', '5432')

        # Set MSDSS_DATABASE_HOST_B, but delete it afterwards
        new_env.set('host', 'invalid-host')
        new_env.delete('host')

        # Check if MSDSS_DATABASE_HOST_B is set
        host_is_set = new_env.is_set('host')

        # See new env
        print('\\nnew_env:\\n')
        for k, name in new_env.mappings.items():
            value = str(new_env.get(k))
            print(f'{name}: {value}')
        print('host_is_set: ' + str(host_is_set))

        # Save new env in a file
        new_env.save()

        # Load the new env
        new_env.load()

        # Remove the new env files
        new_env.clear()
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
        del kwargs['__class__']
        super().__init__(**kwargs)