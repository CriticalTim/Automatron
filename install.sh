#!/bin/bash

echo "Installing Freelancer AutoApply Dependencies..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed"
    echo "Please install Python 3.8+ from your package manager"
    exit 1
fi

echo "Python found, installing dependencies..."

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
echo "Installation complete!"
echo
echo "To run the application:"
echo "  python3 run.py"
echo

# Make run script executable
chmod +x run.py