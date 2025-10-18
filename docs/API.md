# Discord Bot Manager - API Documentation

**Version:** 1.0.0  
**Created by:** headx & the psychon

This document describes the internal API structure of the Discord Bot Manager.

## Table of Contents

- [Overview](#overview)
- [Server Endpoints](#server-endpoints)
- [Data Structures](#data-structures)
- [JavaScript API](#javascript-api)
- [Python API](#python-api)
- [Error Handling](#error-handling)

---

## Overview

The Discord Bot Manager uses a combination of:
- **Frontend:** HTML + JavaScript (localStorage for data persistence)
- **Backend:** Python HTTP server for file serving
- **Data Storage:** Browser localStorage + File system

### Architecture

```
┌─────────────┐
│   Browser   │
│  (Frontend) │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────┐
│   Python    │
│   Server    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ File System │
│   (Bots)    │
└─────────────┘
```

---

## Server Endpoints

### GET /
Serves the main application interface.

**Response:** HTML page

### GET /styles.css
Serves the main stylesheet.

**Response:** CSS file

### GET /script.js
Serves the main JavaScript application.

**Response:** JavaScript file

### GET /bots/{bot_folder}/
Serves bot files when requested.

**Response:** Bot file contents

---

## Data Structures

### Bot Object

```javascript
{
    id: string,              // Unique bot identifier (timestamp)
    name: string,            // Bot display name
    token: string,           // Discord bot token
    clientId: string,        // Discord application client ID
    folder: string,          // Bot folder name
    start: string,           // Start file name (e.g., "main.py")
    invite: string,          // OAuth2 invite URL
    prefix: string,          // Command prefix (default: "!")
    commands: Array<Command>, // Bot commands
    commandMode: string,     // "single" or "multiple"
    files: Object,           // File name -> content mapping
    created: string,         // ISO timestamp
    status: string,          // "online" | "offline" | "error" | "starting" | "stopping"
    lastUpdated: string,     // ISO timestamp
    processId: number,       // Process ID when running
    currentLog: string,      // Current log file path
    settings: {
        autoRestart: boolean,
        logging: boolean,
        debug: boolean
    }
}
```

### Command Object

```javascript
{
    id: string,          // Unique command identifier
    name: string,        // Command name
    description: string, // Command description
    code: string,        // Python code
    category: string,    // Command category
    mode: string        // "single" or "multiple"
}
```

### Template Object

```javascript
{
    name: string,        // Template name
    description: string, // Template description
    category: string,    // Template category
    code: string        // Python command code
}
```

---

## JavaScript API

### Core Functions

#### `initializeApp()`
Initializes the application on page load.

```javascript
function initializeApp()
```

**Description:** Loads saved bots from localStorage and renders the UI.

---

#### `renderBots()`
Renders all bot cards to the overview tab.

```javascript
function renderBots()
```

**Description:** Creates HTML bot cards with status and actions.

---

### Bot Management

#### `handleAddBot(event)`
Handles bot creation form submission.

```javascript
function handleAddBot(e: Event): void
```

**Parameters:**
- `e` - Form submit event

**Validation:**
- Required fields: bot_name, bot_token, client_id
- Client ID must be 17-19 digits
- Token format validation (optional)

**Creates:**
- Bot object with all files
- Configuration files
- Main bot script
- Requirements file

---

#### `deleteBot(botId)`
Deletes a bot and all its data.

```javascript
function deleteBot(botId: string): void
```

**Parameters:**
- `botId` - Unique bot identifier

**Confirmation:** Shows confirmation dialog before deletion.

---

#### `openBotDetails(botId)`
Opens bot details modal for editing.

```javascript
function openBotDetails(botId: string): void
```

**Parameters:**
- `botId` - Unique bot identifier

**Opens:**
- Bot configuration editor
- File tree viewer
- Code editor

---

#### `saveBotInfo()`
Saves changes to bot configuration.

```javascript
function saveBotInfo(): void
```

**Saves:**
- Bot name, folder, token, client ID
- Invite URL
- Start file

---

### File Management

#### `loadFileTree(bot)`
Loads file tree for bot.

```javascript
function loadFileTree(bot: Bot): void
```

**Parameters:**
- `bot` - Bot object

---

#### `loadFile(filename)`
Loads file content into editor.

```javascript
function loadFile(filename: string): void
```

**Parameters:**
- `filename` - Name of file to load

---

#### `saveFile()`
Saves current file in editor.

```javascript
function saveFile(): void
```

**Requirements:**
- File must be loaded
- Editor must have content

---

#### `createNewFile()`
Creates a new file in bot directory.

```javascript
function createNewFile(): void
```

**Input:** Filename from `new-file-name` input field

---

#### `deleteFile(filename)`
Deletes a file from bot.

```javascript
function deleteFile(filename: string): void
```

**Parameters:**
- `filename` - Name of file to delete

---

### Command Builder

#### `openCommandBuilder(mode)`
Opens command builder modal.

```javascript
function openCommandBuilder(mode: 'single' | 'multiple'): void
```

**Parameters:**
- `mode` - Command mode (single file or cogs)

---

#### `addCustomCommand()`
Adds custom command from builder.

```javascript
function addCustomCommand(): void
```

**Validates:**
- Command name (required)
- Command code (required)

**Adds to:** Current commands array

---

#### `removeCommand(commandId)`
Removes command from current bot.

```javascript
function removeCommand(commandId: string): void
```

**Parameters:**
- `commandId` - Command identifier

---

### Templates

#### `useTemplate(templateName)`
Applies a command template.

```javascript
function useTemplate(templateName: string): void
```

**Parameters:**
- `templateName` - Name of template to use

**Available Templates:**
- `basic` - Ping, Hello
- `moderation` - Kick, Clear
- `fun` - 8ball, Dice
- `music` - Play (requires additional setup)

---

### Export/Import

#### `exportBot(botId)`
Exports bot configuration to JSON.

```javascript
function exportBot(botId: string): void
```

**Parameters:**
- `botId` - Bot identifier

**Downloads:** JSON file with bot configuration

---

#### `importBot(file)`
Imports bot from JSON file.

```javascript
function importBot(file: File): void
```

**Parameters:**
- `file` - JSON file with bot configuration

---

### Download Functions

#### `downloadScript(botId, type)`
Downloads start script for bot.

```javascript
function downloadScript(botId: string, type: 'python' | 'batch'): void
```

**Parameters:**
- `botId` - Bot identifier
- `type` - Script type

**Generates:**
- Python start script (.py)
- Windows batch script (.bat)

---

### Utility Functions

#### `showNotification(message, type, duration)`
Shows notification to user.

```javascript
function showNotification(
    message: string,
    type: 'success' | 'error' | 'warning' | 'info' = 'info',
    duration: number = 3000
): void
```

**Parameters:**
- `message` - Notification message
- `type` - Notification type
- `duration` - Display duration in milliseconds

---

#### `showTab(tabName, clickedTab)`
Switches between main tabs.

```javascript
function showTab(tabName: string, clickedTab?: HTMLElement): void
```

**Parameters:**
- `tabName` - Tab identifier ('overview', 'add-bot', 'templates')
- `clickedTab` - Optional clicked tab element

---

#### `generateInviteUrl(clientId)`
Generates OAuth2 invite URL.

```javascript
function generateInviteUrl(clientId: string): string
```

**Parameters:**
- `clientId` - Discord application client ID

**Returns:** OAuth2 invite URL with administrator permissions

---

## Python API

### SimpleWebServer Class

#### `__init__()`
Initializes the web server.

```python
def __init__(self) -> None
```

**Sets up:**
- Base directories
- Logging
- Signal handlers

---

#### `start()`
Starts the web server.

```python
def start(self) -> None
```

**Process:**
1. Finds available port
2. Gets local and public IP
3. Starts HTTP server
4. Serves files

---

#### `find_available_port()`
Finds an available port for the server.

```python
def find_available_port(self) -> int
```

**Preferred Ports:** 8000, 5000, 8080, 3000, 80, 8888, 9000

**Returns:** Available port number

---

### File Generation Functions

#### `generateBotFiles(bot)`
Generates all bot files.

```javascript
function generateBotFiles(bot: Bot): void
```

**Generates:**
- main.py or multi-file structure
- config.json
- requirements.txt
- .env.example

---

#### `generateSingleFileBot(bot)`
Generates single-file bot structure.

```javascript
function generateSingleFileBot(bot: Bot): void
```

**Creates:** Single main.py with all commands

---

#### `generateMultiFileBot(bot)`
Generates multi-file bot structure.

```javascript
function generateMultiFileBot(bot: Bot): void
```

**Creates:**
- main.py (loader)
- cogs/ directory
- Individual cog files

---

## Error Handling

### Error Types

```javascript
{
    code: string,      // Error code
    message: string,   // Error message
    title: string,     // Error title
    solution: string   // Suggested solution
}
```

### Common Error Codes

- `INVALID_TOKEN` - Invalid Discord bot token
- `INVALID_CLIENT_ID` - Invalid client ID format
- `FILE_NOT_FOUND` - File not found
- `SAVE_ERROR` - Error saving data
- `NETWORK_ERROR` - Network request failed

### Error Handler

```javascript
function handleError(error: Error, context: string): void
```

**Displays:** User-friendly error message with solution

---

## Storage

### localStorage Keys

- `discord-bots` - Array of bot objects
- `lastActiveTab` - Last active tab name

### File System Structure

```
discord-bot-manager/
├── bots/
│   └── {bot_folder}/
│       ├── main.py
│       ├── config.json
│       ├── requirements.txt
│       ├── .env
│       ├── cogs/           (if multi-file)
│       │   ├── __init__.py
│       │   ├── basic.py
│       │   └── ...
│       └── logs/
│           └── bot-{date}.log
├── logs/
│   └── server-{date}.log
└── data/
```

---

## Security Considerations

1. **Token Storage**
   - Tokens stored in localStorage (browser)
   - Token visibility toggle in UI
   - No server-side token storage

2. **Input Validation**
   - Client ID format validation
   - Required field validation
   - File name sanitization

3. **File Operations**
   - Restricted to bot directories
   - No arbitrary file access
   - Safe file name handling

---

## Future API Enhancements

Planned for future versions:

- RESTful API endpoints
- WebSocket for real-time updates
- Authentication system
- Database integration
- API rate limiting
- Webhook support

---

**For more information, see:**
- [README.md](README.md) - General documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](CHANGELOG.md) - Version history

**Created with ❤️ by headx & the psychon**
