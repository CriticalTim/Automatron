@echo off
echo Installing Freelancer AutoApply Dependencies...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found, installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo To run the application:
echo   python run.py
echo.
pause