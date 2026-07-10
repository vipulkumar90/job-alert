from database.connection import get_connection
from database.repository import JobRepository


def test_connection() -> None:
    try:
        with get_connection() as conn:  # noqa: F841
            print("✅ Connected to PostgreSQL!")

    except Exception as e:
        print(f"❌ Connection failed: {e}")

def clean_db() -> None:
    try:
        repo = JobRepository()
        repo.delete_all()
        print("Deleting all rows")

    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    # test_connection()
    clean_db()
