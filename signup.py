from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary in-memory "database"
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))