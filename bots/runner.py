import os
import sys
import subprocess
import signal
import json
import time
import logging
from datetime import datetime
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('runner.log'),
        logging.StreamHandler()
    ]
)

def is_process_running(pid):
    """Check if a process is running by PID"""
    try:
        process = psutil.Process(pid)
        return process.is_running()
    except psutil.NoSuchProcess:
        return False

def kill_process(pid):
    """Kill a process and its children"""
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except psutil.NoSuchProcess:
                pass
        parent.terminate()
        
        # Wait for processes to terminate
        _, alive = psutil.wait_procs(children + [parent], timeout=3)
        
        # Force kill if still alive
        for p in alive:
            try:
                p.kill()
            except psutil.NoSuchProcess:
                pass
                
    except psutil.NoSuchProcess:
        pass

def run_bot(folder, start_file, token):
    """Run a Discord bot in a managed process"""
    os.environ['DISCORD_TOKEN'] = token
    original_dir = os.getcwd()
    
    try:
        # Set up bot directory
        folder_path = os.path.abspath(folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            logging.info(f"Created bot directory: {folder_path}")
        
        # Change to bot directory
        os.chdir(folder_path)
        logging.info(f"Changed to directory: {folder_path}")
        
        # Install requirements if they exist
        if os.path.exists('requirements.txt'):
            logging.info("Installing requirements...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
                logging.info("Requirements installed successfully")
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to install requirements: {e}")
                os.chdir(original_dir)
                return None
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Start the bot with log redirection
        log_file = f'logs/bot-{datetime.now():%Y-%m-%d_%H-%M-%S}.log'
        with open(log_file, 'w') as f:
            process = subprocess.Popen(
                [sys.executable, start_file],
                stdout=f,
                stderr=subprocess.STDOUT,
                # Create new process group on Windows
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
        
        # Save process info
        with open('runner_pid.txt', 'w') as f:
            json.dump({
                'pid': process.pid,
                'start_time': datetime.now().isoformat(),
                'folder': folder_path,
                'log_file': log_file
            }, f)
        
        # Return to original directory
        os.chdir(original_dir)
        
        return process
        
    except Exception as e:
        logging.error(f"Error running bot: {e}")
        if os.getcwd() != original_dir:
            os.chdir(original_dir)
        return None

def handle_signals():
    """Set up signal handlers for graceful shutdown"""
    def signal_handler(signum, frame):
        logging.info(f"Received signal {signum}")
        if os.path.exists('runner_pid.txt'):
            try:
                with open('runner_pid.txt', 'r') as f:
                    data = json.load(f)
                    if is_process_running(data['pid']):
                        kill_process(data['pid'])
                        logging.info(f"Terminated bot process {data['pid']}")
            except Exception as e:
                logging.error(f"Error handling shutdown: {e}")
            os.unlink('runner_pid.txt')
        sys.exit(0)

    # Register signal handlers
    if os.name == 'nt':  # Windows
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    else:  # Unix
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)

def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        logging.error("Usage: python runner.py <bot_id>")
        sys.exit(1)
    
    bot_id = sys.argv[1]
    logging.info(f"Starting bot with ID: {bot_id}")
    
    try:
        # Set up signal handlers
        handle_signals()
        
        # Load bot configuration
        with open('../data/bots.json', 'r') as f:
            bots = json.load(f)
        
        bot = next((b for b in bots if b['id'] == bot_id), None)
        if not bot:
            logging.error(f"Bot with ID {bot_id} not found")
            sys.exit(1)
        
        # Check if bot is already running
        if os.path.exists('runner_pid.txt'):
            try:
                with open('runner_pid.txt', 'r') as f:
                    data = json.load(f)
                    if is_process_running(data['pid']):
                        logging.error(f"Bot is already running with PID {data['pid']}")
                        sys.exit(1)
            except Exception:
                pass  # Ignore errors reading old runner_pid.txt
            os.unlink('runner_pid.txt')
        
        # Run the bot
        process = run_bot(bot['folder'], bot['start'], bot['token'])
        if process:
            logging.info(f"Bot started successfully with PID {process.pid}")
            
            # Update bot status in configuration
            bot['status'] = 'online'
            bot['processId'] = process.pid
            bot['lastUpdated'] = datetime.now().isoformat()
            with open('../data/bots.json', 'w') as f:
                json.dump(bots, f, indent=2)
            
            # Wait for process to complete
            try:
                process.wait()
            except KeyboardInterrupt:
                logging.info("Received keyboard interrupt")
                kill_process(process.pid)
            
            # Update status on shutdown
            bot['status'] = 'offline'
            bot['processId'] = None
            bot['lastUpdated'] = datetime.now().isoformat()
            with open('../data/bots.json', 'w') as f:
                json.dump(bots, f, indent=2)
        else:
            logging.error("Failed to start bot")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"Error running bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
