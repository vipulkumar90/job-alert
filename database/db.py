"""
Database connection and initialization.

This module is responsible only for:
    - Creating a connection to the SQLite database.
    - Creating the required tables if they do not already exist.
"""

import sqlite3
from pathlib import Path

from utils.logger import logger

# Path to the SQLite database file.
DATABASE_PATH = Path(__file__).parent / "jobs.db"


def get_connection() -> sqlite3.Connection:
    """
    Create and return a connection to the SQLite database.

    Returns:
        sqlite3.Connection: SQLite connection object.
    """
    return sqlite3.connect(DATABASE_PATH)


def initialize_database() -> None:
    """
    Create the required database tables if they do not already exist.
    """

    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    url TEXT NOT NULL,
                    description TEXT,
                    posted_date TEXT,
                    source TEXT NOT NULL,
                    hash TEXT NOT NULL UNIQUE
                )
            """)

            conn.commit()

    except sqlite3.Error:
        logger.exception("Failed to initialize database")
        raise
