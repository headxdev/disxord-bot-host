# 📁 Discord Bot Manager - Projektstruktur

**Version 2.0** | **Created by headx & the psychon**

## 🗂️ Hauptverzeichnis

```
discord-bot-manager/
│
├── 🐍 Python Backend
│   ├── start.py                 # Hauptserver mit OAuth2
│   ├── auth.py                  # Discord OAuth2 Handler
│   ├── bot_manager.py           # [Deprecated] Bot Management (merged into start.py)
│   ├── setup.py                 # Setup Script
│   └── install.py               # Installation Script
│
├── 🌐 Frontend
│   ├── index.html               # Haupt-Interface
│   ├── script.js                # Core JavaScript
│   ├── auth-handler.js          # OAuth2 Frontend Logic ⭐ NEU
│   ├── styles.css               # Haupt-Styling
│   ├── auth-styles.css          # Auth-Styling ⭐ NEU
│   └── styles-mobile.css        # Mobile Responsive
│
├── 📚 Dokumentation
│   ├── README.md                # Hauptdokumentation (erweitert) ⭐
│   ├── DISCORD_OAUTH_SETUP.md   # OAuth2 Setup Guide ⭐ NEU
│   ├── API.md                   # API Dokumentation ⭐ NEU
│   ├── IMPROVEMENTS.md          # Verbesserungen ⭐ NEU
│   ├── CONTRIBUTING.md          # Contribution Guide ⭐ NEU
│   ├── CHANGELOG.md             # Versionshistorie ⭐ NEU
│   └── PROJECT_STRUCTURE.md     # Diese Datei ⭐ NEU
│
├── 🛠️ Scripts
│   ├── quickstart.sh            # Linux/macOS Quickstart ⭐ NEU
│   ├── quickstart.bat           # Windows Quickstart ⭐ NEU
│   ├── install.sh               # Linux Installation
│   └── install.bat              # Windows Installation
│
├── ⚙️ Konfiguration
│   ├── .env                     # Environment Variables (erweitert) ⭐
│   ├── .gitignore               # Git Ignore Rules ⭐ NEU
│   ├── requirements.txt         # Python Dependencies ⭐ NEU
│   ├── dependencies.json        # Legacy Dependency File
│   └── LICENSE                  # MIT License ⭐ NEU
│
├── 📦 Data & Storage
│   ├── data/                    # User & Session Data
│   │   ├── users.json          # User Accounts ⭐ NEU
│   │   └── sessions.json       # Active Sessions ⭐ NEU
│   │
│   ├── bots/                    # Bot Instances
│   │   ├── bot_1/
│   │   │   ├── main.py
│   │   │   ├── config.json
│   │   │   ├── requirements.txt
│   │   │   ├── .env
│   │   │   ├── cogs/           # Optional Cogs
│   │   │   └── logs/           # Bot Logs
│   │   └── bot_2/
│   │
│   ├── logs/                    # Server Logs
│   │   └── server-YYYY-MM-DD.log
│   │
│   └── cmdtamplates/            # Command Templates
│       ├── api/
│       └── frontend/
│
├── 🔧 Development
│   ├── venv/                    # Python Virtual Environment
│   ├── __pycache__/             # Python Cache
│   └── node_modules/            # (falls npm genutzt wird)
│
└── 🧪 Test & Legacy
    ├── test.py                  # Test Script
    ├── server.php               # Legacy PHP Server
    ├── solar-system.html        # Demo Page
    └── *.new                    # Backup Files
```

## 📄 Datei-Beschreibungen

### 🐍 Python Backend

#### `start.py` ⭐ VERBESSERT
**Hauptserver-Datei mit OAuth2-Integration**
- HTTP Server (ThreadedHTTPServer)
- Discord OAuth2 Authentifizierung
- API Endpoints für User & Applications
- Session Management
- File Serving mit PHP-Support
- Logging System
- ~500 Zeilen Code

**Neue Features:**
- `/auth/login` - OAuth2 URL Generator
- `/auth/callback` - OAuth2 Callback Handler
- `/auth/logout` - User Logout
- `/api/user` - Current User Info
- `/api/discord/applications` - Discord Apps List

#### `auth.py` ⭐ NEU
**Discord OAuth2 Authentication Handler**
- OAuth2 Flow Implementation
- Token Exchange
- User Info Retrieval
- Application List
- Session Management
- Token Refresh
- ~250 Zeilen Code

**Key Features:**
- Secure token storage
- Session expiration (7 days)
- Automatic token refresh
- CSRF protection with state parameter

### 🌐 Frontend

#### `auth-handler.js` ⭐ NEU
**Frontend OAuth2 Integration**
- Authentication Status Check
- Discord Login Flow
- User UI Updates
- Application Loading & Rendering
- Import Bot Functionality
- ~350 Zeilen Code

**Key Functions:**
```javascript
- checkAuthStatus()              // Check if user is logged in
- loginWithDiscord()             // Initiate Discord OAuth2
- logout()                       // Log out user
- loadDiscordApplications()      // Load user's Discord apps
- importDiscordApp()             // Import bot from Discord
- renderDiscordApplications()    // Render apps grid
```

#### `auth-styles.css` ⭐ NEU
**Styling für Auth-Features**
- Header User Info
- Discord Login Button
- Auth Required Card
- Discord Apps Grid
- Import Modal
- Loading States
- ~400 Zeilen CSS

**Design Features:**
- Discord Brand Colors (#5865F2)
- Smooth Animations
- Responsive Design
- Glass Morphism Effects

### 📚 Dokumentation

#### `DISCORD_OAUTH_SETUP.md` ⭐ NEU
**Schritt-für-Schritt OAuth2 Setup**
- Discord Application erstellen
- OAuth2 konfigurieren
- Credentials eintragen
- Troubleshooting
- Security Best Practices

#### `API.md` ⭐ NEU
**Vollständige API-Dokumentation**
- Server Endpoints
- Data Structures
- JavaScript API
- Python API
- Error Handling
- Code Examples

#### `IMPROVEMENTS.md` ⭐ NEU
**Alle Verbesserungen dokumentiert**
- Neue Features
- Code-Qualität
- Performance
- Security
- Developer Experience
- Statistiken

### 🛠️ Scripts

#### `quickstart.sh` / `quickstart.bat` ⭐ NEU
**One-Click Setup & Start**
- Python Version Check
- Virtual Environment Setup
- Dependency Installation
- Directory Creation
- Server Start
- Colored Output

**Usage:**
```bash
# Linux/macOS
./quickstart.sh

# Windows
quickstart.bat
```

### ⚙️ Konfiguration

#### `.env` ⭐ ERWEITERT
**Environment Variables**
```env
# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False
LOG_LEVEL=INFO

# Discord OAuth2 ⭐ NEU
DISCORD_CLIENT_ID=your_id
DISCORD_CLIENT_SECRET=your_secret
DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
```

#### `requirements.txt` ⭐ NEU
**Python Dependencies**
```
discord.py>=2.3.2
python-dotenv>=1.0.0
aiohttp>=3.8.5
PyNaCl>=1.5.0
colorama>=0.4.6
watchdog>=3.0.0
psutil>=5.9.0
```

#### `.gitignore` ⭐ NEU
**Git Ignore Rules**
- Python Cache & Virtual Env
- Environment Files
- Logs & Data
- IDE Files
- OS Files

## 🔄 Datenfluss

### OAuth2 Authentication Flow
```
1. User clicks "Mit Discord anmelden"
   └─> Frontend: auth-handler.js → loginWithDiscord()

2. Server generates OAuth2 URL
   └─> Backend: start.py → /auth/login

3. User authorizes on Discord
   └─> Discord redirects to /auth/callback

4. Server exchanges code for token
   └─> Backend: auth.py → exchange_code()

5. Server creates user session
   └─> Backend: auth.py → create_session()

6. User is redirected to homepage
   └─> Frontend shows user info & Discord apps
```

### Bot Import Flow
```
1. User sees Discord applications
   └─> Frontend: auth-handler.js → loadDiscordApplications()

2. User clicks "Importieren"
   └─> Frontend: auth-handler.js → importDiscordApp()

3. Token input modal appears
   └─> Frontend: auth-handler.js → promptForBotToken()

4. Bot is created with Discord data
   └─> Frontend: script.js → generateBotFiles()

5. Bot appears in overview
   └─> Frontend: script.js → renderBots()
```

## 📊 Codebase-Statistiken

### Lines of Code
- **Python**: ~1,500 lines
  - start.py: ~500
  - auth.py: ~250
  - Others: ~750

- **JavaScript**: ~4,000 lines
  - script.js: ~3,500
  - auth-handler.js: ~350
  - Others: ~150

- **CSS**: ~2,500 lines
  - styles.css: ~2,000
  - auth-styles.css: ~400
  - Others: ~100

- **Documentation**: ~3,500 lines
  - Markdown files: ~3,000
  - Comments: ~500

**Total: ~11,500 lines of code**

### File Count
- **Python Files**: 4 (3 active + 1 deprecated)
- **JavaScript Files**: 3
- **CSS Files**: 3
- **HTML Files**: 2
- **Documentation**: 9
- **Scripts**: 4
- **Config Files**: 5

**Total: 30+ files**

## 🎯 Features-Übersicht

### Core Features (v1.0)
- ✅ Bot Creation & Management
- ✅ Code Editor
- ✅ Command Templates
- ✅ Bot Process Control
- ✅ Export/Import
- ✅ Logging System

### New Features (v2.0)
- ⭐ Discord OAuth2 Login
- ⭐ Auto-Import Discord Bots
- ⭐ User Session Management
- ⭐ Discord Apps Tab
- ⭐ Enhanced Documentation
- ⭐ Quickstart Scripts

### Planned Features (v2.x)
- 🔜 Real-time Bot Status
- 🔜 WebSocket Logs
- 🔜 Performance Metrics
- 🔜 Multi-Language Support
- 🔜 Theme Customization

## 🔐 Security Features

### Authentication
- ✅ OAuth2 Standard
- ✅ CSRF Protection (State Parameter)
- ✅ HttpOnly Cookies
- ✅ Session Expiration
- ✅ Token Refresh

### Data Protection
- ✅ Local Token Storage
- ✅ Environment Variables
- ✅ .gitignore Protection
- ✅ No Hardcoded Credentials
- ✅ Input Validation

## 📱 Responsive Design

### Breakpoints
- **Desktop**: > 1200px
- **Tablet**: 768px - 1199px
- **Mobile**: < 767px

### Mobile Features
- ✅ Hamburger Menu
- ✅ Touch-Friendly Buttons
- ✅ Swipe Gestures
- ✅ Optimized Layout
- ✅ Fast Loading

## 🚀 Performance

### Frontend
- ⚡ Lazy Loading
- ⚡ Cached Responses
- ⚡ Optimized Rendering
- ⚡ Minified Assets

### Backend
- ⚡ Threaded Server
- ⚡ Session Caching
- ⚡ Efficient File I/O
- ⚡ Connection Pooling

## 🛠️ Development Setup

### Prerequisites
```bash
- Python 3.8+
- pip
- Git
- Modern Browser
```

### Quick Setup
```bash
# Clone
git clone https://github.com/youruser/discord-bot-manager.git
cd discord-bot-manager

# Run quickstart
./quickstart.sh  # Linux/macOS
quickstart.bat   # Windows
```

### Manual Setup
```bash
# Virtual Environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install Dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your credentials

# Run
python start.py
```

## 📈 Roadmap

### Version 2.1 (Q2 2024)
- Bot Status Sync
- WebSocket Logs
- Performance Dashboard
- Command Statistics

### Version 2.2 (Q3 2024)
- Theme Builder
- Bot Marketplace
- Cloud Sync
- Collaboration Tools

### Version 3.0 (Q4 2024)
- Docker Support
- Kubernetes
- Auto-Scaling
- Enterprise Features

## 🎉 Changelog Summary

### v2.0.0 (Aktuell)
- ⭐ Discord OAuth2 Integration
- ⭐ Auto Bot Import
- ⭐ Enhanced UI/UX
- ⭐ Comprehensive Documentation
- ⭐ Quickstart Scripts
- 🐛 Bug Fixes

### v1.0.0 (Initial)
- 🎨 Cosmic Theme
- 🤖 Bot Management
- 📝 Code Editor
- ⚡ Templates
- 🔄 Process Control

---

**This project is constantly evolving!**

**Developed with ❤️ by headx & the psychon**

├───backend
│   ├───api
│   ├───auth
│   ├───cmdtemplates
│   │   ├───api
│   │   └───frontend
│   └───data
│       └───logs
├───bots
│   └───testbot
│       ├───cogs
│       ├───commands
│       ├───events
│       ├───infos
│       └───logs
├───cmdtamplates
│   ├───api
│   └───frontend
├───data
├───docs
├───frontend
├───logs
├───manager
├───server
│   └───flask_app
│       ├───venv
│       │   ├───bin
│       │   ├───include
│       │   │   └───python3.12
│       │   ├───lib
│       │   │   └───python3.12
│       │   │       └───site-packages
│       │   │           ├───pip
│       │   │           │   ├───_internal
│       │   │           │   │   ├───cli
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───commands
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───distributions
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───index
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───locations
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───metadata
│       │   │           │   │   │   ├───importlib
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───models
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───network
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───operations
│       │   │           │   │   │   ├───build
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───install
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───req
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───resolution
│       │   │           │   │   │   ├───legacy
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───resolvelib
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───utils
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───vcs
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   └───__pycache__
│       │   │           │   ├───_vendor
│       │   │           │   │   ├───cachecontrol
│       │   │           │   │   │   ├───caches
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───certifi
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───chardet
│       │   │           │   │   │   ├───cli
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───metadata
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───colorama
│       │   │           │   │   │   ├───tests
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───distlib
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───distro
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───idna
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───msgpack
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───packaging
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───pkg_resources
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───platformdirs
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───pygments
│       │   │           │   │   │   ├───filters
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───formatters
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───lexers
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───styles
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───pyparsing
│       │   │           │   │   │   ├───diagram
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───pyproject_hooks
│       │   │           │   │   │   ├───_in_process
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───requests
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───resolvelib
│       │   │           │   │   │   ├───compat
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───rich
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───tenacity
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───tomli
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───truststore
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───urllib3
│       │   │           │   │   │   ├───contrib
│       │   │           │   │   │   │   ├───_securetransport
│       │   │           │   │   │   │   │   └───__pycache__
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───packages
│       │   │           │   │   │   │   ├───backports
│       │   │           │   │   │   │   │   └───__pycache__
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   ├───util
│       │   │           │   │   │   │   └───__pycache__
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   ├───webencodings
│       │   │           │   │   │   └───__pycache__
│       │   │           │   │   └───__pycache__
│       │   │           │   └───__pycache__
│       │   │           └───pip-24.0.dist-info
│       │   └───lib64
│       │       └───python3.12
│       │           └───site-packages
│       │               ├───pip
│       │               │   ├───_internal
│       │               │   │   ├───cli
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───commands
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───distributions
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───index
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───locations
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───metadata
│       │               │   │   │   ├───importlib
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───models
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───network
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───operations
│       │               │   │   │   ├───build
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───install
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───req
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───resolution
│       │               │   │   │   ├───legacy
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───resolvelib
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───utils
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───vcs
│       │               │   │   │   └───__pycache__
│       │               │   │   └───__pycache__
│       │               │   ├───_vendor
│       │               │   │   ├───cachecontrol
│       │               │   │   │   ├───caches
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───certifi
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───chardet
│       │               │   │   │   ├───cli
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───metadata
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───colorama
│       │               │   │   │   ├───tests
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───distlib
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───distro
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───idna
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───msgpack
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───packaging
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───pkg_resources
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───platformdirs
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───pygments
│       │               │   │   │   ├───filters
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───formatters
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───lexers
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───styles
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───pyparsing
│       │               │   │   │   ├───diagram
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───pyproject_hooks
│       │               │   │   │   ├───_in_process
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───requests
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───resolvelib
│       │               │   │   │   ├───compat
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───rich
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───tenacity
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───tomli
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───truststore
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───urllib3
│       │               │   │   │   ├───contrib
│       │               │   │   │   │   ├───_securetransport
│       │               │   │   │   │   │   └───__pycache__
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───packages
│       │               │   │   │   │   ├───backports
│       │               │   │   │   │   │   └───__pycache__
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   ├───util
│       │               │   │   │   │   └───__pycache__
│       │               │   │   │   └───__pycache__
│       │               │   │   ├───webencodings
│       │               │   │   │   └───__pycache__
│       │               │   │   └───__pycache__
│       │               │   └───__pycache__
│       │               └───pip-24.0.dist-info
│       └───__pycache__
├───venv
│   ├───bin
│   ├───include
│   │   └───python3.12
│   ├───lib
│   │   ├───python3.12
│   │   │   └───site-packages
│   │   │       ├───blinker
│   │   │       │   └───__pycache__
│   │   │       ├───blinker-1.9.0.dist-info
│   │   │       ├───click
│   │   │       │   └───__pycache__
│   │   │       ├───click-8.3.0.dist-info
│   │   │       │   └───licenses
│   │   │       ├───flask
│   │   │       │   ├───json
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───sansio
│   │   │       │   │   └───__pycache__
│   │   │       │   └───__pycache__
│   │   │       ├───flask-3.1.2.dist-info
│   │   │       │   └───licenses
│   │   │       ├───itsdangerous
│   │   │       │   └───__pycache__
│   │   │       ├───itsdangerous-2.2.0.dist-info
│   │   │       ├───jinja2
│   │   │       │   └───__pycache__
│   │   │       ├───jinja2-3.1.6.dist-info
│   │   │       │   └───licenses
│   │   │       ├───markupsafe
│   │   │       │   └───__pycache__
│   │   │       ├───MarkupSafe-3.0.2.dist-info
│   │   │       ├───pip
│   │   │       │   ├───_internal
│   │   │       │   │   ├───cli
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───commands
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───distributions
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───index
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───locations
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───metadata
│   │   │       │   │   │   ├───importlib
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───models
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───network
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───operations
│   │   │       │   │   │   ├───build
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───install
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───req
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───resolution
│   │   │       │   │   │   ├───legacy
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───resolvelib
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───utils
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───vcs
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───_vendor
│   │   │       │   │   ├───cachecontrol
│   │   │       │   │   │   ├───caches
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───certifi
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───chardet
│   │   │       │   │   │   ├───cli
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───metadata
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───colorama
│   │   │       │   │   │   ├───tests
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───distlib
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───distro
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───idna
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───msgpack
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───packaging
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───pkg_resources
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───platformdirs
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───pygments
│   │   │       │   │   │   ├───filters
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───formatters
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───lexers
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───styles
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───pyparsing
│   │   │       │   │   │   ├───diagram
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───pyproject_hooks
│   │   │       │   │   │   ├───_in_process
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───requests
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───resolvelib
│   │   │       │   │   │   ├───compat
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───rich
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───tenacity
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───tomli
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───truststore
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───urllib3
│   │   │       │   │   │   ├───contrib
│   │   │       │   │   │   │   ├───_securetransport
│   │   │       │   │   │   │   │   └───__pycache__
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───packages
│   │   │       │   │   │   │   ├───backports
│   │   │       │   │   │   │   │   └───__pycache__
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   ├───util
│   │   │       │   │   │   │   └───__pycache__
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   ├───webencodings
│   │   │       │   │   │   └───__pycache__
│   │   │       │   │   └───__pycache__
│   │   │       │   └───__pycache__
│   │   │       ├───pip-24.0.dist-info
│   │   │       ├───werkzeug
│   │   │       │   ├───datastructures
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───debug
│   │   │       │   │   ├───shared
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───middleware
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───routing
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───sansio
│   │   │       │   │   └───__pycache__
│   │   │       │   ├───wrappers
│   │   │       │   │   └───__pycache__
│   │   │       │   └───__pycache__
│   │   │       └───werkzeug-3.1.3.dist-info
│   │   └───site-packages
│   │       ├───aiohappyeyeballs
│   │       │   └───__pycache__
│   │       ├───aiohappyeyeballs-2.6.1.dist-info
│   │       ├───aiohttp
│   │       │   ├───.hash
│   │       │   ├───_websocket
│   │       │   │   ├───.hash
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───aiohttp-3.13.1.dist-info
│   │       │   └───licenses
│   │       │       └───vendor
│   │       │           └───llhttp
│   │       ├───aiosignal
│   │       │   └───__pycache__
│   │       ├───aiosignal-1.4.0.dist-info
│   │       │   └───licenses
│   │       ├───attr
│   │       │   └───__pycache__
│   │       ├───attrs
│   │       │   └───__pycache__
│   │       ├───attrs-25.4.0.dist-info
│   │       │   └───licenses
│   │       ├───audioop
│   │       │   └───__pycache__
│   │       ├───audioop_lts-0.2.2.dist-info
│   │       │   └───licenses
│   │       ├───blinker
│   │       │   └───__pycache__
│   │       ├───blinker-1.9.0.dist-info
│   │       ├───certifi
│   │       │   └───__pycache__
│   │       ├───certifi-2025.10.5.dist-info
│   │       │   └───licenses
│   │       ├───cffi
│   │       │   └───__pycache__
│   │       ├───cffi-2.0.0.dist-info
│   │       │   └───licenses
│   │       ├───charset_normalizer
│   │       │   ├───cli
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───charset_normalizer-3.4.4.dist-info
│   │       │   └───licenses
│   │       ├───click
│   │       │   └───__pycache__
│   │       ├───click-8.3.0.dist-info
│   │       │   └───licenses
│   │       ├───colorama
│   │       │   ├───tests
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───colorama-0.4.6.dist-info
│   │       │   └───licenses
│   │       ├───discord
│   │       │   ├───app_commands
│   │       │   │   └───__pycache__
│   │       │   ├───bin
│   │       │   ├───ext
│   │       │   │   ├───commands
│   │       │   │   │   └───__pycache__
│   │       │   │   └───tasks
│   │       │   │       └───__pycache__
│   │       │   ├───types
│   │       │   │   └───__pycache__
│   │       │   ├───ui
│   │       │   │   └───__pycache__
│   │       │   ├───webhook
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───discord_py-2.6.4.dist-info
│   │       │   └───licenses
│   │       ├───dotenv
│   │       │   └───__pycache__
│   │       ├───flask
│   │       │   ├───json
│   │       │   │   └───__pycache__
│   │       │   ├───sansio
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───flask-3.1.2.dist-info
│   │       │   └───licenses
│   │       ├───frozenlist
│   │       │   └───__pycache__
│   │       ├───frozenlist-1.8.0.dist-info
│   │       │   └───licenses
│   │       ├───idna
│   │       │   └───__pycache__
│   │       ├───idna-3.11.dist-info
│   │       │   └───licenses
│   │       ├───itsdangerous
│   │       │   └───__pycache__
│   │       ├───itsdangerous-2.2.0.dist-info
│   │       ├───jinja2
│   │       │   └───__pycache__
│   │       ├───jinja2-3.1.6.dist-info
│   │       │   └───licenses
│   │       ├───markupsafe
│   │       │   └───__pycache__
│   │       ├───markupsafe-3.0.3.dist-info
│   │       │   └───licenses
│   │       ├───multidict
│   │       │   └───__pycache__
│   │       ├───multidict-6.7.0.dist-info
│   │       │   └───licenses
│   │       ├───nacl
│   │       │   ├───bindings
│   │       │   │   └───__pycache__
│   │       │   ├───pwhash
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pip
│   │       │   ├───_internal
│   │       │   │   ├───cli
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───commands
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───distributions
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───index
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───locations
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───metadata
│   │       │   │   │   ├───importlib
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───models
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───network
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───operations
│   │       │   │   │   ├───build
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───install
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───req
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───resolution
│   │       │   │   │   ├───legacy
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───resolvelib
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───utils
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───vcs
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───_vendor
│   │       │   │   ├───cachecontrol
│   │       │   │   │   ├───caches
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───certifi
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───dependency_groups
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───distlib
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───distro
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───idna
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───msgpack
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───packaging
│   │       │   │   │   ├───licenses
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───pkg_resources
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───platformdirs
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───pygments
│   │       │   │   │   ├───filters
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───formatters
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───lexers
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───styles
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───pyproject_hooks
│   │       │   │   │   ├───_in_process
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───requests
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───resolvelib
│   │       │   │   │   ├───resolvers
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───rich
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───tomli
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───tomli_w
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───truststore
│   │       │   │   │   └───__pycache__
│   │       │   │   ├───urllib3
│   │       │   │   │   ├───contrib
│   │       │   │   │   │   ├───_securetransport
│   │       │   │   │   │   │   └───__pycache__
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───packages
│   │       │   │   │   │   ├───backports
│   │       │   │   │   │   │   └───__pycache__
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   ├───util
│   │       │   │   │   │   └───__pycache__
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pip-25.2.dist-info
│   │       │   └───licenses
│   │       │       └───src
│   │       │           └───pip
│   │       │               └───_vendor
│   │       │                   ├───cachecontrol
│   │       │                   ├───certifi
│   │       │                   ├───dependency_groups
│   │       │                   ├───distlib
│   │       │                   ├───distro
│   │       │                   ├───idna
│   │       │                   ├───msgpack
│   │       │                   ├───packaging
│   │       │                   ├───pkg_resources
│   │       │                   ├───platformdirs
│   │       │                   ├───pygments
│   │       │                   ├───pyproject_hooks
│   │       │                   ├───requests
│   │       │                   ├───resolvelib
│   │       │                   ├───rich
│   │       │                   ├───tomli
│   │       │                   ├───tomli_w
│   │       │                   ├───truststore
│   │       │                   └───urllib3
│   │       ├───propcache
│   │       │   └───__pycache__
│   │       ├───propcache-0.4.1.dist-info
│   │       │   └───licenses
│   │       ├───psutil
│   │       │   ├───tests
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───psutil-7.1.0.dist-info
│   │       ├───pycparser
│   │       │   ├───ply
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───pycparser-2.23.dist-info
│   │       ├───pynacl-1.6.0.dist-info
│   │       │   └───licenses
│   │       ├───python_dotenv-1.1.1.dist-info
│   │       │   └───licenses
│   │       ├───requests
│   │       │   └───__pycache__
│   │       ├───requests-2.32.5.dist-info
│   │       │   └───licenses
│   │       ├───urllib3
│   │       │   ├───contrib
│   │       │   │   ├───emscripten
│   │       │   │   │   └───__pycache__
│   │       │   │   └───__pycache__
│   │       │   ├───http2
│   │       │   │   └───__pycache__
│   │       │   ├───util
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───urllib3-2.5.0.dist-info
│   │       │   └───licenses
│   │       ├───watchdog
│   │       │   ├───observers
│   │       │   │   └───__pycache__
│   │       │   ├───tricks
│   │       │   │   └───__pycache__
│   │       │   ├───utils
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───watchdog-6.0.0.dist-info
│   │       ├───werkzeug
│   │       │   ├───datastructures
│   │       │   │   └───__pycache__
│   │       │   ├───debug
│   │       │   │   ├───shared
│   │       │   │   └───__pycache__
│   │       │   ├───middleware
│   │       │   │   └───__pycache__
│   │       │   ├───routing
│   │       │   │   └───__pycache__
│   │       │   ├───sansio
│   │       │   │   └───__pycache__
│   │       │   ├───wrappers
│   │       │   │   └───__pycache__
│   │       │   └───__pycache__
│   │       ├───werkzeug-3.1.3.dist-info
│   │       ├───yarl
│   │       │   └───__pycache__
│   │       └───yarl-1.22.0.dist-info
│   │           └───licenses
│   ├───lib64
│   │   └───python3.12
│   │       └───site-packages
│   │           ├───blinker
│   │           │   └───__pycache__
│   │           ├───blinker-1.9.0.dist-info
│   │           ├───click
│   │           │   └───__pycache__
│   │           ├───click-8.3.0.dist-info
│   │           │   └───licenses
│   │           ├───flask
│   │           │   ├───json
│   │           │   │   └───__pycache__
│   │           │   ├───sansio
│   │           │   │   └───__pycache__
│   │           │   └───__pycache__
│   │           ├───flask-3.1.2.dist-info
│   │           │   └───licenses
│   │           ├───itsdangerous
│   │           │   └───__pycache__
│   │           ├───itsdangerous-2.2.0.dist-info
│   │           ├───jinja2
│   │           │   └───__pycache__
│   │           ├───jinja2-3.1.6.dist-info
│   │           │   └───licenses
│   │           ├───markupsafe
│   │           │   └───__pycache__
│   │           ├───MarkupSafe-3.0.2.dist-info
│   │           ├───pip
│   │           │   ├───_internal
│   │           │   │   ├───cli
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───commands
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───distributions
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───index
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───locations
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───metadata
│   │           │   │   │   ├───importlib
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───models
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───network
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───operations
│   │           │   │   │   ├───build
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───install
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───req
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───resolution
│   │           │   │   │   ├───legacy
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───resolvelib
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───utils
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───vcs
│   │           │   │   │   └───__pycache__
│   │           │   │   └───__pycache__
│   │           │   ├───_vendor
│   │           │   │   ├───cachecontrol
│   │           │   │   │   ├───caches
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───certifi
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───chardet
│   │           │   │   │   ├───cli
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───metadata
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───colorama
│   │           │   │   │   ├───tests
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───distlib
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───distro
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───idna
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───msgpack
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───packaging
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───pkg_resources
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───platformdirs
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───pygments
│   │           │   │   │   ├───filters
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───formatters
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───lexers
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───styles
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───pyparsing
│   │           │   │   │   ├───diagram
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───pyproject_hooks
│   │           │   │   │   ├───_in_process
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───requests
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───resolvelib
│   │           │   │   │   ├───compat
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───rich
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───tenacity
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───tomli
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───truststore
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───urllib3
│   │           │   │   │   ├───contrib
│   │           │   │   │   │   ├───_securetransport
│   │           │   │   │   │   │   └───__pycache__
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───packages
│   │           │   │   │   │   ├───backports
│   │           │   │   │   │   │   └───__pycache__
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   ├───util
│   │           │   │   │   │   └───__pycache__
│   │           │   │   │   └───__pycache__
│   │           │   │   ├───webencodings
│   │           │   │   │   └───__pycache__
│   │           │   │   └───__pycache__
│   │           │   └───__pycache__
│   │           ├───pip-24.0.dist-info
│   │           ├───werkzeug
│   │           │   ├───datastructures
│   │           │   │   └───__pycache__
│   │           │   ├───debug
│   │           │   │   ├───shared
│   │           │   │   └───__pycache__
│   │           │   ├───middleware
│   │           │   │   └───__pycache__
│   │           │   ├───routing
│   │           │   │   └───__pycache__
│   │           │   ├───sansio
│   │           │   │   └───__pycache__
│   │           │   ├───wrappers
│   │           │   │   └───__pycache__
│   │           │   └───__pycache__
│   │           └───werkzeug-3.1.3.dist-info
│   └───Scripts
└───__pycache__
