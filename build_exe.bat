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
echo Upgrading pip first...
python -m pip install --upgrade pip

echo Installing requirements...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Failed to install dependencies, trying alternative approach...
    echo Installing each dependency individually...
    pip install customtkinter==5.2.2
    pip install requests==2.31.0
    pip install beautifulsoup4==4.12.3
    pip install PyPDF2==3.0.1
    pip install schedule==1.2.1
    pip install selenium==4.15.2
    pip install webdriver-manager==4.0.1
    pip install python-dotenv==1.0.0
    pip install pyinstaller==6.3.0
    pip install pillow==10.1.0
    
    if errorlevel 1 (
        echo.
        echo Failed to install dependencies
        echo Please check your internet connection and try again
        pause
        exit /b 1
    )
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