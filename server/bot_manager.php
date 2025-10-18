<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

function writeLog($message, $level = 'INFO') {
    $logDir = __DIR__ . '/../logs';
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
    }
    
    $date = date('Y-m-d H:i:s');
    $logFile = $logDir . '/server-' . date('Y-m-d') . '.log';
    $logMessage = "[$date] [$level] $message\n";
    
    file_put_contents($logFile, $logMessage, FILE_APPEND);
}

function startBot($botId) {
    $botsFile = __DIR__ . '/../data/bots.json';
    if (!file_exists($botsFile)) {
        writeLog("Bots configuration not found", "ERROR");
        return ['success' => false, 'message' => 'Bots configuration not found'];
    }
    
    $bots = json_decode(file_get_contents($botsFile), true);
    $bot = null;
    foreach ($bots as &$b) {
        if ($b['id'] === $botId) {
            $bot = &$b;
            break;
        }
    }
    
    if (!$bot) {
        writeLog("Bot not found: $botId", "ERROR");
        return ['success' => false, 'message' => 'Bot not found'];
    }
    
    // Create bot directory if it doesn't exist
    $botDir = __DIR__ . '/../bots/' . $bot['folder'];
    if (!is_dir($botDir)) {
        mkdir($botDir, 0755, true);
        writeLog("Created bot directory: {$bot['folder']}");
    }
    
    // Create Python virtual environment if it doesn't exist
    $venvDir = $botDir . '/venv';
    if (!is_dir($venvDir)) {
        $cmd = PHP_OS === 'WINNT' 
            ? "python -m venv \"$venvDir\""
            : "python3 -m venv \"$venvDir\"";
        
        exec($cmd, $output, $returnVar);
        
        if ($returnVar !== 0) {
            writeLog("Failed to create virtual environment", "ERROR");
            return ['success' => false, 'message' => 'Failed to create virtual environment'];
        }
        
        writeLog("Created virtual environment for bot: {$bot['name']}");
    }
    
    // Install dependencies
    $pipCmd = PHP_OS === 'WINNT'
        ? "\"$venvDir\\Scripts\\pip\" install -r \"$botDir/requirements.txt\""
        : "\"$venvDir/bin/pip\" install -r \"$botDir/requirements.txt\"";
    
    exec($pipCmd, $output, $returnVar);
    
    if ($returnVar !== 0) {
        writeLog("Failed to install dependencies", "ERROR");
        return ['success' => false, 'message' => 'Failed to install dependencies'];
    }
    
    // Create or update .env file
    $envContent = "DISCORD_TOKEN={$bot['token']}\n" .
                 "COMMAND_PREFIX={$bot['prefix']}\n" .
                 "CLIENT_ID={$bot['clientId']}\n" .
                 "BOT_NAME={$bot['name']}\n" .
                 "DEBUG=" . ($bot['settings']['debug'] ? 'true' : 'false') . "\n";
    
    file_put_contents($botDir . '/.env', $envContent);
    
    // Start the bot process
    $pythonCmd = PHP_OS === 'WINNT'
        ? "\"$venvDir\\Scripts\\python\""
        : "\"$venvDir/bin/python\"";
    
    $logFile = $botDir . '/logs/bot-' . date('Y-m-d_H-i-s') . '.log';
    $startCmd = PHP_OS === 'WINNT'
        ? "start /B $pythonCmd \"$botDir/{$bot['start']}\" > \"$logFile\" 2>&1"
        : "$pythonCmd \"$botDir/{$bot['start']}\" > \"$logFile\" 2>&1 &";
    
    if (PHP_OS === 'WINNT') {
        pclose(popen($startCmd, 'r'));
        // Get process ID on Windows
        $wmic = shell_exec('wmic process where "CommandLine like \'%' . $bot['start'] . '%\'" get ProcessId');
        preg_match('/(\d+)/', $wmic, $matches);
        $pid = $matches[1] ?? null;
    } else {
        exec($startCmd . ' echo $!', $output);
        $pid = $output[0] ?? null;
    }
    
    if ($pid) {
        $bot['status'] = 'online';
        $bot['processId'] = $pid;
        $bot['lastUpdated'] = date('c');
        $bot['currentLog'] = $logFile;
        
        file_put_contents($botsFile, json_encode($bots, JSON_PRETTY_PRINT));
        writeLog("Bot started successfully: {$bot['name']} (PID: $pid)");
        
        return [
            'success' => true,
            'message' => 'Bot started',
            'pid' => $pid,
            'logFile' => $logFile
        ];
    }
    
    writeLog("Failed to start bot: {$bot['name']}", "ERROR");
    return ['success' => false, 'message' => 'Failed to start bot'];
}

function stopBot($botId) {
    $botsFile = __DIR__ . '/../data/bots.json';
    if (!file_exists($botsFile)) {
        writeLog("Bots configuration not found", "ERROR");
        return ['success' => false, 'message' => 'Bots configuration not found'];
    }
    
    $bots = json_decode(file_get_contents($botsFile), true);
    $bot = null;
    foreach ($bots as &$b) {
        if ($b['id'] === $botId) {
            $bot = &$b;
            break;
        }
    }
    
    if (!$bot) {
        writeLog("Bot not found: $botId", "ERROR");
        return ['success' => false, 'message' => 'Bot not found'];
    }
    
    if (isset($bot['processId'])) {
        if (PHP_OS === 'WINNT') {
            exec("taskkill /F /PID {$bot['processId']} 2>nul");
        } else {
            exec("kill -15 {$bot['processId']} 2>/dev/null || kill -9 {$bot['processId']} 2>/dev/null");
        }
        
        $bot['status'] = 'offline';
        $bot['processId'] = null;
        $bot['lastUpdated'] = date('c');
        
        file_put_contents($botsFile, json_encode($bots, JSON_PRETTY_PRINT));
        writeLog("Bot stopped: {$bot['name']}");
        
        return ['success' => true, 'message' => 'Bot stopped'];
    }
    
    writeLog("Bot process not found: {$bot['name']}", "WARNING");
    return ['success' => false, 'message' => 'Bot process not found'];
}

function getBotStatus($botId) {
    $botsFile = __DIR__ . '/../data/bots.json';
    if (!file_exists($botsFile)) {
        return ['success' => false, 'message' => 'Bots configuration not found'];
    }
    
    $bots = json_decode(file_get_contents($botsFile), true);
    foreach ($bots as $bot) {
        if ($bot['id'] === $botId) {
            if (isset($bot['processId'])) {
                $running = false;
                
                if (PHP_OS === 'WINNT') {
                    exec("tasklist /FI \"PID eq {$bot['processId']}\" 2>nul", $output);
                    $running = count($output) > 1;
                } else {
                    exec("ps -p {$bot['processId']} -o pid=", $output);
                    $running = !empty($output);
                }
                
                return [
                    'success' => true,
                    'status' => $running ? 'online' : 'offline',
                    'lastUpdated' => $bot['lastUpdated'] ?? null,
                    'currentLog' => $bot['currentLog'] ?? null
                ];
            }
            return ['success' => true, 'status' => $bot['status'] ?? 'offline'];
        }
    }
    
    return ['success' => false, 'message' => 'Bot not found'];
}

function getLogs($botId, $limit = 100) {
    $botsFile = __DIR__ . '/../data/bots.json';
    if (!file_exists($botsFile)) {
        return ['success' => false, 'message' => 'Bots configuration not found'];
    }
    
    $bots = json_decode(file_get_contents($botsFile), true);
    $bot = null;
    foreach ($bots as $b) {
        if ($b['id'] === $botId) {
            $bot = $b;
            break;
        }
    }
    
    if (!$bot) {
        return ['success' => false, 'message' => 'Bot not found'];
    }
    
    $logDir = __DIR__ . '/../bots/' . $bot['folder'] . '/logs';
    if (!is_dir($logDir)) {
        mkdir($logDir, 0755, true);
        writeLog("Created logs directory for bot: {$bot['name']}");
        return ['success' => true, 'logs' => []];
    }
    
    // Get the requested log file if specified
    $requestedFile = $_GET['file'] ?? null;
    if ($requestedFile) {
        $logFile = realpath($requestedFile);
        if ($logFile === false || strpos($logFile, $logDir) !== 0) {
            return ['success' => false, 'message' => 'Invalid log file'];
        }
        
        $content = tailFile($logFile, $limit);
        
        return ['success' => true, 'logs' => [
            [
                'file' => basename($logFile),
                'path' => $logFile,
                'date' => date('Y-m-d H:i:s', filemtime($logFile)),
                'size' => filesize($logFile),
                'content' => $content,
                'isCurrent' => $logFile === ($bot['currentLog'] ?? null)
            ]
        ]];
    }
    
    $logs = [];
    $currentLog = $bot['currentLog'] ?? null;
    
    foreach (scandir($logDir) as $file) {
        if ($file === '.' || $file === '..') continue;
        
        $logFile = "$logDir/$file";
        if (!is_file($logFile)) continue;
        
        $content = tailFile($logFile, $limit);
        
        $logs[] = [
            'file' => $file,
            'path' => $logFile,
            'date' => date('Y-m-d H:i:s', filemtime($logFile)),
            'size' => filesize($logFile),
            'content' => $content,
            'isCurrent' => $logFile === $currentLog
        ];
    }
    
    // Sort logs by date (newest first)
    usort($logs, function($a, $b) {
        return strcmp($b['date'], $a['date']);
    });
    
    return ['success' => true, 'logs' => $logs];
}

function tailFile($file, $lines = 100) {
    if (!file_exists($file)) return '';
    
    $handle = fopen($file, "r");
    if (!$handle) return '';
    
    $linecounter = $lines;
    $pos = -2;
    $beginning = false;
    $text = [];
    
    while ($linecounter > 0) {
        $t = " ";
        while ($t != "\n") {
            if(fseek($handle, $pos, SEEK_END) == -1) {
                $beginning = true;
                break;
            }
            $t = fgetc($handle);
            $pos--;
        }
        
        $linecounter--;
        if ($beginning) {
            rewind($handle);
        }
        
        $text[$lines - $linecounter - 1] = fgets($handle);
        
        if ($beginning) break;
    }
    
    fclose($handle);
    return implode('', array_reverse($text));
}

function downloadLog($file) {
    if (!file_exists($file)) {
        return ['success' => false, 'message' => 'Log file not found'];
    }
    
    // Validate file is in logs directory
    $realPath = realpath($file);
    $logsDir = realpath(__DIR__ . '/../bots');
    if ($realPath === false || strpos($realPath, $logsDir) !== 0) {
        return ['success' => false, 'message' => 'Invalid log file'];
    }
    
    $fileName = basename($file);
    header('Content-Type: text/plain');
    header('Content-Disposition: attachment; filename="' . $fileName . '"');
    header('Content-Length: ' . filesize($file));
    readfile($file);
    exit;
}

function clearLog($botId, $logPath) {
    $botsFile = __DIR__ . '/../data/bots.json';
    if (!file_exists($botsFile)) {
        return ['success' => false, 'message' => 'Bots configuration not found'];
    }
    
    $bots = json_decode(file_get_contents($botsFile), true);
    $bot = null;
    foreach ($bots as $b) {
        if ($b['id'] === $botId) {
            $bot = $b;
            break;
        }
    }
    
    if (!$bot) {
        return ['success' => false, 'message' => 'Bot not found'];
    }
    
    // Validate log file path
    $realPath = realpath($logPath);
    $logDir = realpath(__DIR__ . '/../bots/' . $bot['folder'] . '/logs');
    if ($realPath === false || strpos($realPath, $logDir) !== 0) {
        return ['success' => false, 'message' => 'Invalid log file'];
    }
    
    if (file_exists($logPath)) {
        if ($bot['currentLog'] === $logPath) {
            // For current log, truncate instead of delete
            file_put_contents($logPath, '');
            writeLog("Cleared current log file for bot: {$bot['name']}");
        } else {
            unlink($logPath);
            writeLog("Deleted old log file for bot: {$bot['name']}");
        }
        return ['success' => true, 'message' => 'Log cleared'];
    }
    
    return ['success' => false, 'message' => 'Log file not found'];
}

$action = $_GET['action'] ?? '';
$response = ['success' => false, 'message' => 'Invalid action'];

switch ($action) {
    case 'start':
        $botId = $_POST['botId'] ?? null;
        if (!$botId) {
            $response = ['success' => false, 'message' => 'Bot ID required'];
            break;
        }
        $response = startBot($botId);
        break;
        
    case 'stop':
        $botId = $_POST['botId'] ?? null;
        if (!$botId) {
            $response = ['success' => false, 'message' => 'Bot ID required'];
            break;
        }
        $response = stopBot($botId);
        break;
        
    case 'status':
        $botId = $_GET['botId'] ?? null;
        if (!$botId) {
            $response = ['success' => false, 'message' => 'Bot ID required'];
            break;
        }
        $response = getBotStatus($botId);
        break;
        
    case 'logs':
        $botId = $_GET['botId'] ?? null;
        $limit = $_GET['limit'] ?? 100;
        if (!$botId) {
            $response = ['success' => false, 'message' => 'Bot ID required'];
            break;
        }
        $response = getLogs($botId, $limit);
        break;
        
    case 'download':
        $file = $_GET['file'] ?? null;
        if (!$file) {
            $response = ['success' => false, 'message' => 'File path required'];
            break;
        }
        downloadLog($file);
        break;
        
    case 'clear_log':
        $botId = $_POST['botId'] ?? null;
        $logPath = $_POST['logPath'] ?? null;
        if (!$botId || !$logPath) {
            $response = ['success' => false, 'message' => 'Bot ID and log path required'];
            break;
        }
        $response = clearLog($botId, $logPath);
        break;
}

echo json_encode($response);
