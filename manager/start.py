#!/usr/bin/env python3
"""
Discord Bot Manager - Universal Starter
Created by headx & the psychon

Universal script that works on Windows, Linux, and macOS
Handles installation, setup, and server startup automatically
"""

import os
import sys
import subprocess
import socket
import logging
import time
import json
import signal
import threading
import platform
import shutil
import urllib.request
import mimetypes
import html
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import socketserver
from urllib.parse import urlparse, parse_qs, parse_qsl
from typing import Optional, Dict, Any

# Try to import auth, install dependencies if needed
try:
    from backend.auth.auth import auth
except ImportError:
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv"], check=True)
    from backend.auth.auth import auth

# ANSI color codes for colored output (works on all platforms)
class Colors:
    """Cross-platform colored output"""
    if platform.system() == 'Windows':
        # Enable ANSI colors on Windows 10+
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except:
            pass
    
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def disable():
        """Disable colors for unsupported terminals"""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.END = ''
        Colors.BOLD = ''

class SimpleWebServer:
    """Simple web server for serving static files and basic PHP"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.server_dir = self.base_dir
        self.logs_dir = self.base_dir / 'logs'
        self.bots_dir = self.base_dir / 'bots'
        self.templates_dir = self.base_dir / 'cmdtamplates'
        
        # Create required directories
        self.logs_dir.mkdir(exist_ok=True)
        self.bots_dir.mkdir(exist_ok=True)
        self.templates_dir.mkdir(exist_ok=True)
        
        self.logger = self._setup_logging()
        self.current_port = None
        self.server = None
        self._setup_signal_handlers()
    
        def _setup_logging(self):
        """Setup logging with file and console output"""
        timestamp = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs_dir / f'server-{timestamp}.log'
        
        # Create file handler with UTF-8 encoding
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
        
        # Create console handler with UTF-8 encoding
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s'))
        
        # Create logger
        logger = logging.getLogger('SimpleWebServer')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        logger.info(f"Logging to: {log_file}")
        return logger
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Signal {signum} received. Shutting down server...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    def get_public_ip(self):
        """Get public IP address"""
        try:
            with urllib.request.urlopen('https://api.ipify.org?format=text', timeout=5) as response:
                return response.read().decode().strip()
        except:
            try:
                with urllib.request.urlopen('https://ifconfig.me/ip', timeout=5) as response:
                    return response.read().decode().strip()
            except:
                return None
    
    def is_port_available(self, port, host="0.0.0.0"):
        """Check if port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                result = sock.connect_ex((host, port))
                return result != 0
        except Exception:
            return False
    
    def find_available_port(self):
        """Find available port"""
        preferred_ports = [8000, 5000, 8080, 3000, 80, 8888, 9000]
        
        for port in preferred_ports:
            if self.is_port_available(port):
                self.logger.info(f"Using port: {port}")
                return port
        
        for port in range(5000, 9000):
            if self.is_port_available(port):
                self.logger.info(f"Found free port: {port}")
                return port
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(('', 0))
            port = sock.getsockname()[1]
            self.logger.info(f"OS chose port {port}")
            return port
    
    def execute_php(self, php_file):
        """Execute PHP file and return output"""
        try:
            result = subprocess.run(
                ['php', str(php_file)],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.server_dir
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"PHP Error: {result.stderr}"
                
        except FileNotFoundError:
            return "PHP not installed"
        except subprocess.TimeoutExpired:
            return "PHP script timeout"
        except Exception as e:
            return f"PHP execution error: {e}"

    def start(self):
        """Start the web server"""
        try:
            self.logger.info("=" * 60)
            self.logger.info("=== Discord Bot Manager Web Server ===")
            self.logger.info("=" * 60)
            
            if not self.server_dir.exists():
                self.logger.error(f"❌ Server directory not found: {self.server_dir}")
                self.logger.info("Creating directory...")
                self.server_dir.mkdir(parents=True, exist_ok=True)
            
            required_files = ['index.html']
            for file_name in required_files:
                file_path = self.server_dir / file_name
                if not file_path.exists():
                    self.logger.warning(f"⚠️  File not found: {file_name}")
            
            port = self.find_available_port()
            self.current_port = port
            
            local_ip = self.get_local_ip()
            public_ip = self.get_public_ip()
            
            self.logger.info("=" * 50)
            self.logger.info("=== SERVER ACCESS ===")
            self.logger.info("=" * 50)
            self.logger.info(f"[*] Localhost:      http://127.0.0.1:{port}")
            self.logger.info(f"[*] Local Network:  http://{local_ip}:{port}")
            
            if public_ip:
                self.logger.info(f"[*] Public IP:      {public_ip}")
                self.logger.info(f"[*] Public Access:  http://{public_ip}:{port}")
                self.logger.info("    (Port forwarding required in router)")
            
            self.logger.info("=" * 50)
            self.logger.info(f"[*] Serving files from: {self.server_dir}")
            self.logger.info("[!] Press Ctrl+C to stop")
            self.logger.info("=" * 50)
            
            def handler(*args, **kwargs):
                return CustomHTTPRequestHandler(*args, server_instance=self, **kwargs)
            
            self.server = ThreadedHTTPServer(("0.0.0.0", port), handler)
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            self.logger.info("🛑 Server stopping...")
        except Exception as e:
            self.logger.error(f"💥 Error: {e}")
            sys.exit(1)
    
    def shutdown(self):
        """Shutdown the server"""
        if self.server:
            self.logger.info("🔄 Server shutting down...")
            self.server.shutdown()
            self.server.server_close()
        self.logger.info("✅ Server stopped")

class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom HTTP request handler with PHP support"""
    
    def __init__(self, *args, server_instance=None, **kwargs):
        self.server_instance = server_instance
        super().__init__(*args, **kwargs)
    
        def do_GET(self):
        """Handle GET requests"""
        try:
            os.chdir(self.server_instance.server_dir)
            parsed_path = urlparse(self.path)
            file_path = parsed_path.path.lstrip('/')
            query_params = dict(parse_qsl(parsed_path.query))
            
            # Handle Discord OAuth2 callback
            if file_path == 'auth/callback':
                self._handle_oauth_callback(query_params)
                return
            
            # Handle auth URL generation
            if file_path == 'auth/login':
                self._handle_auth_login()
                return
            
            # Handle user info
            if file_path == 'api/user':
                self._handle_user_info()
                return
            
            # Handle Discord applications
            if file_path == 'api/discord/applications':
                self._handle_discord_applications()
                return
            
            # Handle logout
            if file_path == 'auth/logout':
                self._handle_logout()
                return
            
            if not file_path or file_path == '/':
                file_path = 'index.html'
            
            full_path = self.server_instance.server_dir / file_path
            
            if not full_path.exists():
                self.send_error(404, f"File not found: {file_path}")
                return
            
            if file_path.endswith('.php'):
                try:
                    output = self.server_instance.execute_php(full_path)
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', len(output.encode()))
                    self.end_headers()
                    self.wfile.write(output.encode())
                    return
                except Exception as e:
                    self.send_error(500, f"PHP execution error: {e}")
                    return
            
            try:
                with open(full_path, 'rb') as f:
                    content = f.read()
                
                content_type, _ = mimetypes.guess_type(str(full_path))
                if content_type is None:
                    content_type = 'application/octet-stream'
                
                self.send_response(200)
                self.send_header('Content-type', content_type)
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
                
            except Exception as e:
                self.send_error(500, f"Error reading file: {e}")
                
        except Exception as e:
            self.server_instance.logger.error(f"Request handling error: {e}")
            self.send_error(500, "Internal server error")
    
    def do_POST(self):
        """Handle POST requests (for PHP)"""
        try:
            parsed_path = urlparse(self.path)
            file_path = parsed_path.path.lstrip('/')
            
            if file_path.endswith('.php'):
                full_path = self.server_instance.server_dir / file_path
                
                if full_path.exists():
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    
                    env = os.environ.copy()
                    env['REQUEST_METHOD'] = 'POST'
                    env['CONTENT_LENGTH'] = str(content_length)
                    env['CONTENT_TYPE'] = self.headers.get('Content-Type', '')
                    
                    try:
                        result = subprocess.run(
                            ['php', str(full_path)],
                            input=post_data,
                            capture_output=True,
                            timeout=30,
                            cwd=self.server_instance.server_dir,
                            env=env
                        )
                        
                        if result.returncode == 0:
                            output = result.stdout.decode()
                            self.send_response(200)
                            self.send_header('Content-type', 'text/html; charset=utf-8')
                            self.send_header('Content-Length', len(output.encode()))
                            self.end_headers()
                            self.wfile.write(output.encode())
                        else:
                            self.send_error(500, f"PHP Error: {result.stderr.decode()}")
                            
                    except Exception as e:
                        self.send_error(500, f"PHP execution error: {e}")
                else:
                    self.send_error(404, "PHP file not found")
            else:
                self.send_error(405, "Method not allowed")
                
        except Exception as e:
            self.server_instance.logger.error(f"POST handling error: {e}")
            self.send_error(500, "Internal server error")
    
        def _get_session_cookie(self):
        """Extract session cookie from request"""
        cookie_header = self.headers.get('Cookie', '')
        cookies = dict(item.split('=', 1) for item in cookie_header.split('; ') if '=' in item)
        return cookies.get('session_id')
    
    def _set_session_cookie(self, session_id):
        """Set session cookie in response"""
        self.send_header('Set-Cookie', f'session_id={session_id}; Path=/; HttpOnly; Max-Age=604800')
    
    def _handle_oauth_callback(self, params):
        """Handle Discord OAuth2 callback"""
        code = params.get('code')
        state = params.get('state')
        error = params.get('error')
        
        if error:
            self._send_json_response({'error': error}, 400)
            return
        
        if not code:
            self._send_json_response({'error': 'No authorization code'}, 400)
            return
        
        # Exchange code for token
        token_data = auth.exchange_code(code)
        if not token_data:
            self._send_json_response({'error': 'Failed to exchange code'}, 500)
            return
        
        # Get user info
        user_info = auth.get_user_info(token_data['access_token'])
        if not user_info:
            self._send_json_response({'error': 'Failed to get user info'}, 500)
            return
        
        # Create session
        session_id = auth.create_session(user_info['id'], user_info, token_data)
        
        # Redirect to main page with session cookie
        self.send_response(302)
        self._set_session_cookie(session_id)
        self.send_header('Location', '/?login=success')
        self.end_headers()
    
    def _handle_auth_login(self):
        """Generate and return Discord OAuth2 URL"""
        auth_url = auth.generate_auth_url()
        self._send_json_response({'auth_url': auth_url})
    
    def _handle_user_info(self):
        """Return current user info"""
        session_id = self._get_session_cookie()
        
        if not session_id:
            self._send_json_response({'authenticated': False}, 200)
            return
        
        session_data = auth.validate_session(session_id)
        
        if not session_data:
            self._send_json_response({'authenticated': False}, 200)
            return
        
        self._send_json_response({
            'authenticated': True,
            'user': session_data['user']
        })
    
    def _handle_discord_applications(self):
        """Get user's Discord applications"""
        session_id = self._get_session_cookie()
        
        if not session_id:
            self._send_json_response({'error': 'Not authenticated'}, 401)
            return
        
        session_data = auth.validate_session(session_id)
        
        if not session_data:
            self._send_json_response({'error': 'Invalid session'}, 401)
            return
        
        access_token = session_data['session']['access_token']
        
        # Get user's applications
        applications = auth.get_user_applications(access_token)
        
        if applications is None:
            self._send_json_response({'error': 'Failed to fetch applications'}, 500)
            return
        
        self._send_json_response({'applications': applications})
    
    def _handle_logout(self):
        """Logout user"""
        session_id = self._get_session_cookie()
        
        if session_id:
            auth.logout(session_id)
        
        self.send_response(302)
        self.send_header('Set-Cookie', 'session_id=; Path=/; HttpOnly; Max-Age=0')
        self.send_header('Location', '/')
        self.end_headers()
    
    def _send_json_response(self, data, status=200):
        """Send JSON response"""
        json_data = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_data))
        self.end_headers()
        self.wfile.write(json_data)
    
    def log_message(self, format, *args):
        """Override log message to use our logger"""
        self.server_instance.logger.info(f"{self.address_string()} - {format % args}")

class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    """Threaded HTTP server for better performance"""
    daemon_threads = True
    allow_reuse_address = True

def print_color(text, color, bold=False):
    """Print colored text"""
    if bold:
        print(f"{Colors.BOLD}{color}{text}{Colors.END}")
    else:
        print(f"{color}{text}{Colors.END}")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print_color("Error: Python 3.8 or higher is required", Colors.RED, True)
        sys.exit(1)
    print_color("✓ Python version check passed", Colors.GREEN)

def check_package_manager():
    """Check which package manager is available (cross-platform)"""
    def _check_cmd(cmd):
        try:
            if platform.system() == "Windows":
                result = subprocess.run([cmd, '--version'], 
                                      capture_output=True, 
                                      shell=True,
                                      text=True)
            else:
                result = subprocess.run(['which', cmd], 
                                      capture_output=True,
                                      text=True)
            return result.returncode == 0
        except:
            return False

    system = platform.system().lower()
    
    # Windows package managers
    if system == "windows":
        if _check_cmd('winget'):
            return "winget", "winget install -e --id PHP.PHP"
        elif _check_cmd('choco'):
            return "choco", "choco install php -y"
        elif _check_cmd('scoop'):
            return "scoop", "scoop install php"
        else:
            return "manual", "https://windows.php.net/download/"
    
    # Linux package managers
    elif system == "linux":
        # Debian/Ubuntu
        if _check_cmd('apt-get') or _check_cmd('apt'):
            return "apt", "sudo apt update && sudo apt install -y php php-cli php-common"
        # Fedora/RHEL/CentOS
        elif _check_cmd('dnf'):
            return "dnf", "sudo dnf install -y php php-cli php-common"
        elif _check_cmd('yum'):
            return "yum", "sudo yum install -y php php-cli php-common"
        # Arch Linux
        elif _check_cmd('pacman'):
            return "pacman", "sudo pacman -S --noconfirm php"
        # openSUSE
        elif _check_cmd('zypper'):
            return "zypper", "sudo zypper install -y php php-cli"
        # Alpine Linux
        elif _check_cmd('apk'):
            return "apk", "sudo apk add php php-cli"
        # Universal
        elif _check_cmd('snap'):
            return "snap", "sudo snap install php"
        else:
            return "manual", "Install PHP using your system's package manager"
    
    # macOS
    elif system == "darwin":
        if _check_cmd('brew'):
            return "brew", "brew install php"
        else:
            # Install Homebrew first
            return "brew-install", '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    
    return "unknown", "Manual installation required"

def install_system_dependencies():
    """Install system-level dependencies (cross-platform)"""
    # Check if PHP is already installed
    try:
        result = subprocess.run(['php', '--version'], 
                              capture_output=True, 
                              text=True,
                              shell=(platform.system() == "Windows"))
        if result.returncode == 0:
            version = result.stdout.split()[1] if result.stdout else "unknown"
            print_color(f"✓ PHP {version} is already installed", Colors.GREEN)
            return True
    except FileNotFoundError:
        pass
    
    # Get package manager
    pkg_manager, install_cmd = check_package_manager()
    
    if pkg_manager == "unknown":
        print_color("⚠ Could not detect package manager", Colors.YELLOW)
        print_color("PHP installation skipped - bot manager will work without PHP", Colors.YELLOW)
        return True
    
    if pkg_manager == "manual":
        print_color("⚠ Manual PHP installation required", Colors.YELLOW)
        print_color(f"Download from: {install_cmd}", Colors.BLUE)
        print_color("PHP is optional for bot manager core functionality", Colors.YELLOW)
        return True
    
    # Try to install
    print_color(f"Installing PHP using {pkg_manager}...", Colors.YELLOW)
    
    try:
        if pkg_manager == "brew-install":
            print_color("Installing Homebrew first...", Colors.YELLOW)
            subprocess.run(install_cmd, shell=True, check=True)
            install_cmd = "brew install php"
        
        # Ask for confirmation on Linux/macOS (requires sudo)
        if platform.system() != "Windows" and "sudo" in install_cmd:
            print_color("\n⚠ This requires administrator privileges", Colors.YELLOW)
            response = input("Continue with installation? [Y/n]: ").strip().lower()
            if response and response != 'y':
                print_color("Installation skipped", Colors.YELLOW)
                return True
        
        # Run installation
        subprocess.run(install_cmd, shell=True, check=True)
        print_color("✓ PHP installed successfully", Colors.GREEN)
        return True
        
    except subprocess.CalledProcessError as e:
        print_color(f"⚠ PHP installation failed: {e}", Colors.YELLOW)
        print_color("Continuing without PHP (optional dependency)", Colors.YELLOW)
        return True
    except Exception as e:
        print_color(f"⚠ Unexpected error: {e}", Colors.YELLOW)
        print_color("Continuing without PHP", Colors.YELLOW)
        return True

def install_python_dependencies():
    """Install required Python packages (cross-platform)"""
    # Check if requirements.txt exists
    requirements_file = Path(__file__).parent / 'requirements.txt'
    
    if requirements_file.exists():
        print_color("Installing from requirements.txt...", Colors.BLUE)
        try:
            # Upgrade pip first
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], capture_output=True, check=False)
            
            # Install from requirements.txt
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print_color("✓ All dependencies installed successfully", Colors.GREEN)
            else:
                print_color("⚠ Some dependencies failed to install", Colors.YELLOW)
                if result.stderr:
                    print_color(f"Details: {result.stderr[:200]}...", Colors.YELLOW)
        except Exception as e:
            print_color(f"⚠ Error during installation: {e}", Colors.YELLOW)
    else:
        # Fallback: install minimal requirements
        print_color("requirements.txt not found, installing minimal dependencies...", Colors.YELLOW)
        minimal_requirements = [
            "discord.py>=2.3.2",
            "python-dotenv>=1.0.0",
            "aiohttp>=3.8.5",
        ]
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", "pip"
            ], capture_output=True, check=False)
            
            for req in minimal_requirements:
                print(f"  Installing {req.split('>=')[0]}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", req
                ], capture_output=True)
                
                if result.returncode == 0:
                    print_color(f"  ✓ {req.split('>=')[0]} installed", Colors.GREEN)
                else:
                    print_color(f"  ⚠ {req.split('>=')[0]} failed", Colors.YELLOW)
            
            print_color("✓ Minimal dependencies installed", Colors.GREEN)
        except Exception as e:
            print_color(f"⚠ Error: {e}", Colors.YELLOW)
            print_color("You may need to install dependencies manually", Colors.YELLOW)

def setup_directory_structure():
    """Create necessary directories (cross-platform)"""
    base_path = Path(__file__).parent
    
    directories = {
        "bots": "Bot instances storage",
        "cmdtamplates": "Command templates",
        "cmdtamplates/api": "API templates",
        "cmdtamplates/frontend": "Frontend templates",
        "logs": "Server logs",
        "data": "User data & sessions"
    }
    
    created = 0
    for directory, description in directories.items():
        dir_path = base_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print_color(f"  ✓ Created {directory}/", Colors.GREEN)
            created += 1
        else:
            print(f"  - {directory}/ (exists)")
    
    if created == 0:
        print_color("  ✓ All directories already exist", Colors.GREEN)
    else:
        print_color(f"  ✓ Created {created} new directories", Colors.GREEN)

def create_env_file():
    """Create .env configuration file if it doesn't exist (cross-platform)"""
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        print_color("  - .env file already exists", Colors.YELLOW)
        return
    
    # Create .env with sensible defaults
    env_content = f"""# Discord Bot Manager - Environment Configuration
# Created by headx & the psychon
# Platform: {platform.system()} {platform.release()}
# Python: {sys.version.split()[0]}

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO

# Bot Defaults
DEFAULT_PREFIX=!
ENABLE_HTTPS=False

# Discord OAuth2 Configuration (Optional)
# Get these from: https://discord.com/developers/applications
# 1. Create a new application
# 2. Go to OAuth2 settings
# 3. Add redirect URL: http://localhost:8000/auth/callback
# 4. Copy Client ID and Client Secret below

DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback

# Advanced Settings
# AUTO_RESTART_BOTS=True
# MAX_LOG_SIZE=10485760
# LOG_RETENTION_DAYS=30
"""
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        print_color("  ✓ Created .env configuration file", Colors.GREEN)
        
        # Create .env.example as well
        example_path = Path(__file__).parent / '.env.example'
        if not example_path.exists():
            with open(example_path, 'w', encoding='utf-8') as f:
                f.write(env_content)
            print_color("  ✓ Created .env.example", Colors.GREEN)
    except Exception as e:
        print_color(f"  ⚠ Could not create .env file: {e}", Colors.YELLOW)

def check_and_setup():
    """Check if setup is needed and run it"""
    base_path = Path(__file__).parent
    
    # Check if first run
    setup_marker = base_path / '.setup_complete'
    
    if not setup_marker.exists():
        print_color("\n" + "="*60, Colors.BLUE)
        print_color("   FIRST TIME SETUP - Discord Bot Manager", Colors.HEADER, True)
        print_color("   Created by headx & the psychon", Colors.BLUE)
        print_color("="*60 + "\n", Colors.BLUE)
        
        # Check Python version
        print_color("[1/5] Checking Python version...", Colors.BLUE)
        check_python_version()
        
        # Install system dependencies
        print_color("\n[2/5] Installing system dependencies...", Colors.BLUE)
        if not install_system_dependencies():
            print_color("Warning: Some system dependencies failed to install", Colors.YELLOW)
            print_color("The bot manager will still work, but some features might be limited", Colors.YELLOW)
        
        # Install Python dependencies
        print_color("\n[3/5] Installing Python dependencies...", Colors.BLUE)
        install_python_dependencies()
        
        # Setup directories
        print_color("\n[4/5] Setting up directory structure...", Colors.BLUE)
        setup_directory_structure()
        
        # Create config files
        print_color("\n[5/5] Creating configuration files...", Colors.BLUE)
        create_env_file()
        
        # Mark setup as complete
        setup_marker.touch()
        
        print_color("\n" + "="*60, Colors.GREEN)
        print_color("   ✓ SETUP COMPLETE!", Colors.GREEN, True)
        print_color("="*60 + "\n", Colors.GREEN)
        
        time.sleep(1)

def main():
    """Main entry point"""
    try:
        # ASCII Art Banner
        print_banner()
        
        # Check and run setup if needed
        check_and_setup()
        
        # Start the server
        print_color("Starting Discord Bot Manager Server...", Colors.BLUE, True)
        print_color("Press Ctrl+C to stop\n", Colors.YELLOW)
        
        server = SimpleWebServer()
        server.start()
        
    except KeyboardInterrupt:
        print_color("\n\n🛑 Server stopped by user", Colors.YELLOW)
        print_color("Goodbye! 👋\n", Colors.GREEN)
    except Exception as e:
        print_color(f"\n\n❌ Error: {e}", Colors.RED, True)
        print_color("Check the logs for more details\n", Colors.YELLOW)
        sys.exit(1)

def print_banner():
    """Print ASCII art banner"""
    banner = f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  {Colors.HEADER}🤖  DISCORD BOT MANAGER  🤖{Colors.BLUE}                          ║
║                                                           ║
║  {Colors.GREEN}✨ Universal Edition v2.0{Colors.BLUE}                            ║
║  {Colors.YELLOW}👨‍💻 Created by headx & the psychon{Colors.BLUE}                   ║
║                                                           ║
║  {Colors.CYAN}Platform: {platform.system()} {platform.release()}{Colors.BLUE}                          ║
║  {Colors.CYAN}Python: {sys.version.split()[0]}{Colors.BLUE}                                      ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)

if __name__ == "__main__":
    main()
