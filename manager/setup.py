#!/usr/bin/env python3
import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)

def install_system_dependencies():
    """Install system-level dependencies based on OS"""
    system = platform.system().lower()
    
    if system == "linux":
        try:
            # Install PHP and other dependencies on Ubuntu/Debian
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run([
                "sudo", "apt", "install", "-y",
                "php", "php-cli", "php-fpm", "php-json", "php-common",
                "php-mysql", "php-zip", "php-gd", "php-mbstring",
                "php-curl", "php-xml", "php-pear", "php-bcmath"
            ], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error installing system dependencies: {e}")
            print("Please install PHP manually according to your distribution")
    
    elif system == "windows":
        print("For Windows users:")
        print("1. Please install PHP from: https://windows.php.net/download/")
        print("2. Add PHP to your system PATH")
        input("Press Enter when you have completed these steps...")

def install_python_dependencies():
    """Install required Python packages"""
    requirements = [
        "discord.py>=2.3.2",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.8.5",
        "PyNaCl>=1.5.0",
        "colorama>=0.4.6",  # For colored console output
        "watchdog>=3.0.0",  # For file monitoring
        "psutil>=5.9.0",    # For process management
    ]
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], check=True)
        
        for req in requirements:
            print(f"Installing {req}")
            subprocess.run([
                sys.executable, "-m", "pip", "install", req
            ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing Python dependencies: {e}")
        sys.exit(1)

def setup_directory_structure():
    """Create necessary directories if they don't exist"""
    directories = [
        "bots",
        "cmdtamplates",
        "cmdtamplates/api",
        "cmdtamplates/frontend",
        "logs",
        "data"
    ]
    
    base_path = Path(__file__).parent
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        with open(env_path, 'w') as f:
            f.write("""# Discord Bot Manager Environment Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO
DEFAULT_PREFIX=!
ENABLE_HTTPS=False
""")
        print("Created .env configuration file")

def main():
    """Main setup function"""
    print("=== Discord Bot Manager Setup ===")
    
    # Check Python version
    check_python_version()
    print("✓ Python version check passed")
    
    # Install system dependencies
    print("\nInstalling system dependencies...")
    install_system_dependencies()
    print("✓ System dependencies installed")
    
    # Install Python packages
    print("\nInstalling Python dependencies...")
    install_python_dependencies()
    print("✓ Python dependencies installed")
    
    # Setup directory structure
    print("\nSetting up directory structure...")
    setup_directory_structure()
    print("✓ Directory structure created")
    
    # Create environment file
    print("\nCreating configuration files...")
    create_env_file()
    print("✓ Configuration files created")
    
    print("\n=== Setup Complete ===")
    print("You can now run the Discord Bot Manager using:")
    print("python bot_manager.py")

if __name__ == "__main__":
    main()
