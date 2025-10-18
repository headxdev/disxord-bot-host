# 🤖 Discord Bot Manager

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.3.2%2B-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Created by headx & the psychon**

## 🌟 Overview

The Discord Bot Manager is a comprehensive tool designed to simplify the creation, management, and operation of Discord bots. It provides a beautiful, user-friendly web interface with a cosmic space theme that allows users to create and manage multiple Discord bots without writing code manually.

### ✨ Key Features

- 🎨 **Beautiful Cosmic UI** - Stunning space-themed interface with animated planets and nebulae
- 🔐 **Discord OAuth2 Login** - Connect your Discord account and import your bots automatically
- 🤖 **Auto-Import Bots** - Import your existing Discord applications with one click
- 🚀 **Quick Bot Creation** - Create Discord bots in minutes with an intuitive form-based interface
- 📝 **Code Editor** - Built-in file editor for customizing bot code
- ⚡ **Command Templates** - Pre-built command templates for common bot functions
- 🔄 **Live Bot Management** - Start, stop, and monitor your bots in real-time
- 📊 **Status Monitoring** - Visual status indicators for all your bots
- 📦 **Export/Import** - Export bot configurations and import them on other systems
- 🌐 **Cross-Platform** - Works on Windows, Linux, and macOS
- 📱 **Responsive Design** - Mobile-friendly interface
- 🔒 **Secure** - OAuth2 authentication and local token storage

## Project Structure
The project consists of the following files and directories:

- **bot_manager.py**: The main control file for the bot manager. It handles the creation, starting, and stopping of bots, and dynamically generates the necessary folder structure and files when a new bot is created.

- **index.html**: The frontend file that provides the user interface for interacting with the bot manager.

- **style.css**: Contains styles for the website, defining the visual appearance of the frontend.
 - **styles-mobile.css**: Mobile-specific overrides and optimizations.
 - **theme-overrides.css**: Final layout and visual overrides applied after the main theme.

- **script.js**: Adds interactivity to the website, handling user actions and making API calls to the backend.

- **server.php**: Acts as the backend connector between the website and the Python bot manager, processing requests from the frontend and communicating with bot_manager.py.

- **server.log**: Used for logging events and errors related to the bot manager itself, providing a centralized log for debugging.

- **bots/**: Directory containing all the bot instances created by the manager.

  - **testbot/**: An example bot folder that is dynamically created when a new bot is added. It contains:
    - **start.py**: Responsible for loading the bot's configuration, starting the bot, and redirecting logs to a new log file in the logs directory.
    - **infos/**: Directory containing configuration files for the bot.
      - **config.json**: Holds the bot's configuration settings, such as the token, command prefix, and bot name.
    - **commands/**: Directory where the bot's command files are stored.
      - **ping.js**: Defines a command that responds with a "pong" message when invoked.
      - **hello.js**: Defines a command that responds with a greeting message when invoked.
    - **cogs/**: Directory for optional extensions or modules for the bot, following the Discord.py standard.
      - **example.py**: Serves as an example cog that can be extended or modified for additional functionality.
    - **events/**: Directory containing event handler files for the bot.
      - **on_ready.py**: Defines actions to take when the bot is ready and connected to Discord.
    - **requirements.txt**: Lists the dependencies required for the bot, such as discord.py.
    - **logs/**: Directory where log files for the bot are stored.
      - **log-17-00-28-09-2025.txt**: An example log file created when the bot is started, capturing its runtime logs.

- **README.md**: This documentation file, providing an overview of the project and instructions for setup and usage.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser
- Discord Bot Token (from [Discord Developer Portal](https://discord.com/developers/applications))

### ⚡ Super Quick Start (1 Command!)

**Das ist ALLES was Sie brauchen:**

```bash
# Clone the repository
git clone https://github.com/yourusername/discord-bot-manager.git
cd discord-bot-manager

# Start (macht automatisch alles!)
python start.py
```

**Das war's!** 🎉

Der `start.py` Script:
- ✅ Erkennt Ihr Betriebssystem automatisch (Windows/Linux/macOS)
- ✅ Prüft Python-Version
- ✅ Installiert alle Dependencies automatisch
- ✅ Erstellt notwendige Verzeichnisse
- ✅ Generiert Konfigurationsdateien
- ✅ Startet den Server

**Siehe auch:** [START_HERE.md](START_HERE.md) für detaillierte Anleitung

### Alternative: Mit Virtual Environment (Empfohlen für Entwickler)

```bash
# Clone
git clone https://github.com/yourusername/discord-bot-manager.git
cd discord-bot-manager

# Virtual Environment erstellen
python -m venv venv

# Aktivieren
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Starten (installiert automatisch dependencies)
python start.py
```

### Discord OAuth2 Setup (Optional but Recommended)

To enable Discord login and automatic bot import:

1. Follow the detailed guide in [DISCORD_OAUTH_SETUP.md](DISCORD_OAUTH_SETUP.md)
2. Create a Discord application at [Discord Developer Portal](https://discord.com/developers/applications)
3. Get your Client ID and Client Secret
4. Add them to your `.env` file:
   ```env
   DISCORD_CLIENT_ID=your_client_id
   DISCORD_CLIENT_SECRET=your_client_secret
   DISCORD_REDIRECT_URI=http://localhost:8000/auth/callback
   ```
5. Restart the server

### Erster Start

1. **Server startet automatisch** beim ersten Ausführen von `python start.py`
2. Öffnen Sie Ihren Browser und gehen zu `http://localhost:8000`
3. Sie sehen das Discord Bot Manager Interface
4. **[Optional]** Klicken Sie "Mit Discord anmelden" um OAuth2 zu aktivieren
5. Erstellen Sie Ihren ersten Bot:
   - **Option A:** "Discord Apps" Tab → Automatischer Import (wenn angemeldet)
   - **Option B:** "Bot hinzufügen" Tab → Manuell erstellen

**Hinweis:** Beim ersten Start werden Sie durch das Setup geführt. Danach startet der Server direkt.

### Creating a Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give your application a name
4. Go to the "Bot" section
5. Click "Add Bot"
6. Click "Reset Token" to get your bot token
7. Enable "Message Content Intent" under "Privileged Gateway Intents"
8. Copy the token and paste it into the Bot Manager

## 📖 Usage

### Connecting Your Discord Account

1. **Click "Mit Discord anmelden"** in the header
2. **Authorize the application** on Discord
3. **You're connected!** Your profile will appear in the header

### Importing Discord Bots Automatically

1. **Log in with Discord** (see above)
2. **Navigate to "Discord Apps" tab**
3. **See all your Discord applications** listed automatically
4. **Click "Importieren"** on any bot
5. **Enter the bot token** when prompted
6. **Done!** Your bot is imported with all settings

Benefits of auto-import:
- ✅ No manual data entry
- ✅ Correct Client ID automatically
- ✅ Application name and icon pre-filled
- ✅ Easy management of multiple bots

### Creating a New Bot

1. **Navigate to "Bot hinzufügen" tab**
2. **Fill in basic information:**
   - Bot Name (required)
   - Discord Bot Token (required)
   - Client ID (required)
   - Command Prefix (default: !)
   - Bot Folder (auto-generated if empty)

3. **Add Commands:**
   - Choose between single file or multi-file (Cogs) structure
   - Add commands from templates or create custom commands
   - Use the command builder for quick command creation

4. **Click "Bot erstellen"**

### Managing Bots

#### Bot Overview
- View all your bots in the "Übersicht" tab
- See status indicators (online/offline/error)
- Quick actions: Start, Stop, Manage, Delete

#### Bot Details
- Click "Verwalten" on any bot card
- Edit bot configuration
- View and edit bot files
- Download scripts and exports
- View OAuth2 invite link

#### File Management
- View bot files in the file tree
- Click any file to edit in the code editor
- Create new files with the "Neue Datei" button
- Save changes with the "Speichern" button

### Using Command Templates

1. Go to the "Templates" tab
2. Browse categories: Moderation, Fun, Utility, Music
3. Click "Template nutzen" to add commands to your bot
4. Templates will be automatically added to your current bot

### Starting and Stopping Bots

- **Start:** Click the green "Start" button on any bot
- **Stop:** Click the red "Stop" button on a running bot
- **Restart:** Stop and start the bot again

### Viewing Logs

1. Click "Logs" button on any bot card
2. View real-time logs with auto-scroll
3. Switch between log files using the dropdown
4. Download or clear logs as needed

### Exporting and Importing Bots

#### Export
1. Open bot details
2. Click "Export" button
3. Save the JSON file

#### Import (Manual)
1. Click "Bot importieren" in the footer
2. Select your exported JSON file
3. Bot will be created with all settings

#### Import (from Discord)
1. Log in with Discord
2. Go to "Discord Apps" tab
3. Click "Importieren" on any application
4. Enter bot token
5. Bot is imported automatically!

## 🛠️ Advanced Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Bot Defaults
DEFAULT_PREFIX=!
LOG_LEVEL=INFO

# Security
ENABLE_HTTPS=False
```

### Custom Port

The server automatically finds an available port. To force a specific port, edit the `.env` file.

### Directory Structure

```
discord-bot-manager/
├── bots/                    # Bot instances
│   ├── bot_1/
│   │   ├── main.py
│   │   ├── config.json
│   │   ├── requirements.txt
│   │   ├── .env
│   │   └── logs/
│   └── bot_2/
├── cmdtamplates/           # Command templates
├── logs/                   # Server logs
├── data/                   # Data storage
├── start.py               # Main server file
├── index.html             # Web interface
├── script.js              # Frontend logic
├── styles.css             # Styling
└── README.md              # This file
```

## 🎨 Customization

### Modifying the Theme

Edit `styles.css` to change colors, animations, or layout:

```css
:root {
    --primary: #9d4edd;
    --secondary: #4d9eff;
    --accent: #ff4d8f;
    /* ... more variables */
}
```

### Adding Custom Templates

Create new command templates in `script.js`:

```javascript
commandTemplates.custom = [
    {
        name: 'mycommand',
        description: 'My custom command',
        category: 'Custom',
        code: `@bot.command(name='mycommand')
async def mycommand(ctx):
    await ctx.send('Hello!')`
    }
];
```

## 🐛 Troubleshooting

### Common Issues

**Issue: Bot won't start**
- Verify the bot token is correct
- Check that all required intents are enabled in Discord Developer Portal
- Review logs for specific error messages

**Issue: Port already in use**
- The server will automatically find a free port
- Check the console output for the actual port being used

**Issue: Commands not working**
- Ensure Message Content Intent is enabled
- Check the command prefix matches
- Verify the bot has necessary permissions

**Issue: Can't connect to web interface**
- Check firewall settings
- Verify the server is running
- Try using localhost:8000 instead of 127.0.0.1:8000

### Getting Help

- Check existing [GitHub Issues](https://github.com/yourusername/discord-bot-manager/issues)
- Create a new issue with:
  - Operating system
  - Python version
  - Error messages
  - Steps to reproduce

## 📝 API Reference

### Server Endpoints

```
GET  /                      # Main interface
GET  /api/bots             # Get all bots
POST /api/bots/create      # Create new bot
POST /api/bots/start       # Start bot
POST /api/bots/stop        # Stop bot
GET  /api/bots/logs        # Get bot logs
POST /api/bots/delete      # Delete bot
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/AmazingFeature`
3. **Commit your changes:** `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch:** `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/discord-bot-manager.git
cd discord-bot-manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python start.py
```

### Code Style

- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Comment complex logic
- Write descriptive commit messages

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **headx** - *Initial work and development*
- **the psychon** - *Initial work and development*

## 🙏 Acknowledgments

- Discord.py community for the excellent library
- All contributors who help improve this project
- The Discord Bot developer community

## 📊 Project Status

- ✅ Core functionality complete
- ✅ Web interface operational
- ✅ Command templates available
- 🚧 Additional templates in development
- 🚧 Plugin system planned
- 🚧 API documentation in progress

## 🔗 Links

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API Documentation](https://discord.com/developers/docs)
- [Discord OAuth2 Setup Guide](DISCORD_OAUTH_SETUP.md)
- [API Documentation](API.md)

---

**Made with ❤️ by headx & the psychon**
