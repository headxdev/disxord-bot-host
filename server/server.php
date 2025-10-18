<?php
/**
 * Discord Bot Manager Server
 * Backend API for bot management
 * 
 * @author headx & the psychon
 * @version 2.0
 */

// Security headers
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('X-XSS-Protection: 1; mode=block');

// Enable error reporting for development
error_reporting(E_ALL);
ini_set('display_errors', 0); // Don't display errors in production

// Custom error handler to log errors
set_error_handler(function($severity, $message, $file, $line) {
    error_log("PHP Error [$severity]: $message in $file on line $line");
    if ($severity === E_ERROR || $severity === E_PARSE) {
        sendError('Internal server error');
    }
});

/**
 * Send error response
 * @param string $message Error message
 * @param int $code HTTP status code
 */
function sendError($message, $code = 400) {
    http_response_code($code);
    echo json_encode([
        'status' => 'error',
        'message' => filter_var($message, FILTER_SANITIZE_STRING),
        'timestamp' => time()
    ], JSON_UNESCAPED_UNICODE);
    exit;
}

/**
 * Send success response
 * @param array $data Response data
 */
function sendSuccess($data = []) {
    $response = array_merge([
        'status' => 'success',
        'timestamp' => time()
    ], $data);
    echo json_encode($response, JSON_UNESCAPED_UNICODE);
    exit;
}

// Validate request method
$allowedMethods = ['GET', 'POST'];
if (!in_array($_SERVER['REQUEST_METHOD'], $allowedMethods)) {
    sendError('Method not allowed', 405);
}

// Get request data with validation
$requestData = null;
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $rawInput = file_get_contents('php://input');
    if (!empty($rawInput)) {
        $requestData = json_decode($rawInput, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            sendError('Invalid JSON data', 400);
        }
    }
}

// Get and validate action
$action = filter_var($_GET['action'] ?? ($requestData['action'] ?? null), FILTER_SANITIZE_STRING);

if (!$action) {
    sendError('No action specified', 400);
}

// Validate action against whitelist
$allowedActions = [
    'list_bots', 'create_bot', 'start_bot', 'stop_bot', 
    'delete_bot', 'get_logs', 'health', 'get_status'
];

if (!in_array($action, $allowedActions)) {
    sendError('Invalid action specified', 400);
}

// Route actions
switch ($action) {
    case 'list_bots':
        listBots();
        break;
        
    case 'create_bot':
        if (!$requestData) sendError('No bot data provided');
        createBot($requestData);
        break;
        
    case 'start_bot':
        if (!isset($_GET['name']) && !isset($requestData['name'])) {
            sendError('Bot name required');
        }
        startBot($_GET['name'] ?? $requestData['name']);
        break;
        
    case 'stop_bot':
        if (!isset($_GET['name']) && !isset($requestData['name'])) {
            sendError('Bot name required');
        }
        stopBot($_GET['name'] ?? $requestData['name']);
        break;
        
    case 'delete_bot':
        if (!isset($_GET['name']) && !isset($requestData['name'])) {
            sendError('Bot name required');
        }
        deleteBot($_GET['name'] ?? $requestData['name']);
        break;
        
    case 'get_logs':
        if (!isset($_GET['name'])) sendError('Bot name required');
        getLogs($_GET['name']);
        break;
        
    default:
        sendError('Invalid action');
}

// List all bots
function listBots() {
    $botDir = __DIR__ . '/bots';
    if (!is_dir($botDir)) {
        mkdir($botDir, 0755, true);
    }
    
    $bots = [];
    foreach (scandir($botDir) as $item) {
        if ($item === '.' || $item === '..' || $item === 'userinfo.txt') continue;
        
        $path = "$botDir/$item";
        if (!is_dir($path)) continue;
        
        // Get bot info
        $configFile = "$path/infos/config.json";
        $config = file_exists($configFile) ? json_decode(file_get_contents($configFile), true) : [];
        
        $bots[] = [
            'name' => $item,
            'status' => checkBotStatus($item),
            'config' => $config,
            'commands' => countCommands($path),
            'lastLog' => getLastLog($path)
        ];
    }
    
    sendSuccess(['bots' => $bots]);
}

// Create a new bot
function createBot($data) {
    if (!isset($data['name']) || !isset($data['token'])) {
        sendError('Name and token required');
    }
    
    $botName = preg_replace('/[^a-zA-Z0-9_-]/', '', $data['name']);
    $botDir = __DIR__ . "/bots/$botName";
    
    if (is_dir($botDir)) {
        sendError('Bot already exists');
    }
    
    // Create directory structure
    mkdir($botDir, 0755, true);
    mkdir("$botDir/cogs", 0755, true);
    mkdir("$botDir/events", 0755, true);
    mkdir("$botDir/commands", 0755, true);
    mkdir("$botDir/logs", 0755, true);
    mkdir("$botDir/infos", 0755, true);
    
    // Save config
    file_put_contents(
        "$botDir/infos/config.json",
        json_encode([
            'token' => $data['token'],
            'prefix' => $data['prefix'] ?? '!',
            'name' => $botName,
            'owner' => $data['owner'] ?? '',
            'created' => date('Y-m-d H:i:s')
        ], JSON_PRETTY_PRINT)
    );
    
    // Create main bot file
    createMainPyFile($botDir, $data);
    
    // Copy command templates if specified
    if (isset($data['templates']) && is_array($data['templates'])) {
        foreach ($data['templates'] as $template) {
            $templateFile = __DIR__ . "/cmdtamplates/$template.py";
            if (file_exists($templateFile)) {
                copy($templateFile, "$botDir/cogs/$template.py");
            }
        }
    }
    
    sendSuccess(['message' => 'Bot created successfully']);
}

// Start a bot
function startBot($name) {
    $botDir = __DIR__ . "/bots/$name";
    if (!is_dir($botDir)) {
        sendError('Bot not found');
    }
    
    if (checkBotStatus($name) === 'running') {
        sendError('Bot is already running');
    }
    
    // Start bot process
    $command = PHP_OS === 'WINNT' 
        ? "start /B python start.py > logs/latest.log 2>&1"
        : "python3 start.py > logs/latest.log 2>&1 &";
    
    chdir($botDir);
    exec($command);
    
    sleep(2); // Wait for bot to start
    
    if (checkBotStatus($name) === 'running') {
        sendSuccess(['message' => 'Bot started successfully']);
    } else {
        sendError('Failed to start bot');
    }
}

// Stop a bot
function stopBot($name) {
    if (checkBotStatus($name) !== 'running') {
        sendError('Bot is not running');
    }
    
    if (PHP_OS === 'WINNT') {
        exec("taskkill /F /FI \"WINDOWTITLE eq $name\" /IM python.exe");
    } else {
        exec("pkill -f \"python.*$name/start.py\"");
    }
    
    sleep(1); // Wait for process to end
    
    if (checkBotStatus($name) === 'stopped') {
        sendSuccess(['message' => 'Bot stopped successfully']);
    } else {
        sendError('Failed to stop bot');
    }
}

// Delete a bot
function deleteBot($name) {
    $botDir = __DIR__ . "/bots/$name";
    if (!is_dir($botDir)) {
        sendError('Bot not found');
    }
    
    // Stop bot if running
    if (checkBotStatus($name) === 'running') {
        stopBot($name);
    }
    
    // Delete directory
    deleteDirectory($botDir);
    
    sendSuccess(['message' => 'Bot deleted successfully']);
}

// Get bot logs
function getLogs($name) {
    $botDir = __DIR__ . "/bots/$name";
    $logDir = "$botDir/logs";
    
    if (!is_dir($botDir)) {
        sendError('Bot not found');
    }
    
    if (!is_dir($logDir)) {
        sendSuccess(['logs' => []]);
    }
    
    $logs = [];
    foreach (scandir($logDir) as $file) {
        if ($file === '.' || $file === '..') continue;
        
        $logs[] = [
            'name' => $file,
            'date' => date('Y-m-d H:i:s', filemtime("$logDir/$file")),
            'size' => filesize("$logDir/$file"),
            'content' => file_get_contents("$logDir/$file")
        ];
    }
    
    sendSuccess(['logs' => $logs]);
}

// Utility functions
function checkBotStatus($name) {
    $running = false;
    
    if (PHP_OS === 'WINNT') {
        exec("tasklist /FI \"WINDOWTITLE eq $name\"", $output);
        $running = count($output) > 1;
    } else {
        exec("pgrep -f \"python.*$name/start.py\"", $output);
        $running = !empty($output);
    }
    
    return $running ? 'running' : 'stopped';
}

function countCommands($botPath) {
    $count = 0;
    
    // Count Python commands
    foreach (glob("$botPath/cogs/*.py") as $file) {
        $content = file_get_contents($file);
        $count += substr_count($content, '@commands.command');
    }
    
    // Count JavaScript commands
    $count += count(glob("$botPath/commands/*.js"));
    
    return $count;
}

function getLastLog($botPath) {
    $logDir = "$botPath/logs";
    if (!is_dir($logDir)) return null;
    
    $latest = null;
    $latestTime = 0;
    
    foreach (scandir($logDir) as $file) {
        if ($file === '.' || $file === '..') continue;
        
        $time = filemtime("$logDir/$file");
        if ($time > $latestTime) {
            $latestTime = $time;
            $latest = $file;
        }
    }
    
    return $latest ? [
        'file' => $latest,
        'date' => date('Y-m-d H:i:s', $latestTime),
        'content' => file_get_contents("$logDir/$latest")
    ] : null;
}

function deleteDirectory($dir) {
    if (!is_dir($dir)) return;
    
    $files = array_diff(scandir($dir), ['.', '..']);
    foreach ($files as $file) {
        $path = "$dir/$file";
        is_dir($path) ? deleteDirectory($path) : unlink($path);
    }
    
    rmdir($dir);
}

function createMainPyFile($botDir, $data) {
    $content = <<<PYTHON
import discord
from discord.ext import commands
import json
import os
import logging
from datetime import datetime

# Setup logging
LOG_FILE = f'logs/bot-{datetime.now():%Y-%m-%d_%H-%M-%S}.log'
os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

# Load config
try:
    with open('infos/config.json') as f:
        config = json.load(f)
except Exception as e:
    logging.error(f'Failed to load config: {e}')
    exit(1)

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix=config.get('prefix', '!'),
    intents=intents,
    help_command=None
)

# Load cogs
for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        try:
            bot.load_extension(f'cogs.{filename[:-3]}')
            logging.info(f'Loaded extension: {filename}')
        except Exception as e:
            logging.error(f'Failed to load {filename}: {e}')

@bot.event
async def on_ready():
    logging.info(f'Bot is ready: {bot.user.name}')
    print(f'''
    ===============================
    Bot is ready!
    Name: {bot.user.name}
    ID: {bot.user.id}
    Guilds: {len(bot.guilds)}
    Created by headx and the psychon
    ===============================
    ''')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'❌ Command not found. Use `{bot.command_prefix}help` to see available commands.')
    else:
        logging.error(f'Error in {ctx.command}: {error}')
        await ctx.send(f'❌ An error occurred: {str(error)}')

if __name__ == '__main__':
    try:
        bot.run(config['token'])
    except discord.LoginFailure:
        logging.error('Invalid bot token')
    except Exception as e:
        logging.error(f'Failed to start bot: {e}')
PYTHON;

    file_put_contents("$botDir/start.py", $content);
}
