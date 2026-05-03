from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Needed for session management

@app.route('/')
def home():
    return "Welcome to the Login Page!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '1234':
            return "Login successful!"
        else:
            return "Invalid credentials"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)