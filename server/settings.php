<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$settingsFile = '../data/settings.json';

// Create settings file if it doesn't exist
if (!file_exists($settingsFile)) {
    $defaultSettings = [
        'server' => [
            'port' => 8000,
            'host' => '0.0.0.0',
            'debug' => false,
            'logLevel' => 'info',
            'maxLogFiles' => 10,
            'maxLogSize' => 10485760, // 10MB
            'autoStartBots' => false,
            'checkInterval' => 30
        ],
        'bots' => [
            'defaultPrefix' => '!',
            'autoRestart' => true,
            'maxRestartAttempts' => 3,
            'restartDelay' => 5,
            'logRetentionDays' => 7,
            'defaultPermissions' => [
                'administrator' => false,
                'sendMessages' => true,
                'readMessages' => true,
                'embedLinks' => true
            ]
        ],
        'security' => [
            'tokenEncryption' => true,
            'rateLimiting' => true,
            'maxRequestsPerMinute' => 60,
            'allowedOrigins' => ['localhost', '127.0.0.1']
        ],
        'ui' => [
            'theme' => 'dark',
            'language' => 'de',
            'animations' => true,
            'compactMode' => false,
            'showAdvancedOptions' => false
        ]
    ];
    
    file_put_contents($settingsFile, json_encode($defaultSettings, JSON_PRETTY_PRINT));
}

function getSettings() {
    global $settingsFile;
    return json_decode(file_get_contents($settingsFile), true);
}

function updateSettings($newSettings) {
    global $settingsFile;
    $currentSettings = getSettings();
    $updatedSettings = array_merge_recursive($currentSettings, $newSettings);
    file_put_contents($settingsFile, json_encode($updatedSettings, JSON_PRETTY_PRINT));
    return $updatedSettings;
}

$action = $_GET['action'] ?? '';
$response = ['success' => false, 'message' => 'Invalid action'];

switch ($action) {
    case 'get':
        $response = [
            'success' => true,
            'settings' => getSettings()
        ];
        break;
        
    case 'update':
        $data = json_decode(file_get_contents('php://input'), true);
        if ($data) {
            $response = [
                'success' => true,
                'settings' => updateSettings($data)
            ];
        } else {
            $response = [
                'success' => false,
                'message' => 'Invalid settings data'
            ];
        }
        break;
        
    default:
        $response = [
            'success' => false,
            'message' => 'Invalid action'
        ];
}

echo json_encode($response);
