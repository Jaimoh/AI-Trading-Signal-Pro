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
def username_exists(username):

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(
        "SELECT 1 FROM users WHERE username = ?",
        (username,)
        )

        result = cursor.fetchone()

        connection.close()

        return result is not None
def username_exists_except(username, user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE username = ? AND id != ?",
        (username, user_id)
    )
    result = cursor.fetchone()

    connection.close()
    return result is not None

def email_exists(email):
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,)
        )
        result = cursor.fetchone()

        connection.close()

def email_exists_except(email, user_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE email = ? AND id != ?",
        (email, user_id)
    )
    result = cursor.fetchone()

    connection.close()
    return result is not None

def create_user(
        first_name,
        last_name,
        username,
        email,
        password_hash
        ):

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO users(
                first_name,
                last_name,
                username,
                email,
                password_hash
            )
            VALUES(?,?,?,?,?) 
                   """,
                   (
                       first_name,
                       last_name,
                       username,
                       email,
                       password_hash,
                   )

        ) 
        connection.commit()
        connection.close()
        return True
def get_user(username):

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    return dict(user)  # Convert Row object to dictionary
def update_user(
    user_id,
    first_name,
    last_name,
    username,
    email
    ): 

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET
            first_name = ?,
            last_name = ?,
            username = ?,
            email = ?
        WHERE id = ?
        """,
        (
            first_name,
            last_name,
            username,
            email,
            user_id
        )
    )

    connection.commit()
    connection.close()

    return True
def get_user_by_id(user_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    return dict(user)  # Convert Row object to dictionary
    
#def get_user(username):

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()

    connection.close()

    return user