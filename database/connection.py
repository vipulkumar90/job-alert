import sqlite3
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

from config import (DATABASE_PROVIDER, POSTGRES_DATABASE, POSTGRES_HOST,
                    POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_SSLMODE,
                    POSTGRES_USER, SQLITE_DATABASE_PATH)
from utils.logger import logger

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_PATH = BASE_DIR / SQLITE_DATABASE_PATH

PARAM = "?" if DATABASE_PROVIDER == "sqlite" else "%s"


def database_exists() -> bool:
    """
    Check whether the configured database exists.

    For PostgreSQL, assume the database already exists.
    """
    if DATABASE_PROVIDER == "sqlite":
        exists = SQLITE_PATH.exists()

        if exists:
            logger.debug("SQLite database found at '%s'.", SQLITE_PATH)
        else:
            logger.debug("SQLite database does not exist.")

        return exists

    logger.debug("Using PostgreSQL. Skipping local database existence check.")
    return True


def get_connection():
    """
    Return a database connection based on the configured provider.
    """
    try:
        if DATABASE_PROVIDER == "sqlite":
            SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)

            connection = sqlite3.connect(SQLITE_PATH)
            connection.row_factory = sqlite3.Row

            logger.debug("Connected to SQLite database.")

            return connection

        elif DATABASE_PROVIDER == "postgres":
            connection = psycopg.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                dbname=POSTGRES_DATABASE,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                sslmode=POSTGRES_SSLMODE,
                row_factory=dict_row,
            )

            logger.debug("Connected to PostgreSQL database.")

            return connection

        else:
            raise ValueError(f"Unsupported DATABASE_PROVIDER: '{DATABASE_PROVIDER}'")

    except Exception:
        logger.exception("Failed to establish database connection.")
        raise


def placeholder(count: int) -> str:
    return ",".join([PARAM] * count)
