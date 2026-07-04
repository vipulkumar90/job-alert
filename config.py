import os

from dotenv import load_dotenv

load_dotenv()

# Discord
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")

# Database Provider
DATABASE_PROVIDER = (
    os.getenv(
        "DATABASE_PROVIDER",
        "sqlite",
    )
    .strip()
    .lower()
)

# SQLite
SQLITE_DATABASE_PATH = os.getenv(
    "SQLITE_DATABASE_PATH",
    "database/jobs.db",
)

# PostgreSQL
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_SSLMODE = os.getenv(
    "POSTGRES_SSLMODE",
    "require",
)
