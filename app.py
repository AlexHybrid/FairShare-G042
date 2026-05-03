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

        # Simple hardcoded check
        if username == 'admin' and password == '1234':
            session['user'] = username  # store user in session
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
        
    return render_template('login.html')

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Hello, {session['user']}! Welcome to your dashboard."
    else:
        return redirect(url_for('login'))
    
# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)