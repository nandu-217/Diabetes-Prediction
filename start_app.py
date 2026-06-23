"""
Quick Start Script for Diabetes Prediction System
Run this to install dependencies and start the application
"""

import subprocess
import sys
import os

def print_header(text):
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")

def install_dependencies():
    print_header("INSTALLING DEPENDENCIES")
    try:
        print("Installing Python packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def train_model():
    print_header("TRAINING ML MODEL")
    try:
        print("Training diabetes prediction model...")
        subprocess.check_call([sys.executable, "train_model.py"])
        print("✓ Model trained successfully!")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to train model")
        return False

def start_server():
    print_header("STARTING APPLICATION")
    print("Starting Flask backend server...")
    print("\nAccess the application at: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        os.chdir('backend')
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    print_header("DIABETES PREDICTION SYSTEM - SETUP WIZARD")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\nPlease check your internet connection and try again.")
        return
    
    # Step 2: Train model
    choice = input("\nDo you want to train the ML model now? (y/n): ").lower()
    if choice == 'y':
        if not train_model():
            print("\nYou can train the model later by running: python train_model.py")
    
    # Step 3: Start server
    print("\n")
    start_server()

if __name__ == "__main__":
    main()
