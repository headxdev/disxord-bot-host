#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Manager - Complete Unified System v2.0
Professional startup, management, and deployment system.
All functions integrated in one script.

@author headx & the psychon  
@version 2.0
"""

import os
import sys
import time
import json
import venv
import shutil
import logging
import platform
import subprocess
import webbrowser
import threading
import socket
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List

# ANSI Color Codes
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

    @staticmethod
    def colorize(text: str, color: str) -> str:
        if platform.system() == 'Windows':
            try:
                os.system('color')
            except:
                return text
        return f"{color}{text}{Colors.RESET}"


def print_banner():
    banner = f"""
{Colors.PURPLE}╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║            🤖 DISCORD BOT MANAGER v2.0 - PROFESSIONAL EDITION        ║
║                                                                      ║
║                    Created by headx & the psychon                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)


def print_step(step: int, title: str, description: str = ""):
    print(f"\n{Colors.BOLD}[{step}/7] {Colors.CYAN}{title}{Colors.RESET}")
    if description:
        print(f"    {Colors.WHITE}{description}{Colors.RESET}")


def print_success(message: str):
    print(f"    {Colors.GREEN}✓{Colors.RESET} {message}")


def print_warning(message: str):
    print(f"    {Colors.YELLOW}⚠{Colors.RESET} {message}")


def print_error(message: str):
    print(f"    {Colors.RED}✗{Colors.RESET} {message}")


def print_info(message: str):
    print(f"    {Colors.BLUE}ℹ{Colors.RESET} {message}")


class DiscordBotManager:
    """Complete Discord Bot Manager with setup and runtime management."""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.venv_path = self.base_path / 'venv'
        self.logs_path = self.base_path / 'logs'
        self.config_path = self.base_path / 'config.json'
        self.bots_path = self.base_path / 'bots'
        self.data_path = self.base_path / 'data'
        
        self.setup_logging()
        
        self.system_info = {
            'os': platform.system(),
            'python_version': platform.python_version(),
            'architecture': platform.machine(),
            'processor': platform.processor() or 'Unknown'
        }
        
        self.bot_processes: Dict[str, subprocess.Popen] = {}
        self.config = {}
        self.website_process = None
    
    def setup_logging(self):
        self.logs_path.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.logs_path / 'startup.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_python_version(self) -> bool:
        print_step(1, "System Check", "Verifying Python version and system compatibility")
        
        version = sys.version_info
        min_version = (3, 8)
        
        print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
        print_info(f"Operating System: {self.system_info['os']} ({self.system_info['architecture']})")
        
        if version[:2] >= min_version:
            print_success(f"Python {version.major}.{version.minor} is supported")
            return True
        else:
            print_error(f"Python {min_version[0]}.{min_version[1]}+ required, found {version.major}.{version.minor}")
            return False
    
    def create_directories(self):
        print_step(2, "Directory Setup", "Creating required directories")
        
        directories = [
            self.logs_path,
            self.data_path,
            self.bots_path,
            self.base_path / 'config',
            self.base_path / 'backups'
        ]
        
        try:
            for directory in directories:
                if not directory.exists():
                    directory.mkdir(parents=True, exist_ok=True)
                    print_success(f"Created directory: {directory.name}/")
                else:
                    print_info(f"Directory exists: {directory.name}/")
            return True
        except Exception as e:
            print_error(f"Failed to create directories: {e}")
            return False
    
    def setup_virtual_environment(self) -> bool:
        print_step(3, "Virtual Environment", "Setting up isolated Python environment")
        
        if not self.venv_path.exists():
            try:
                print_info("Creating virtual environment...")
                venv.create(self.venv_path, with_pip=True)
                print_success("Virtual environment created successfully")
            except Exception as e:
                print_error(f"Failed to create virtual environment: {e}")
                return False
        else:
            print_info("Virtual environment already exists")
        
        return True
    
    def install_dependencies(self) -> bool:
        print_step(4, "Dependencies", "Installing required Python packages")
        
        if platform.system() == 'Windows':
            pip_exe = self.venv_path / 'Scripts' / 'pip.exe'
        else:
            pip_exe = self.venv_path / 'bin' / 'pip'
        
        requirements_file = self.base_path / 'requirements.txt'
        
        if not requirements_file.exists():
            print_error("requirements.txt not found")
            return False
        
        try:
            print_info("Upgrading pip...")
            subprocess.run([str(pip_exe), 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True, text=True)
            print_success("pip upgraded successfully.")

            print_info("Installing Flask...")
            subprocess.run([str(pip_exe), 'install', '--force-reinstall', 'flask'], 
                         check=True, capture_output=True, text=True)
            print_success("Flask installed successfully.")

            print_info("Installing dependencies from requirements.txt...")
            subprocess.run([str(pip_exe), 'install', '-r', str(requirements_file)], 
                         check=True, capture_output=True, text=True)
            
            print_success("All dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print_error(f"Failed to install dependencies: {e.stderr}")
            return False
        except Exception as e:
            print_error(f"An unexpected error occurred during dependency installation: {e}")
            return False
    
    def create_default_config(self):
        print_step(5, "Configuration", "Setting up default configuration")
        
        try:
            if not self.config_path.exists():
                default_config = {
                    "app": {
                        "name": "Discord Bot Manager",
                        "version": "2.0.0",
                        "host": "0.0.0.0",
                        "port": 8000,
                        "debug": False
                    },
                    "security": {
                        "session_timeout": 3600,
                        "max_login_attempts": 5,
                        "csrf_enabled": True
                    },
                    "bot_defaults": {
                        "prefix": "!",
                        "max_bots": 10,
                        "auto_restart": True
                    },
                    "features": {
                        "discord_oauth": True,
                        "auto_backup": True,
                        "command_logging": True
                    }
                }
                
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2)
                print_success("Default configuration created")
                self.config = default_config
            else:
                print_info("Configuration file already exists")
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            
            env_template = self.base_path / '.env.template'
            if not env_template.exists():
                env_content = """# Discord Bot Manager Environment Variables
# Copy this file to .env and fill in your values

# Server Configuration
HOST=0.0.0.0
PORT=5000
DEBUG=False

# Discord OAuth2
DISCORD_CLIENT_ID=deine_client_id
DISCORD_CLIENT_SECRET=dein_client_secret
DISCORD_REDIRECT_URI=http://localhost:5000/auth/callback

# Security
SECRET_KEY=generiere_mit_secrets.token_urlsafe(32)
ENCRYPTION_KEY=generiere_mit_Fernet.generate_key()
SESSION_TIMEOUT=3600

# Bot Defaults
DEFAULT_PREFIX=!
MAX_BOTS_PER_USER=10

# Features
ENABLE_DISCORD_OAUTH=True
ENABLE_AUTO_BACKUP=True
ENABLE_COMMAND_LOGGING=True
"""
                with open(env_template, 'w', encoding='utf-8') as f:
                    f.write(env_content)
                print_success("Environment template created (.env.template)")
            else:
                print_info("Environment template already exists")
            
            return True
        except Exception as e:
            print_error(f"Failed to setup configuration: {e}")
            return False
    
    def check_ports(self) -> int:
        print_step(6, "Network Setup", "Finding available port for web interface")
        
        preferred_ports = [5000, 8000, 8080, 3000, 8888]
        
        for port in preferred_ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('localhost', port))
                    print_success(f"Port {port} is available")
                    return port
            except OSError:
                print_info(f"Port {port} is in use")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))
            port = s.getsockname()[1]
            print_success(f"Using available port: {port}")
            return port
    
    def load_env_config(self):
        """Load configuration from .env file."""
        env_path = self.base_path / '.env'
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            self.config[key.strip()] = value.strip()
            except Exception as e:
                self.logger.error(f"Failed to load .env config: {e}")
    
    def get_network_info(self) -> tuple:
        """Get WLAN/LAN and public IP addresses."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            wlan_ip = s.getsockname()[0]
            s.close()
        except Exception:
            wlan_ip = '127.0.0.1'

        try:
            public_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf8').strip()
        except Exception:
            public_ip = 'unknown'
        
        return wlan_ip, public_ip
    
    def start_website(self, host: str = '0.0.0.0', port: int = 5000, open_browser: bool = True) -> Optional[subprocess.Popen]:
        """Start the Flask website."""
        flask_app_file = self.base_path / 'server' / 'app.py'
        if not flask_app_file.exists():
            self.logger.info(f"No Flask app found at {flask_app_file}")
            return None

        if platform.system() == 'Windows':
            venv_python = self.venv_path / 'Scripts' / 'python.exe'
        else:
            venv_python = self.venv_path / 'bin' / 'python'
        
        if not venv_python.exists():
            self.logger.info("Project venv Python not found, trying system Python.")
            venv_python = shutil.which('python') or shutil.which('python3')

        cmd = [str(venv_python), '-m', 'flask', 'run', '--host', host, '--port', str(port)]
        env = os.environ.copy()
        env['FLASK_APP'] = str(flask_app_file)
        env['FLASK_ENV'] = 'development' if self.config.get('app', {}).get('debug') else 'production'
        
        wlan_ip, public_ip = self.get_network_info()
        env['WLAN_IP'] = wlan_ip
        env['PUBLIC_IP'] = public_ip
        
        self.logger.info(f"Starting Flask app at http://{host}:{port}")
        
        flask_log = self.logs_path / 'flask-server.log'
        flask_log.parent.mkdir(parents=True, exist_ok=True)
        
        log_f = open(flask_log, 'a', encoding='utf-8')
        
        # Use a specific environment for the subprocess
        proc_env = os.environ.copy()
        proc_env.update(env)
        
        proc = subprocess.Popen(
            cmd,
            cwd=str(self.base_path), # Run from base path
            stdout=log_f,
            stderr=log_f,
            env=proc_env,
            text=True
        )

        if open_browser:
            # Wait for the server to be ready before opening the browser
            self.wait_for_server(host, port, open_browser=True)

        self.website_process = proc
        return proc
    
    def wait_for_server(self, host: str, port: int, timeout: int = 30, open_browser: bool = False):
        """Waits for the Flask server to start and optionally opens a browser."""
        start_time = time.time()
        
        # Use 127.0.0.1 for health check as it's most reliable locally
        check_host = '127.0.0.1'
        health_url = f'http://{check_host}:{port}/health'
        web_url = f'http://{check_host}:{port}/'

        print_info(f"Waiting for web server to start (up to {timeout}s)...")
        
        server_ready = False
        while time.time() - start_time < timeout:
            try:
                with urllib.request.urlopen(health_url, timeout=1) as response:
                    if response.status == 200:
                        print_success("Web server is running.")
                        server_ready = True
                        break
            except (urllib.error.URLError, socket.timeout):
                # This is expected if the server is not yet up
                time.sleep(0.5)
            except Exception as e:
                self.logger.error(f"Error while waiting for server: {e}")
                time.sleep(1)
        
        if server_ready:
            if open_browser:
                try:
                    webbrowser.open(web_url)
                    print_success(f"Opened website in your browser: {web_url}")
                except Exception as e:
                    print_warning(f"Could not open browser: {e}")
                    print_info(f"Please open manually: {web_url}")
        else:
            print_error("Web server failed to start in time.")
            print_info("The server might still be running in the background.")
            print_info(f"Try accessing it manually at {web_url}")

    def open_firewall_port(self, port: int) -> bool:
        """Open firewall port for incoming connections. Does not require admin rights."""
        try:
            if platform.system() == 'Windows':
                # First, check if the rule already exists
                check_cmd = [
                    "netsh", "advfirewall", "firewall", "show", "rule", f"name=DiscordBotManager-{port}"
                ]
                try:
                    result = subprocess.run(check_cmd, check=True, capture_output=True, text=True)
                    if "No rules match the specified criteria" not in result.stdout:
                        print_info(f"Firewall rule 'DiscordBotManager-{port}' already exists.")
                        return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    # If check fails, we assume we need to add it.
                    pass

                # Add the rule. This may fail without admin rights.
                add_cmd = [
                    "netsh", "advfirewall", "firewall", "add", "rule",
                    f"name=DiscordBotManager-{port}", "dir=in", "action=allow",
                    "protocol=TCP", f"localport={port}"
                ]
                subprocess.run(add_cmd, check=True, capture_output=True, text=True)
                self.logger.info(f"Successfully opened Windows firewall TCP port {port}")
                print_success(f"Firewall port {port} opened (Windows).")
                return True
            elif platform.system() == 'Linux':
                # Linux implementation remains the same
                if shutil.which('ufw'):
                    subprocess.run(['sudo', 'ufw', 'allow', str(port)], check=True, capture_output=True)
                    self.logger.info(f"Opened UFW TCP port {port}")
                    print_success(f"Firewall port {port} opened (UFW)")
                    return True
                else:
                    print_warning("UFW not found, please open port manually")
                    return False
            else:
                print_warning("Automatic firewall opening not supported on this OS")
                return False
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            print_warning(f"Failed to open firewall port. Please run as administrator or open port {port} manually.")
            self.logger.warning(f"Firewall command failed: {e}")
            return False
        except Exception as e:
            print_error(f"An unexpected error occurred while managing firewall: {e}")
            self.logger.error(f"Firewall management error: {e}")
            return False
    
    def start_bot(self, bot_id: str) -> dict:
        """Start a Discord bot."""
        try:
            bots_file = self.data_path / 'bots.json'
            if not bots_file.exists():
                return {"success": False, "message": "Bots configuration not found"}
            
            with open(bots_file, 'r', encoding='utf-8') as f:
                bots = json.load(f)
            
            bot = next((b for b in bots if b['id'] == bot_id), None)
            if not bot:
                return {"success": False, "message": f"Bot {bot_id} not found"}
            
            if bot_id in self.bot_processes:
                return {"success": False, "message": "Bot is already running"}
            
            bot_dir = self.bots_path / bot['folder']
            if not bot_dir.exists():
                return {"success": False, "message": f"Bot directory not found"}
            
            python_exe = str(self.venv_path / 'Scripts' / 'python.exe') if platform.system() == 'Windows' else str(self.venv_path / 'bin' / 'python')
            
            start_script = bot_dir / bot.get('start', 'start.py')
            if not start_script.exists():
                return {"success": False, "message": "Start script not found"}
            
            timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
            log_file = self.logs_path / f"{bot['folder']}-{timestamp}.log"
            
            with open(log_file, 'w', encoding='utf-8') as f:
                process = subprocess.Popen(
                    [python_exe, str(start_script)],
                    cwd=str(bot_dir),
                    stdout=f,
                    stderr=subprocess.STDOUT,
                    text=True
                )
            
            self.bot_processes[bot_id] = process
            bot['status'] = 'online'
            
            with open(bots_file, 'w', encoding='utf-8') as f:
                json.dump(bots, f, indent=2)
            
            return {"success": True, "message": f"Bot started"}
            
        except Exception as e:
            self.logger.error(f"Failed to start bot: {e}")
            return {"success": False, "message": str(e)}
    
    def stop_bot(self, bot_id: str) -> dict:
        """Stop a Discord bot."""
        try:
            if bot_id not in self.bot_processes:
                return {"success": False, "message": "Bot is not running"}
            
            process = self.bot_processes[bot_id]
            process.terminate()
            
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
            
            del self.bot_processes[bot_id]
            
            bots_file = self.data_path / 'bots.json'
            if bots_file.exists():
                with open(bots_file, 'r', encoding='utf-8') as f:
                    bots = json.load(f)
                
                for bot in bots:
                    if bot['id'] == bot_id:
                        bot['status'] = 'offline'
                        break
                
                with open(bots_file, 'w', encoding='utf-8') as f:
                    json.dump(bots, f, indent=2)
            
            return {"success": True, "message": "Bot stopped"}
            
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def run_setup(self) -> bool:
        """Run the complete setup process."""
        print_banner()
        print(f"{Colors.WHITE}Setting up Discord Bot Manager for first use...{Colors.RESET}\n")
        
        setup_steps = [
            self.check_python_version,
            self.create_directories,
            self.setup_virtual_environment,
            self.install_dependencies,
            self.create_default_config,
            lambda: True,
        ]
        
        for i, step in enumerate(setup_steps, 1):
            try:
                if not step():
                    print_error(f"Setup failed at step {i}")
                    return False
            except KeyboardInterrupt:
                print_error("\nSetup interrupted")
                return False
            except Exception as e:
                print_error(f"Error in step {i}: {e}")
                return False
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}Setup completed successfully!{Colors.RESET}")
        print(f"{Colors.CYAN}Next steps:{Colors.RESET}")
        print(f"  • Edit .env file with your Discord credentials")
        print(f"  • Run the application to start the web interface")
        print(f"  • Access the website in your browser")
        
        return True
    
    def run_server(self):
        """Run the complete server with website and bot management."""
        print_banner()
        print(f"{Colors.WHITE}Starting Discord Bot Manager Server...{Colors.RESET}\n")
        
        self.load_env_config()
        
        wlan_ip, public_ip = self.get_network_info()
        print_info(f"WLAN/LAN IP: {wlan_ip}")
        print_info(f"Public IP: {public_ip}")
        
        host = self.config.get('HOST') or '0.0.0.0'
        port = int(self.config.get('PORT') or 5000)
        
        print_info(f"Starting website on {host}:{port}...")
        self.start_website(host=host, port=port, open_browser=True)
        self.open_firewall_port(port)
        
        print(f"\n{Colors.GREEN}Server running!{Colors.RESET}")
        print(f"{Colors.GREEN}Press Ctrl+C to stop{Colors.RESET}\n")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Shutting down...{Colors.RESET}")
            
            for bot_id, process in list(self.bot_processes.items()):
                process.terminate()
            
            if self.website_process:
                self.website_process.terminate()
            
            print_success("Shutdown complete")


def main():
    """Main entry point."""
    manager = DiscordBotManager()
    try:
        # Always ensure dependencies are installed before running the server.
        print_banner()
        print(f"{Colors.WHITE}Ensuring all dependencies are up to date...{Colors.RESET}\n")
        if not manager.install_dependencies():
            print(f"\n{Colors.RED}Dependency installation failed. Please check the errors above.{Colors.RESET}")
            sys.exit(1)

        # Check for and create missing directories and config files without a full setup run.
        if not manager.create_directories():
             print(f"\n{Colors.RED}Directory creation failed.{Colors.RESET}")
             sys.exit(1)
        if not manager.create_default_config():
             print(f"\n{Colors.RED}Configuration setup failed.{Colors.RESET}")
             sys.exit(1)

        # Now, proceed to start the server.
        manager.run_server()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user. Shutting down...{Colors.RESET}")
        if manager.website_process:
            manager.website_process.terminate()
        sys.exit(0)
    except Exception as e:
        logging.exception(f"A critical error occurred: {e}")
        print(f"{Colors.RED}A critical error occurred: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()