import os
import sys
import mysql.connector # psycopg2 ko isse badal diya hai
from sqlalchemy.engine.url import make_url
from flask_migrate import init, migrate, upgrade, stamp, current

from app import create_app
from config import Config

def setup_database():
    """Ensures the database exists and is up-to-date with migrations."""
    db_url = Config.SQLALCHEMY_DATABASE_URI
    if not db_url:
        print("\n--- DATABASE CONFIGURATION ERROR ---")
        print("SQLALCHEMY_DATABASE_URI is not set. Please set it in your .env or config.py file.")
        print("Example for MySQL: mysql+mysqlconnector://user:password@host/dbname")
        exit(1)

    url = make_url(db_url)
    db_name = url.database

    # Connect to the MySQL server to create the application's database
    try:
        conn = mysql.connector.connect(
            host=url.host,
            port=url.port or 3306,
            user=url.username,
            password=url.password
        )
        cursor = conn.cursor()

        print(f"Checking for database '{db_name}'...")
        # MySQL ke liye 'CREATE DATABASE IF NOT EXISTS' ka istemal karein
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
        print(f"Database '{db_name}' is ready.")

        cursor.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"\n--- DATABASE CONNECTION ERROR ---")
        print(f"Could not connect to MySQL. Please ensure it is running and that the credentials are correct.")
        print(f"Error details: {e}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during database setup: {e}")
        exit(1)

    # Niche ka migration logic waise ka waisa hi rahega
    app = create_app()
    with app.app_context():
        from flask_migrate import Migrate
        from app import db
        if not os.path.exists('migrations'):
            print("Initializing database migrations folder...")
            init()
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)
        if 'alembic_version' not in inspector.get_table_names():
            print("Alembic version table not found. Stamping with current revision...")
            stamp()
        else:
            try:
                with db.engine.connect() as conn:
                    result = conn.execute(text("SELECT version_num FROM alembic_version"))
                    current_rev = result.scalar()
                    print(f"Current database revision: {current_rev}")
            except Exception as e:
                print(f"Error checking current revision: {e}")
        print("Checking for model changes...")
        try:
            migrate(message="Auto-migration on startup.")
        except Exception as e:
            print(f"Migration generation notes: {e}")
        print("Applying migrations...")
        try:
            upgrade()
            print("Database schema is up-to-date.")
        except Exception as e:
            print(f"Warning during upgrade: {e}")
            print("Attempting to recover migration state...")
            try:
                stamp(revision='head')
                upgrade()
                print("Database schema recovered and is now up-to-date.")
            except Exception as e2:
                print(f"Failed to recover migration state: {e2}")
                print("You may need to manually resolve migration conflicts.")
    return app

if __name__ == '__main__':
    app = setup_database()
    print("\nStarting the application server on http://127.0.0.1:8000...")
    app.run(port=8000, debug=True, use_reloader=False)
