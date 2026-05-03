from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

# Home route
@app.route('/')
def home():
    return "Welcome to the Login Page! <a href='/login'>Go to Login</a>"

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

if __name__ == '__main__':
    app.run(debug=True)