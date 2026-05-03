from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory "database"
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        # Check if user exists and password matches
        if username in users and users[username]['password'] == password:
            return f"Welcome, {username}!"
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

         # Validation
        if username in users:
            error = "Username already exists"
            return render_template('register.html', error=error)
        if password != confirm_password:
            error = "Passwords do not match"
            return render_template('register.html', error=error)