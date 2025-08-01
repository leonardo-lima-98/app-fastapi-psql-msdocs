
class Settings():
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    GLANCES_URL: str

    TENANT_ID: str
    CLIENT_ID: str
    CLIENT_SECRET: str
    AUTHORITY: str
    JWKS_URL: str
    SCOPE: list[str]

import logging
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

ENV = os.getenv("ENV")
def get_sql_url():
    if ENV == 'PRD':
        logger.info("Connecting to Azure PostgreSQL Flexible server based on AZURE_POSTGRESQL_CONNECTIONSTRING...")
        env_connection_string = os.getenv("AZURE_POSTGRESQL_CONNECTIONSTRING")
        if env_connection_string is None:
            logger.info("Missing environment variable AZURE_POSTGRESQL_CONNECTIONSTRING")
        else:
            # Parse the connection string
            details = dict(item.split('=') for item in env_connection_string.split())

            # Properly format the URL for SQLAlchemy
            sql_url = (
                f"postgresql://{quote_plus(details['user'])}:{quote_plus(details['password'])}"
                f"@{details['host']}:{details['port']}/{details['dbname']}?sslmode={details['sslmode']}"
            )
            return sql_url

    else:
        logger.info("Connecting to local PostgreSQL server based on .env file...")
        load_dotenv()
        POSTGRES_USERNAME = os.environ.get("DBUSER")
        POSTGRES_PASSWORD = os.environ.get("DBPASS")
        POSTGRES_HOST = os.environ.get("DBHOST")
        POSTGRES_DATABASE = os.environ.get("DBNAME")
        POSTGRES_PORT = os.environ.get("DBPORT", 5432)

        sql_url = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        return sql_url


VALID_TOKEN = 'meu-token-secreto-123'