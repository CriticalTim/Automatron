@echo off
echo Building Automatron Executable...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Installing/updating PyInstaller and dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Building executable (this may take several minutes)...
echo.

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Automatron.exe del Automatron.exe

REM Build with PyInstaller
pyinstaller --clean Automatron.spec

if errorlevel 1 (
    echo.
    echo Build failed! Check the output above for errors.
    pause
    exit /b 1
)

REM Move executable to main directory
if exist dist\Automatron.exe (
    move dist\Automatron.exe .
    echo.
    echo SUCCESS! Automatron.exe has been created.
    echo.
    echo You can now run the application by double-clicking Automatron.exe
    echo.
    
    REM Clean up build files
    rmdir /s /q build
    rmdir /s /q dist
    if exist Automatron.spec.orig del Automatron.spec.orig
    
) else (
    echo.
    echo Build completed but executable not found in expected location.
    echo Check the dist folder for the executable.
)

echo.
pause