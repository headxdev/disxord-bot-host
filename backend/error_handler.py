#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Manager - Enhanced Error Handler
Comprehensive error handling and reporting system.

@author headx & the psychon
@version 2.0
"""

import sys
import logging
import traceback
import json
from datetime import datetime
from typing import Dict, Any, Optional, Union
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Ensure logs directory exists
log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

# Configure enhanced logging
def setup_logging():
    """Set up comprehensive logging configuration."""
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)8s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / 'errors.log',
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

class ErrorCode:
    """Error codes for the application."""
    BOT_NOT_FOUND = "BOT_NOT_FOUND"
    BOT_ALREADY_RUNNING = "BOT_ALREADY_RUNNING"
    BOT_NOT_RUNNING = "BOT_NOT_RUNNING"
    INVALID_TOKEN = "INVALID_TOKEN"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    INVALID_CONFIG = "INVALID_CONFIG"
    NETWORK_ERROR = "NETWORK_ERROR"
    DISCORD_API_ERROR = "DISCORD_API_ERROR"
    ENVIRONMENT_ERROR = "ENVIRONMENT_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"

class BotManagerError(Exception):
    """Base exception class for bot manager errors."""
    def __init__(
        self,
        code: str,
        message: str,
        details: Optional[str] = None,
        suggestion: Optional[str] = None
    ):
        self.code = code
        self.message = message
        self.details = details
        self.suggestion = suggestion
        super().__init__(message)

class ErrorHandler:
    """Handles errors in the bot manager application."""
    
    def __init__(self):
        self.error_log_path = Path('logs/errors.log')
        self.error_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Handle any error in the application and return a formatted response.
        
        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred
            
        Returns:
            Dict containing error details formatted for the frontend
        """
        error_info = {
            "success": False,
            "code": ErrorCode.UNKNOWN_ERROR,
            "message": str(error),
            "details": None,
            "suggestion": None,
            "timestamp": logging.Formatter.formatTime(logging.Formatter(), None),
            "context": context
        }

        if isinstance(error, BotManagerError):
            error_info.update({
                "code": error.code,
                "message": error.message,
                "details": error.details,
                "suggestion": error.suggestion
            })
        elif isinstance(error, FileNotFoundError):
            error_info.update({
                "code": ErrorCode.FILE_NOT_FOUND,
                "message": "Die angeforderte Datei wurde nicht gefunden",
                "suggestion": "Überprüfen Sie den Dateipfad und stellen Sie sicher, dass die Datei existiert"
            })
        elif isinstance(error, PermissionError):
            error_info.update({
                "code": ErrorCode.PERMISSION_DENIED,
                "message": "Keine Berechtigung für diese Operation",
                "suggestion": "Überprüfen Sie die Dateiberechtigungen und Zugriffsrechte"
            })
        elif "discord.errors.Forbidden" in str(type(error)):
            error_info.update({
                "code": ErrorCode.DISCORD_API_ERROR,
                "message": "Discord API Fehler: Keine Berechtigung",
                "suggestion": "Überprüfen Sie die Bot-Berechtigungen und Token"
            })
        elif "discord.errors.InvalidToken" in str(type(error)):
            error_info.update({
                "code": ErrorCode.INVALID_TOKEN,
                "message": "Ungültiger Discord Bot Token",
                "suggestion": "Überprüfen Sie den Bot-Token in den Einstellungen"
            })

        # Log the error
        self._log_error(error_info, error)
        
        return error_info

    def _log_error(self, error_info: Dict[str, Any], error: Exception) -> None:
        """Log error details to file and console."""
        error_message = (
            f"\n{'='*50}\n"
            f"Error occurred at {error_info['timestamp']}\n"
            f"Code: {error_info['code']}\n"
            f"Message: {error_info['message']}\n"
            f"Context: {error_info['context']}\n"
        )
        
        if error_info['details']:
            error_message += f"Details: {error_info['details']}\n"
        
        if error_info['suggestion']:
            error_message += f"Suggestion: {error_info['suggestion']}\n"
        
        error_message += f"\nStack Trace:\n{traceback.format_exc()}\n{'='*50}\n"
        
        logger.error(error_message)

    def create_bot_error(
        self,
        code: str,
        message: str,
        details: Optional[str] = None,
        suggestion: Optional[str] = None
    ) -> BotManagerError:
        """Create a new BotManagerError with the given parameters."""
        return BotManagerError(code, message, details, suggestion)

# Global error handler instance
error_handler = ErrorHandler()