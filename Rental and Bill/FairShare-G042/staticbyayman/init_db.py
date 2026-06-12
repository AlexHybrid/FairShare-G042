import os
import sqlite3

# This script creates our SQLite database and the users table.
# Run this file ONCE before starting the Flask app:
#   python init_db.py

# Resolve the database path relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

def create_db():
    # Connect to the database (it will be created if it doesn't exist)
    connection = sqlite3.connect(DB_PATH)

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()

    # Create a table named 'users' if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Save the changes and close the connection
    connection.commit()
    connection.close()
    print(f"Database created at: {DB_PATH}")
    print("Table 'users' ready.")

if __name__ == '__main__':
    create_db()
