<?php

class ErrorHandler {
    private static $errorLogPath = '../logs/server_errors.log';
    
    private static $errorCodes = [
        'INVALID_REQUEST' => [
            'httpCode' => 400,
            'message' => 'Ungültige Anfrage'
        ],
        'BOT_NOT_FOUND' => [
            'httpCode' => 404,
            'message' => 'Bot nicht gefunden'
        ],
        'INVALID_TOKEN' => [
            'httpCode' => 401,
            'message' => 'Ungültiger Bot-Token'
        ],
        'PROCESS_ERROR' => [
            'httpCode' => 500,
            'message' => 'Fehler beim Bot-Prozess'
        ],
        'FILE_ERROR' => [
            'httpCode' => 500,
            'message' => 'Dateisystem-Fehler'
        ],
        'PERMISSION_ERROR' => [
            'httpCode' => 403,
            'message' => 'Keine Berechtigung'
        ]
    ];
    
    public static function handleError($code, $message = null, $details = null, $suggestion = null) {
        $error = self::$errorCodes[$code] ?? [
            'httpCode' => 500,
            'message' => 'Unbekannter Fehler'
        ];
        
        $response = [
            'success' => false,
            'code' => $code,
            'message' => $message ?? $error['message'],
            'details' => $details,
            'suggestion' => $suggestion,
            'timestamp' => date('Y-m-d H:i:s')
        ];
        
        // Log error
        self::logError($response);
        
        // Set HTTP response code
        http_response_code($error['httpCode']);
        
        return $response;
    }
    
    public static function logError($errorData) {
        $logEntry = sprintf(
            "[%s] %s\nCode: %s\nMessage: %s\nDetails: %s\nSuggestion: %s\n%s\n",
            $errorData['timestamp'],
            str_repeat('=', 50),
            $errorData['code'],
            $errorData['message'],
            $errorData['details'] ?? 'N/A',
            $errorData['suggestion'] ?? 'N/A',
            str_repeat('=', 50)
        );
        
        $logDir = dirname(self::$errorLogPath);
        if (!is_dir($logDir)) {
            mkdir($logDir, 0755, true);
        }
        
        file_put_contents(self::$errorLogPath, $logEntry, FILE_APPEND);
    }
    
    public static function getBotError($action, $botId = null) {
        switch ($action) {
            case 'start':
                return self::handleError(
                    'PROCESS_ERROR',
                    'Fehler beim Starten des Bots',
                    $botId ? "Bot ID: $botId" : null,
                    'Überprüfen Sie die Bot-Konfiguration und Berechtigungen'
                );
            
            case 'stop':
                return self::handleError(
                    'PROCESS_ERROR',
                    'Fehler beim Stoppen des Bots',
                    $botId ? "Bot ID: $botId" : null,
                    'Der Bot-Prozess reagiert möglicherweise nicht'
                );
            
            case 'status':
                return self::handleError(
                    'BOT_NOT_FOUND',
                    'Bot-Status konnte nicht abgerufen werden',
                    $botId ? "Bot ID: $botId" : null,
                    'Stellen Sie sicher, dass der Bot existiert und korrekt konfiguriert ist'
                );
            
            case 'logs':
                return self::handleError(
                    'FILE_ERROR',
                    'Fehler beim Laden der Logs',
                    $botId ? "Bot ID: $botId" : null,
                    'Überprüfen Sie die Log-Dateiberechtigungen'
                );
            
            default:
                return self::handleError(
                    'INVALID_REQUEST',
                    'Ungültige Aktion',
                    "Aktion: $action",
                    'Verwenden Sie eine gültige Aktion (start, stop, status, logs)'
                );
        }
    }
}