import sqlite3

# This script creates our SQLite database and the users table.
# Run this file once before starting the Flask app.

def create_db():
    # Connect to the database (it will be created if it doesn't exist)
    connection = sqlite3.connect('users.db')

    # Create a cursor object to execute SQL commands
    cursor = connection.cursor()
    
    # Create a table named 'users' if it doesn't already exist
    # It has an id (primary key), name, email (must be unique), and password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')