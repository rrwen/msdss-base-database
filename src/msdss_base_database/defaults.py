DEFAULT_DOTENV_KWARGS = dict(
    driver='MSDSS_DATABASE_DRIVER',
    user='MSDSS_DATABASE_USER',
    password='MSDSS_DATABASE_PASSWORD',
    host='MSDSS_DATABASE_HOST',
    port='MSDSS_DATABASE_PORT',
    database='MSDSS_DATABASE_NAME',
    env_file='./.env',
    key_path=None,
    defaults=dict(
        driver='postgresql',
        user='msdss',
        password='msdss123',
        host='localhost',
        port='5432',
        database='msdss'
    )
)
DEFAULT_SUPPORTED_OPERATORS = ['=', '!=', '>', '>=', '>', '<', '<=', 'LIKE', 'NOTLIKE', 'ILIKE', 'NOTILIKE', 'CONTAINS', 'STARTSWITH', 'ENDSWITH']