#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
from pathlib import Path

def check_python():
    """Check Python version and install required packages"""
    print("Checking Python installation...")
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required!")
        sys.exit(1)
    
    # Install required packages
    requirements = [
        'python-dotenv',
        'aiohttp',
        'discord.py',
        'PyNaCl'  # For voice support
    ]
    
    for package in requirements:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', package], check=True)
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"Error installing {package}")
            sys.exit(1)

def check_php():
    """Check PHP installation and install if needed"""
    print("\nChecking PHP installation...")
    
    system = platform.system().lower()
    if system == "linux":
        try:
            # Check if PHP is installed
            subprocess.run(['php', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✓ PHP is already installed")
        except FileNotFoundError:
            print("Installing PHP...")
            try:
                subprocess.run(['sudo', 'apt', 'update'], check=True)
                subprocess.run(['sudo', 'apt', 'install', '-y', 'php', 'php-cli'], check=True)
                print("✓ PHP installed successfully")
            except subprocess.CalledProcessError:
                print("Error installing PHP. Please install manually:")
                print("sudo apt update && sudo apt install php php-cli")
                sys.exit(1)
    elif system == "windows":
        try:
            subprocess.run(['php', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✓ PHP is already installed")
        except FileNotFoundError:
            print("PHP not found! Please install PHP for Windows:")
            print("1. Download PHP from: https://windows.php.net/download/")
            print("2. Extract to C:\\php")
            print("3. Add C:\\php to your PATH environment variable")
            print("4. Rename php.ini-development to php.ini")
            input("Press Enter when you have completed these steps...")

def setup_directories():
    """Create necessary directories and copy files"""
    print("\nSetting up directory structure...")
    
    base_dir = Path(__file__).parent
    required_dirs = ['bots', 'logs', 'cmdtamplates']
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def main():
    """Main installation function"""
    print("=== Discord Bot Manager Installation ===")
    
    check_python()
    check_php()
    setup_directories()
    
    print("\n=== Installation Complete ===")
    print("You can now start the server by running:")
    print("python bot_manager.py")

if __name__ == "__main__":
    main()
