"""Check the database connection using the local, ignored .env file."""

from app import get_db


def main() -> int:
    try:
        conn = get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT count(*) FROM yokai_compendium")
                total = cursor.fetchone()[0]
        finally:
            conn.close()
    except Exception as error:
        # Connection errors can contain server addresses or credentials.
        print(f"Database connection failed ({type(error).__name__}).")
        return 1

    print(f"Database connection succeeded. Yokai records: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
