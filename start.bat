@echo off
setlocal enabledelayedexpansion

echo ===================================================
echo             Starting FairShare System              
echo ===================================================

:: Check for Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to your system PATH.
    echo Please install Python (version 3.10 or higher recommended) from https://www.python.org/
    pause
    exit /b 1
)

:: Navigate to the folder containing this batch script
cd /d "%~dp0"

:: Create virtual environment if it does not exist
if not exist "venv" (
    echo [INFO] Creating Python virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment and install dependencies
echo [INFO] Activating virtual environment...
call venv\Scripts\activate

echo [INFO] Installing required dependencies...
pip install -r backup_backendddd\requirements.txt
if !errorlevel! neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

:: Open the browser pointing to localhost:5000
echo [INFO] Launching default web browser...
start http://127.0.0.1:5000

:: Start the Flask app
echo [INFO] Starting Flask backend server...
python backup_backendddd\app.py

pause
