#!/bin/bash

echo "Building Automatron Executable..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "Installing/updating PyInstaller and dependencies..."

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found, installing..."
    python3 -m ensurepip --default-pip
fi

# Install dependencies
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo
    echo "Failed to install dependencies"
    echo "Please check your internet connection and try again"
    exit 1
fi

echo
echo "Building executable (this may take several minutes)..."
echo

# Clean previous builds
rm -rf build dist
rm -f Automatron

# Build with PyInstaller
python3 -m PyInstaller --clean Automatron.spec

if [ $? -ne 0 ]; then
    echo
    echo "Build failed! Check the output above for errors."
    exit 1
fi

# Move executable to main directory
if [ -f "dist/Automatron" ]; then
    mv dist/Automatron .
    echo
    echo "SUCCESS! Automatron executable has been created."
    echo
    echo "You can now run the application with: ./Automatron"
    echo
    
    # Make executable
    chmod +x Automatron
    
    # Clean up build files
    rm -rf build dist
    rm -f Automatron.spec.orig
    
else
    echo
    echo "Build completed but executable not found in expected location."
    echo "Check the dist folder for the executable."
fi

echo