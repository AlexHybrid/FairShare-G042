import os
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests
# A secret key is required to use Flask sessions securely
app.secret_key = 'your_very_secret_key_here'

# Resolve paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'users.db')

FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, '../Rental and Bill/frontend'))
RENTAL_DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '../Rental and Bill/backend/rental_blossoms.db'))
UPLOAD_DIR = os.path.abspath(os.path.join(BASE_DIR, '../Rental and Bill/backend/uploads'))
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to get a database connection for users
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name like a dictionary
    return conn

# Helper function to get a database connection for rental expenses
def get_rental_db_connection():
    conn = sqlite3.connect(RENTAL_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the rental database schema
def init_rental_db():
    conn = get_rental_db_connection()
    cursor = conn.cursor()
    
    # Create expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            room TEXT NOT NULL,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            payment_method TEXT,
            category TEXT,
            notes TEXT,
            receipt_path TEXT,
            is_recurring INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    
    # Migration: Add columns if they don't exist
    columns = [row[1] for row in cursor.execute('PRAGMA table_info(expenses)').fetchall()]
    if 'payment_method' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN payment_method TEXT')
    if 'category' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN category TEXT')
    if 'notes' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN notes TEXT')
    if 'receipt_path' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN receipt_path TEXT')
    if 'is_recurring' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN is_recurring INTEGER DEFAULT 0')
    if 'status' not in columns:
        cursor.execute('ALTER TABLE expenses ADD COLUMN status TEXT DEFAULT "Pending"')
    
    # Check if table is empty, if so, populate with initial data
    cursor.execute('SELECT COUNT(*) FROM expenses')
    count = cursor.fetchone()[0]
    
    if count == 0:
        initial_data = [
            ('01/06/26', 'Room A', 'Electricity Bill', 1200.0, 'Cash', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room B', 'Water Bill', 800.0, 'Cash', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room C', 'Internet', 300.0, 'Bank Transfer', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room D', 'Gas Bill', 500.0, 'Cash', 'Utilities', '', '', 0, 'Paid'),
            ('01/06/26', 'Room E', 'Cleaning', 200.0, 'Cash', 'Maintenance', '', '', 0, 'Paid')
        ]
        cursor.executemany('''
            INSERT INTO expenses (date, room, type, amount, payment_method, category, notes, receipt_path, is_recurring, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', initial_data)
        
    conn.commit()
    conn.close()

# Initialize database on startup
init_rental_db()


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

    # Hash the password for security (never store raw passwords!)
    hashed_password = generate_password_hash(password)

    # Open the database connection
    conn = get_db_connection()
    try:
        # Insert the new user into the database
        conn.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, hashed_password)
        )
        conn.commit()
        flash('Account created successfully! Please log in.', 'success')
    except sqlite3.IntegrityError:
        # This error happens if the email is already in the database (UNIQUE constraint)
        flash('An account with this email already exists.', 'error')
    finally:
        # Always close the database connection when done
        conn.close()

    return redirect(url_for('index'))

# Route to handle the login form submission
@app.route('/login', methods=['POST'])
def login():
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
        flash('Invalid email or password. Please try again.', 'error')
        return redirect(url_for('index'))

# Route for the dashboard page (only accessible if logged in)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('index'))
    return send_from_directory(FRONTEND_DIR, 'index.html')

# Route to log out
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

# Expense API routes
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    conn = get_rental_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses')
    rows = cursor.fetchall()
    conn.close()

    expenses = []
    for row in rows:
        expenses.append({
            'id':             row['id'],
            'date':           row['date'],
            'room':           row['room'],
            'type':           row['type'],
            'amount':         row['amount'],
            'payment_method': row['payment_method'] or 'Cash',
            'category':       row['category']       or 'Utilities',
            'notes':          row['notes']           or '',
            'receipt_path':   row['receipt_path']    or '',
            'is_recurring':   bool(row['is_recurring']),
            'status':         row['status']          or 'Pending',
        })
    return jsonify(expenses)

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    date           = data.get('date')
    room           = data.get('room')
    type_          = data.get('type')
    amount         = data.get('amount')
    payment_method = data.get('payment_method', 'Cash')
    category       = data.get('category', 'Utilities')
    notes          = data.get('notes', '')
    receipt_path   = data.get('receipt_path', '')
    is_recurring   = 1 if data.get('is_recurring') else 0
    status         = data.get('status', 'Pending')

    if not all([date, room, type_, amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_rental_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses
            (date, room, type, amount, payment_method, category, notes, receipt_path, is_recurring, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (date, room, type_, float(amount), payment_method, category, notes, receipt_path, is_recurring, status))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success'}), 201

@app.route('/api/expenses/upload', methods=['POST'])
def upload_receipt():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    if 'receipt' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['receipt']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_DIR, filename)
        file.save(filepath)
        return jsonify({'receipt_path': filename}), 200
    return jsonify({'error': 'File type not allowed'}), 400

# Catch-all route to serve static files from frontend and upload folders
@app.route('/<path:path>')
def static_files(path):
    # If the file exists in frontend directory, serve it
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    # If the file exists in the upload directory, serve it
    elif os.path.exists(os.path.join(UPLOAD_DIR, path)):
        return send_from_directory(UPLOAD_DIR, path)
    else:
        return jsonify({'error': 'File not found'}), 404

# Start the application
if __name__ == '__main__':
    # debug=True allows the server to auto-reload when you change the code
    app.run(debug=True, port=5000)

