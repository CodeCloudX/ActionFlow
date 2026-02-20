import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.engine.url import make_url

from app import create_app, db
from config import Config

def create_database_if_not_exists():
    """Connects to PostgreSQL to ensure the target database exists."""
    db_url = Config.SQLALCHEMY_DATABASE_URI
    if not db_url:
        print("FATAL: SQLALCHEMY_DATABASE_URI is not set.", file=sys.stderr)
        sys.exit(1)

    url = make_url(db_url)
    db_name = url.database

    try:
        # Connect to the default 'postgres' database to check for the app DB
        conn = psycopg2.connect(
            host=url.host, port=url.port, user=url.username,
            password=url.password, dbname='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if not cursor.fetchone():
                print(f"Database '{db_name}' not found. Creating...")
                cursor.execute(f'CREATE DATABASE "{db_name}"')
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"FATAL: Could not connect to PostgreSQL server.", file=sys.stderr)
        print("Please ensure it is running and connection details are correct.", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    # Step 1: Ensure the database exists before starting the app.
    create_database_if_not_exists()

    # Step 2: Initialize the Flask app using the factory pattern.
    app = create_app()

    # Step 3: Create all database tables.
    with app.app_context():
        print("Ensuring all database tables exist...")
        db.create_all() # This command is safe and will not re-create existing tables.
        print("Tables verified.")

    # Step 4: Run the application server with the reloader.
    app.run(port=8000, debug=False, use_reloader=True)
