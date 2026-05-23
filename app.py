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
    
     # Hash the password for security (we should never store raw passwords!)
    hashed_password = generate_password_hash(password)
    
    # Open the database connection
    conn = get_db_connection()
    try:
        # Insert the new user into the database
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                     (name, email, hashed_password))
        conn.commit()
        # Let the user know the account was created
        flash('Account created successfully! Please log in.', 'success')
    except sqlite3.IntegrityError:
        # This error happens if the email is already in the database (since email is UNIQUE)
        flash('An account with this email already exists.', 'error')
    finally:
        # Always close the database connection when done
        conn.close()
        
    # Go back to the main page
    return redirect(url_for('index'))

# Route to handle the login form submission
@app.route('/login', methods=['POST'])
def login():
    # Get the data from the HTML form
    email = request.form['email']
    password = request.form['password']
    
    # Find the user by their email in the database
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    
    # Check if user exists and if the password matches the hash in the database
    if user and check_password_hash(user['password'], password):
        # Successful login: store user details in the session
        session['user_id'] = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('dashboard'))
    else:
        # Failed login
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('index'))
    
# Route for the dashboard page (only accessible if logged in)
@app.route('/dashboard')
def dashboard():
    # Check if the user is actually logged in
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('index'))
        
    # Render the dashboard template, passing the user's name
    return render_template('dashboard.html', name=session['user_name'])
