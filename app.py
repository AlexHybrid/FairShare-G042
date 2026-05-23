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

# Route for the main page (Login and Signup forms)
@app.route('/')
def index():
    # If the user is already logged in, send them straight to the dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

# Route to handle the signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    # Get the data submitted from the HTML form
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    # Basic validation: check if passwords match
    if password != confirm_password:
        flash('Passwords do not match!', 'error')
        return redirect(url_for('index'))
        