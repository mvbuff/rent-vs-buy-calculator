#!/usr/bin/env python3
"""
Home Ownership vs Rent Calculator Launcher
Choose between web and desktop versions
"""

import sys
import subprocess
import os

def check_streamlit_installed():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_streamlit():
    """Install Streamlit and dependencies"""
    print("Installing Streamlit and dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_web_version():
    """Run the Streamlit web version"""
    if not check_streamlit_installed():
        print("📦 Streamlit not found. Installing dependencies...")
        if not install_streamlit():
            return False
    
    print("🌐 Starting web version...")
    print("🚀 Your calculator will open in your browser!")
    print("📍 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 Web server stopped")
    except FileNotFoundError:
        print("❌ streamlit_app.py not found")
        return False
    return True

def run_desktop_version():
    """Run the Tkinter desktop version"""
    print("🖥️  Starting desktop version...")
    try:
        subprocess.run([sys.executable, "home_calculator.py"])
    except FileNotFoundError:
        print("❌ home_calculator.py not found")
        return False
    return True

def main():
    print("🏠 Home Ownership vs Rent Calculator")
    print("=" * 50)
    print()
    print("Choose your preferred version:")
    print("1. 🌐 Web Version (Recommended) - Modern interface, runs in browser")
    print("2. 🖥️  Desktop Version - Traditional GUI, no internet required")
    print("3. ℹ️  Help & Info")
    print("4. 🚪 Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                if run_web_version():
                    break
            elif choice == "2":
                if run_desktop_version():
                    break
            elif choice == "3":
                print("\n📚 Help & Information:")
                print("- Web Version: Modern interface with better visualizations")
                print("- Desktop Version: Works offline, traditional GUI")
                print("- Both versions have identical calculation logic")
                print("- Web version requires internet for initial setup only")
                print()
            elif choice == "4":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
        except EOFError:
            print("\n👋 Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main() 