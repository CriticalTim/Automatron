#!/usr/bin/env python3
"""
Freelancer AutoApply - Main Entry Point
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from main import FreelancerApp
    
    if __name__ == "__main__":
        print("Starting Freelancer AutoApply...")
        print("Loading application...")
        
        app = FreelancerApp()
        app.run()
        
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required dependencies:")
    print("pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)