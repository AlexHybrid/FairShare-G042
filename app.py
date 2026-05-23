from flask import Flask, render_template, request, redirect, url_for, session, flash 
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask application
app = Flask(__name__)
# A secret key is required to use Flask sessions securely
app.secret_key = 'your_very_secret_key_here'

# Helper function to get a database connection
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name like a dictionary
    return conn