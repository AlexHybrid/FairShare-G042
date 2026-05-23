import sqlite3

# This script creates our SQLite database and the users table.
# Run this file once before starting the Flask app.

def create_db():
    # Connect to the database (it will be created if it doesn't exist)
    connection = sqlite3.connect('users.db')