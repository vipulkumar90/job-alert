from database.connection import get_connection


def test_connection() -> None:
    try:
        with get_connection() as conn:
            print("✅ Connected to PostgreSQL!")

    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    test_connection()
