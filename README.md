# 🏠 FairShare Expense Tracker

A simple and beautiful web application to track and share household/room expenses among tenants. Built with a Flask backend (SQLite database) and a responsive frontend dashboard.

---

## 🚀 How to Run the Application

### Method 1: The Quick Start Script (Windows Only)
1. Make sure you have **Python 3.10+** installed on your system.
2. Double-click the **`start.bat`** file in the root folder.
3. This script will automatically:
   - Create a Python virtual environment (`venv`).
   - Install all required dependencies (Flask, CORS, openpyxl, reportlab).
   - Start the backend server on `http://127.0.0.1:5000`.
   - Open your default web browser to the dashboard.

---

### Method 2: Manual Installation (Windows, Mac, or Linux)

#### 1. Setup Virtual Environment
Open your terminal inside the project directory and run:
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows (Command Prompt):
call venv\Scripts\activate
# On Windows (PowerShell):
.\venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r backup_backendddd/requirements.txt
```

#### 3. Run the Backend Server
```bash
python backup_backendddd/app.py
```

#### 4. Open the Web App
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure
- `backup_backendddd/`: Flask app, SQLite database logic, and export utilities.
- `frontend/`: Dashboard, stylesheets, assets, and page scripts.
- `start.bat`: One-click runner for Windows.
- `README.md`: Setup instructions.
