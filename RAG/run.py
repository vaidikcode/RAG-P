#!/usr/bin/env python3

import sys
import subprocess

def install_requirements():
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing packages: {e}")
        return False

def run_application():
    print("Starting RAG application...")
    try:
        from app import main
        main()
    except ImportError as e:
        print(f"Import error: {e}")
        print("Make sure all dependencies are installed.")
        return False
    except Exception as e:
        print(f"Application error: {e}")
        return False

def main():
    print("RAG Application Setup")
    print("=" * 30)
    
    choice = input("Do you want to install dependencies? (y/n): ").lower()
    if choice == 'y':
        if not install_requirements():
            return
    
    print("\nStarting application...")
    run_application()

if __name__ == "__main__":
    main()
