import sqlite3
import os

# Database location
DB_FOLDER = "database"
DB_NAME = "trading.db"
DB_PATH = os.path.join(DB_FOLDER, DB_NAME)


def initialize_database():
    """Create the database and users table if they do not exist."""

    # Create the database folder if needed
    os.makedirs(DB_FOLDER, exist_ok=True)

    # Connect to SQLite
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("✅ Database initialized successfully.")