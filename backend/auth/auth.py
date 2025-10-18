#!/usr/bin/env python3
"""
Discord OAuth2 Authentication System
Created by headx & the psychon
"""

import os
import json
import time
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import urllib.parse
import urllib.request

class DiscordAuth:
    """Discord OAuth2 authentication handler"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.data_dir = self.base_dir / 'data'
        self.users_file = self.data_dir / 'users.json'
        self.sessions_file = self.data_dir / 'sessions.json'
        
        # Discord OAuth2 Configuration
        self.client_id = os.getenv('DISCORD_CLIENT_ID', '')
        self.client_secret = os.getenv('DISCORD_CLIENT_SECRET', '')
        self.redirect_uri = os.getenv('DISCORD_REDIRECT_URI', 'http://localhost:8000/auth/callback')
        
        self.data_dir.mkdir(exist_ok=True)
        self._load_data()
    
    def _load_data(self):
        """Load user and session data"""
        if self.users_file.exists():
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {}
        
        if self.sessions_file.exists():
            with open(self.sessions_file, 'r', encoding='utf-8') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = {}
    
    def _save_data(self):
        """Save user and session data"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=2)
        
        with open(self.sessions_file, 'w', encoding='utf-8') as f:
            json.dump(self.sessions, f, indent=2)
    
    def generate_auth_url(self, state: Optional[str] = None) -> str:
        """Generate Discord OAuth2 authorization URL"""
        if not state:
            state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'identify email guilds applications.commands.permissions.update',
            'state': state
        }
        
        return f"https://discord.com/api/oauth2/authorize?{urllib.parse.urlencode(params)}"
    
    def exchange_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Exchange authorization code for access token"""
        data = urllib.parse.urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }).encode()
        
        try:
            req = urllib.request.Request(
                'https://discord.com/api/oauth2/token',
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error exchanging code: {e}")
            return None
    
    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Get user information from Discord API"""
        try:
            req = urllib.request.Request(
                'https://discord.com/api/users/@me',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def get_user_guilds(self, access_token: str) -> Optional[list]:
        """Get user's Discord guilds"""
        try:
            req = urllib.request.Request(
                'https://discord.com/api/users/@me/guilds',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error getting guilds: {e}")
            return None
    
    def get_user_applications(self, access_token: str) -> Optional[list]:
        """Get user's Discord applications (bots)"""
        try:
            req = urllib.request.Request(
                'https://discord.com/api/oauth2/applications/@me',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            with urllib.request.urlopen(req) as response:
                apps = json.loads(response.read().decode())
                return apps if isinstance(apps, list) else [apps]
        except Exception as e:
            print(f"Error getting applications: {e}")
            return None
    
    def create_session(self, user_id: str, user_data: Dict[str, Any], 
                      token_data: Dict[str, Any]) -> str:
        """Create user session"""
        session_id = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'access_token': token_data.get('access_token'),
            'refresh_token': token_data.get('refresh_token'),
            'token_expires_at': (datetime.now() + 
                               timedelta(seconds=token_data.get('expires_in', 604800))).isoformat()
        }
        
        # Save user data
        self.users[user_id] = {
            'id': user_data.get('id'),
            'username': user_data.get('username'),
            'discriminator': user_data.get('discriminator'),
            'email': user_data.get('email'),
            'avatar': user_data.get('avatar'),
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat()
        }
        
        self._save_data()
        return session_id
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate session and return user data"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            del self.sessions[session_id]
            self._save_data()
            return None
        
        user_id = session['user_id']
        if user_id not in self.users:
            return None
        
        return {
            'session': session,
            'user': self.users[user_id]
        }
    
    def refresh_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token"""
        data = urllib.parse.urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }).encode()
        
        try:
            req = urllib.request.Request(
                'https://discord.com/api/oauth2/token',
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error refreshing token: {e}")
            return None
    
    def logout(self, session_id: str) -> bool:
        """Logout user and invalidate session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            self._save_data()
            return True
        return False
    
    def get_bot_token(self, application_id: str, access_token: str) -> Optional[str]:
        """Get bot token for application (if possible)"""
        try:
            req = urllib.request.Request(
                f'https://discord.com/api/applications/{application_id}/bot',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                return data.get('token')
        except Exception as e:
            print(f"Error getting bot token: {e}")
            return None

# Global auth instance
auth = DiscordAuth()
