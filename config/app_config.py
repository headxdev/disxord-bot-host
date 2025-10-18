#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Bot Manager - Application Configuration
Centralized configuration management for the application.

@author headx & the psychon
@version 2.0
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ServerConfig:
    """Server configuration settings."""
    host: str = field(default_factory=lambda: os.getenv('HOST', '0.0.0.0'))
    port: int = field(default_factory=lambda: int(os.getenv('PORT', '8000')))
    debug: bool = field(default_factory=lambda: os.getenv('DEBUG', 'False').lower() == 'true')
    enable_https: bool = field(default_factory=lambda: os.getenv('ENABLE_HTTPS', 'False').lower() == 'true')
    ssl_cert_path: Optional[str] = field(default_factory=lambda: os.getenv('SSL_CERT_PATH'))
    ssl_key_path: Optional[str] = field(default_factory=lambda: os.getenv('SSL_KEY_PATH'))
    max_upload_size: int = field(default_factory=lambda: int(os.getenv('MAX_UPLOAD_SIZE', '10485760')))  # 10MB
    cors_enabled: bool = field(default_factory=lambda: os.getenv('CORS_ENABLED', 'True').lower() == 'true')
    cors_origins: str = field(default_factory=lambda: os.getenv('CORS_ORIGINS', '*'))


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    type: str = field(default_factory=lambda: os.getenv('DB_TYPE', 'sqlite'))
    path: str = field(default_factory=lambda: os.getenv('DB_PATH', 'data/bots.db'))
    backup_enabled: bool = field(default_factory=lambda: os.getenv('DB_BACKUP_ENABLED', 'True').lower() == 'true')
    backup_interval: int = field(default_factory=lambda: int(os.getenv('DB_BACKUP_INTERVAL', '3600')))  # 1 hour
    max_backups: int = field(default_factory=lambda: int(os.getenv('DB_MAX_BACKUPS', '24')))


@dataclass
class BotConfig:
    """Bot default configuration settings."""
    default_prefix: str = field(default_factory=lambda: os.getenv('DEFAULT_PREFIX', '!'))
    max_bots_per_user: int = field(default_factory=lambda: int(os.getenv('MAX_BOTS_PER_USER', '10')))
    bot_timeout: int = field(default_factory=lambda: int(os.getenv('BOT_TIMEOUT', '300')))  # 5 minutes
    auto_restart: bool = field(default_factory=lambda: os.getenv('AUTO_RESTART', 'True').lower() == 'true')
    log_retention_days: int = field(default_factory=lambda: int(os.getenv('LOG_RETENTION_DAYS', '30')))
    max_log_size: int = field(default_factory=lambda: int(os.getenv('MAX_LOG_SIZE', '52428800')))  # 50MB


@dataclass
class SecurityConfig:
    """Security configuration settings."""
    secret_key: str = field(default_factory=lambda: os.getenv('SECRET_KEY', os.urandom(32).hex()))
    session_timeout: int = field(default_factory=lambda: int(os.getenv('SESSION_TIMEOUT', '3600')))  # 1 hour
    max_login_attempts: int = field(default_factory=lambda: int(os.getenv('MAX_LOGIN_ATTEMPTS', '5')))
    lockout_duration: int = field(default_factory=lambda: int(os.getenv('LOCKOUT_DURATION', '300')))  # 5 minutes
    password_min_length: int = field(default_factory=lambda: int(os.getenv('PASSWORD_MIN_LENGTH', '8')))
    require_https: bool = field(default_factory=lambda: os.getenv('REQUIRE_HTTPS', 'False').lower() == 'true')
    csrf_enabled: bool = field(default_factory=lambda: os.getenv('CSRF_ENABLED', 'True').lower() == 'true')


@dataclass
class DiscordConfig:
    """Discord OAuth2 configuration settings."""
    client_id: Optional[str] = field(default_factory=lambda: os.getenv('DISCORD_CLIENT_ID'))
    client_secret: Optional[str] = field(default_factory=lambda: os.getenv('DISCORD_CLIENT_SECRET'))
    redirect_uri: str = field(default_factory=lambda: os.getenv('DISCORD_REDIRECT_URI', 'http://localhost:8000/auth/callback'))
    bot_permissions: int = field(default_factory=lambda: int(os.getenv('DISCORD_BOT_PERMISSIONS', '8')))  # Administrator
    oauth_enabled: bool = field(default_factory=lambda: bool(os.getenv('DISCORD_CLIENT_ID') and os.getenv('DISCORD_CLIENT_SECRET')))


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str = field(default_factory=lambda: os.getenv('LOG_LEVEL', 'INFO'))
    format: str = field(default_factory=lambda: os.getenv('LOG_FORMAT', '%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
    file_enabled: bool = field(default_factory=lambda: os.getenv('LOG_FILE_ENABLED', 'True').lower() == 'true')
    file_path: str = field(default_factory=lambda: os.getenv('LOG_FILE_PATH', 'logs/app.log'))
    max_file_size: int = field(default_factory=lambda: int(os.getenv('LOG_MAX_FILE_SIZE', '10485760')))  # 10MB
    backup_count: int = field(default_factory=lambda: int(os.getenv('LOG_BACKUP_COUNT', '5')))
    console_enabled: bool = field(default_factory=lambda: os.getenv('LOG_CONSOLE_ENABLED', 'True').lower() == 'true')


@dataclass
class PerformanceConfig:
    """Performance and optimization settings."""
    cache_enabled: bool = field(default_factory=lambda: os.getenv('CACHE_ENABLED', 'True').lower() == 'true')
    cache_timeout: int = field(default_factory=lambda: int(os.getenv('CACHE_TIMEOUT', '300')))  # 5 minutes
    compression_enabled: bool = field(default_factory=lambda: os.getenv('COMPRESSION_ENABLED', 'True').lower() == 'true')
    minify_css: bool = field(default_factory=lambda: os.getenv('MINIFY_CSS', 'False').lower() == 'true')
    minify_js: bool = field(default_factory=lambda: os.getenv('MINIFY_JS', 'False').lower() == 'true')
    enable_etags: bool = field(default_factory=lambda: os.getenv('ENABLE_ETAGS', 'True').lower() == 'true')


@dataclass
class AppConfig:
    """Main application configuration."""
    server: ServerConfig = field(default_factory=ServerConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    bot: BotConfig = field(default_factory=BotConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    discord: DiscordConfig = field(default_factory=DiscordConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    
    # Application metadata
    name: str = "Discord Bot Manager"
    version: str = "2.0.0"
    description: str = "Professional Discord Bot Management System"
    authors: list = field(default_factory=lambda: ["headx", "the psychon"])
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'AppConfig':
        """Load configuration from JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            return cls()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return cls(**data)
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Warning: Failed to load config from {config_path}: {e}")
            return cls()
    
    def save_to_file(self, config_path: str) -> bool:
        """Save configuration to JSON file."""
        try:
            config_file = Path(config_path)
            config_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert dataclass to dict, excluding functions and private attributes
            config_dict = {}
            for key, value in self.__dict__.items():
                if not key.startswith('_') and not callable(value):
                    if hasattr(value, '__dict__'):
                        config_dict[key] = {k: v for k, v in value.__dict__.items() 
                                          if not k.startswith('_') and not callable(v)}
                    else:
                        config_dict[key] = value
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, default=str)
            
            return True
        except Exception as e:
            print(f"Error: Failed to save config to {config_path}: {e}")
            return False
    
    def validate(self) -> Dict[str, str]:
        """Validate configuration and return any errors."""
        errors = {}
        
        # Validate server configuration
        if self.server.port < 1 or self.server.port > 65535:
            errors['server.port'] = "Port must be between 1 and 65535"
        
        if self.server.enable_https:
            if not self.server.ssl_cert_path or not Path(self.server.ssl_cert_path).exists():
                errors['server.ssl_cert_path'] = "SSL certificate file not found"
            if not self.server.ssl_key_path or not Path(self.server.ssl_key_path).exists():
                errors['server.ssl_key_path'] = "SSL key file not found"
        
        # Validate Discord OAuth2
        if self.discord.oauth_enabled:
            if not self.discord.client_id:
                errors['discord.client_id'] = "Discord client ID is required for OAuth2"
            if not self.discord.client_secret:
                errors['discord.client_secret'] = "Discord client secret is required for OAuth2"
        
        # Validate security settings
        if len(self.security.secret_key) < 32:
            errors['security.secret_key'] = "Secret key must be at least 32 characters long"
        
        if self.security.password_min_length < 8:
            errors['security.password_min_length'] = "Minimum password length should be at least 8"
        
        # Validate bot settings
        if self.bot.max_bots_per_user < 1:
            errors['bot.max_bots_per_user'] = "Max bots per user must be at least 1"
        
        return errors
    
    def get_database_url(self) -> str:
        """Get database connection URL."""
        if self.database.type == 'sqlite':
            return f"sqlite:///{self.database.path}"
        else:
            return self.database.path
    
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.server.debug and self.security.require_https


# Global configuration instance
config = AppConfig()

# Load configuration from file if it exists
config_file_path = Path(__file__).parent.parent / 'config.json'
if config_file_path.exists():
    config = AppConfig.load_from_file(str(config_file_path))

# Validate configuration on import
validation_errors = config.validate()
if validation_errors:
    print("Configuration validation errors:")
    for key, error in validation_errors.items():
        print(f"  - {key}: {error}")