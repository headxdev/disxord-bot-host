/**
 * Theme management and responsive design utilities
 */
(function() {
    'use strict';

    // Throttle function for performance optimization
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Detect screen orientation / resolution and swap theme CSS
    function updateThemeStyle() {
        try {
            let link = document.getElementById('theme-style');
            if (!link) {
                link = document.createElement('link');
                link.rel = 'stylesheet';
                link.id = 'theme-style';
                document.head.appendChild(link);
            }

            const { innerWidth: w = 1024, innerHeight: h = 768 } = window;
            const isMobile = h > w || w <= 800;
            const desired = isMobile ? 'styles-mobile.css' : 'style.css';
            
            if (!link.href.endsWith(desired)) {
                link.href = desired;
                console.log('Switched theme to', desired);
            }
        } catch (error) {
            console.warn('Failed to update theme style:', error);
        }
    }

    // Throttled update function for better performance
    const throttledUpdateTheme = throttle(updateThemeStyle, 250);

    // Event listeners
    document.addEventListener('DOMContentLoaded', updateThemeStyle);
    window.addEventListener('resize', throttledUpdateTheme);
    window.addEventListener('orientationchange', () => {
        // Small delay for orientation change to complete
        setTimeout(updateThemeStyle, 100);
    });

// Expose toggler for debugging
window.toggleTheme = function(forceMobile) {
    var link = document.getElementById('theme-style');
    var pred = (typeof forceMobile === 'boolean') ? forceMobile : ((window.innerHeight > window.innerWidth) || (window.innerWidth <= 800));
    link.href = pred ? 'styles-mobile.css' : 'style.css';
    console.log('Theme manually set to', link.href);

    // Fetch install and network info and render in header
    async function fetchInstallInfo() {
        try {
            const res = await fetch('/info');
            if (!res.ok) return;
            const data = await res.json();
            const info = document.createElement('div');
            info.className = 'install-info';
            info.style.fontSize = '0.9em';
            info.style.color = 'var(--text-muted)';
            info.innerText = `LAN: ${data.wlan_ip} • Public: ${data.public_ip}`;
            const headerActions = document.querySelector('.header-actions');
            if (headerActions && !document.querySelector('.install-info')) {
                headerActions.insertBefore(info, headerActions.firstChild);
            }
        } catch (e) {
            // ignore
        }
    }

// call on load
    // document.addEventListener('DOMContentLoaded', fetchInstallInfo);
}

})();

// ...existing code...
// Discord Bot Manager - Enhanced Version
// Created by headx and the psychon
// Features: Token management, Command builder, Template system

let bots = [];
let currentBotId = null;
let currentFile = null;
let currentCommands = [];
let commandMode = 'single';
let commandTemplates = {};

// ===============================
// INITIALIZATION
// ===============================

document.addEventListener('DOMContentLoaded', function() {
    updateThemeStyle();
    initializeApp();
    loadCommandTemplates();
    setupEventListeners();
    initializeTabs();
});

function initializeTabs() {
    // Restore last active tab
    const lastActiveTab = localStorage.getItem('lastActiveTab') || 'overview';
    const tabButton = document.querySelector(`[data-tab="${lastActiveTab}"]`);
    
    if (tabButton) {
        showTab(lastActiveTab, tabButton);
    }
    
    // Initialize card hover effects
    initializeCardEffects();
}

function initializeCardEffects() {
    // No mousemove effects needed - CSS will handle the hover animation
    console.log("Simple card hover effects initialized");
}

function initializeApp() {
    renderBots();
    
    // Load from localStorage if available
    const savedBots = localStorage.getItem('discord-bots');
    if (savedBots) {
        try {
            bots = JSON.parse(savedBots);
            renderBots();
        } catch (e) {
            console.error('Error loading saved bots:', e);
        }
    }
    
    console.log("Enhanced Discord Bot Manager initialized - Created by headx and the psychon");
}

function setupEventListeners() {
    // Form submission
    const addBotForm = document.getElementById('add-bot-form');
    if (addBotForm) {
        addBotForm.addEventListener('submit', handleAddBot);
    }
    
    // Auto-save on page unload
    window.addEventListener('beforeunload', function() {
        saveBots();
    });
    
    // Auto-generate invite URL on client ID change
    const clientIdInput = document.getElementById('client_id');
    if (clientIdInput) {
        clientIdInput.addEventListener('input', function() {
            updateInvitePreview(this.value);
        });
    }

    // Setup token visibility toggle
    setupTokenVisibilityToggles();
}

function setupTokenVisibilityToggles() {
    // Setup toggle for add bot form
    const addBotToken = document.getElementById('bot_token');
    const addBotToggle = document.getElementById('token-toggle');
    if (addBotToken && addBotToggle) {
        addBotToggle.addEventListener('click', () => toggleTokenVisibility(addBotToken, addBotToggle));
    }

    // Setup toggle for edit bot form
    const editBotToken = document.getElementById('edit-bot-token');
    const editBotToggle = document.querySelector('.btn-secondary[onclick="toggleEditTokenVisibility()"]');
    if (editBotToken && editBotToggle) {
        editBotToggle.addEventListener('click', () => toggleTokenVisibility(editBotToken, editBotToggle));
    }
}

function toggleTokenVisibility(inputElement, toggleButton) {
    if (!inputElement || !toggleButton) return;
    
    const isVisible = inputElement.type === 'text';
    inputElement.type = isVisible ? 'password' : 'text';
    toggleButton.innerHTML = isVisible ? '👁️' : '👁️‍🗨️';
    toggleButton.title = isVisible ? 'Token anzeigen' : 'Token verbergen';
}

// ===============================
// TAB MANAGEMENT
// ===============================

function showTab(tabName, clickedTab = null) {
    console.log(`Attempting to show tab: ${tabName}`);
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active from navigation tabs (support legacy .nav-tab too)
    document.querySelectorAll('.navigation-tab, .nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    const targetTab = document.getElementById(tabName);
    console.log('Target tab element:', targetTab);
    if (targetTab) {
        targetTab.classList.add('active');
        console.log(`Added 'active' class to tab: ${tabName}`);
        
        // If it's the templates tab, show the first template section
        if (tabName === 'templates') {
            const firstTemplateSection = document.querySelector('.template-section');
            if (firstTemplateSection) {
                showTemplateSection('moderation');
            }
        }
        
        // Smooth scroll to tab
        targetTab.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Add active to clicked navigation tab (support legacy .nav-tab)
    if (clickedTab) {
        clickedTab.classList.add('active');
    } else {
        // Find and activate corresponding navigation tab
        document.querySelector(`.navigation-tab[data-tab="${tabName}"]`)?.classList.add('active');
        document.querySelector(`.nav-tab[data-tab="${tabName}"]`)?.classList.add('active');
    }
    
    // Save last active tab
    localStorage.setItem('lastActiveTab', tabName);
}

// Template Section Handling
function showTemplateSection(sectionName) {
    // Hide all template sections
    document.querySelectorAll('.template-section').forEach(section => {
        section.style.display = 'none';
        section.classList.remove('active');
    });
    
    // Show selected template section
    const targetSection = document.getElementById(`${sectionName}-templates`);
    if (targetSection) {
        targetSection.style.display = 'block';
        setTimeout(() => {
            targetSection.classList.add('active');
        }, 50);
    }
    
    // Update template navigation
    document.querySelectorAll('.template-nav .nav-tab').forEach(tab => {
        if (tab.getAttribute('data-tab') === sectionName) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });
}

// Initialize template navigation
document.addEventListener('DOMContentLoaded', function() {
    const templateNavButtons = document.querySelectorAll('.template-navigation .navigation-tab, .template-nav .nav-tab');
    templateNavButtons.forEach(button => {
        button.addEventListener('click', () => {
            const section = button.getAttribute('data-tab');
            showTemplateSection(section);
        });
    });
});

function switchCommandMode(mode) {
    commandMode = mode;
    
    // Update tab buttons (support legacy .tab-btn and new .tab-button)
    document.querySelectorAll('.tab-btn, .tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    // If the event exists, mark its target active
    if (typeof event !== 'undefined' && event?.target) {
        event.target.classList.add('active');
    }
    
    // Show/hide mode sections
    const singleMode = document.getElementById('single-mode');
    const multipleMode = document.getElementById('multiple-mode');
    
    if (singleMode && multipleMode) {
        singleMode.style.display = mode === 'single' ? 'block' : 'none';
        multipleMode.style.display = mode === 'multiple' ? 'block' : 'none';
    }
    
    // Clear current commands when switching modes
    currentCommands = [];
    updateCommandPreview();
}

// ===============================
// BOT MANAGEMENT
// ===============================

function handleAddBot(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    
    // Only validate that fields are not empty
    const requiredFields = {
        'bot_name': 'Bot Name',
        'bot_token': 'Discord Bot Token',
        'client_id': 'Client ID'
    };
    
    for (const [field, label] of Object.entries(requiredFields)) {
        const value = formData.get(field)?.trim();
        if (!value) {
            showNotification(`Bitte füllen Sie das Feld "${label}" aus!`, 'error');
            const input = document.getElementById(field);
            if (input) {
                input.focus();
                input.classList.add('error');
                setTimeout(() => input.classList.remove('error'), 3000);
            }
            return;
        }
    }
    
    const token = formData.get('bot_token');
    
    // Validate client ID
    const clientId = formData.get('client_id');
    if (!validateClientId(clientId)) {
        showNotification('Ungültige Client ID! Die ID muss 17-19 Ziffern lang sein.', 'error');
        return;
    }
    
    // Create new bot object with improved defaults and validation
    const newBot = {
        id: Date.now().toString(),
        name: formData.get('bot_name').trim(),
        token: token.trim(),
        clientId: clientId.trim(),
        folder: formData.get('bot_folder')?.trim() || `bot_${Date.now()}`,
        start: formData.get('bot_start')?.trim() || 'main.py',
        invite: formData.get('bot_invite')?.trim() || generateInviteUrl(clientId),
        prefix: formData.get('command_prefix')?.trim() || '!',
        commands: [...currentCommands],
        commandMode: commandMode,
        files: {},
        created: new Date().toISOString(),
        status: 'offline',
        lastUpdated: new Date().toISOString(),
        settings: {
            autoRestart: formData.get('auto_restart') === 'true',
            logging: formData.get('enable_logging') === 'true',
            debug: formData.get('debug_mode') === 'true'
        }
    };
    
    // Generate bot files
    generateBotFiles(newBot);
    
    // Add to bots array
    bots.push(newBot);
    
    // Save and update UI
    saveBots();
    renderBots();
    
    // Reset form and show success
    e.target.reset();
    currentCommands = [];
    updateCommandPreview();
    
    showNotification('Bot erfolgreich erstellt!', 'success');
    
    // Switch to overview tab
    showTab('overview');
}

function renderBots() {
    const botList = document.getElementById('bot-list');
    if (!botList) return;
    
    botList.innerHTML = '';
    
    if (bots.length === 0) {
        botList.innerHTML = `
            <div class="no-bots draggable-container empty">
                <div>
                    <h3>Keine Bots gefunden</h3>
                    <p>Klicken Sie auf "Bot hinzufügen" um zu beginnen!</p>
                    <button class="btn btn-primary btn-large" onclick="showTab('add-bot')">
                        ➕ Bot Hinzufügen
                    </button>
                </div>
            </div>
        `;
        return;
    }
    
    // Sort bots by status (online first) and then by name
    const sortedBots = [...bots].sort((a, b) => {
        if (a.status === 'online' && b.status !== 'online') return -1;
        if (a.status !== 'online' && b.status === 'online') return 1;
        return a.name.localeCompare(b.name);
    });
    
    sortedBots.forEach(bot => {
        const botCard = document.createElement('div');
        botCard.classList.add('bot-card');
        botCard.classList.add(`status-${bot.status}`);
        // mark with data attribute for ordering and drag logic
        botCard.dataset.botId = bot.id;
        
        const lastUpdated = bot.lastUpdated ? new Date(bot.lastUpdated) : new Date(bot.created);
        const timeAgo = getTimeAgo(lastUpdated);
        
        botCard.setAttribute('draggable', 'true');
        botCard.dataset.botId = bot.id;
        botCard.innerHTML = `
            <div class="bot-header">
                <div class="widget-drag-handle" title="Zum Verschieben ziehen">☰</div>
                <div class="bot-title">
                    <h3>${bot.name}</h3>
                    <span class="bot-status ${bot.status}">
                        ${getStatusIcon(bot.status)} ${bot.status}
                    </span>
                </div>
                <div class="bot-meta">
                    <span title="Zuletzt aktualisiert: ${lastUpdated.toLocaleString()}">
                        ${timeAgo}
                    </span>
                </div>
            </div>
            <div class="bot-info">
                <div class="info-grid">
                    <div class="info-item">
                        <span class="label">Ordner:</span>
                        <span class="value">${bot.folder}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Start-Datei:</span>
                        <span class="value">${bot.start}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Client ID:</span>
                        <span class="value">${bot.clientId}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Commands:</span>
                        <span class="value badge">${bot.commands ? bot.commands.length : 0}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Prefix:</span>
                        <span class="value code">${bot.prefix}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">Erstellt:</span>
                        <span class="value">${new Date(bot.created).toLocaleDateString()}</span>
                    </div>
                </div>
                ${bot.settings ? `
                <div class="bot-settings">
                    <span class="setting ${bot.settings.autoRestart ? 'active' : ''}">
                        🔄 Auto-Restart
                    </span>
                    <span class="setting ${bot.settings.logging ? 'active' : ''}">
                        📝 Logging
                    </span>
                    <span class="setting ${bot.settings.debug ? 'active' : ''}">
                        🔧 Debug
                    </span>
                </div>
                ` : ''}
            </div>
            <div class="bot-actions">
                <div class="action-group primary">
                    <button class="btn btn-primary with-icon" onclick="openBotDetails('${bot.id}')">
                        ⚙️ Verwalten
                    </button>
                    <button class="btn ${bot.status === 'online' ? 'btn-danger' : 'btn-success'} with-icon" 
                            onclick="toggleBotStatus('${bot.id}')">
                        ${bot.status === 'online' ? '⏹️ Stop' : '▶️ Start'}
                    </button>
                </div>
                <div class="action-group secondary">
                    <button class="btn btn-info with-icon" onclick="showBotLogs('${bot.id}')">
                        � Logs
                    </button>
                    <div class="dropdown">
                        <button class="btn btn-secondary">📥 Download</button>
                        <div class="dropdown-content">
                            <a onclick="downloadScript('${bot.id}', 'python')">🐍 Python Script</a>
                            <a onclick="downloadScript('${bot.id}', 'batch')">📝 Batch Script</a>
                            <a onclick="exportBot('${bot.id}')">💾 Bot Config</a>
                        </div>
                    </div>
                    ${bot.invite ? `
                    <a href="${bot.invite}" target="_blank" class="btn btn-primary with-icon">
                        🔗 Einladen
                    </a>
                    ` : ''}
                    <button class="btn btn-danger with-icon" onclick="deleteBot('${bot.id}')">
                        🗑️ Löschen
                    </button>
                </div>
            </div>
        `;
        botList.appendChild(botCard);
    });
    // Initialize drag & drop handlers for widgets (idempotent)
    try {
        initWidgetDragAndDrop();
        // Dispatch event for bot rendering completion
        document.dispatchEvent(new CustomEvent('botsRendered'));
    } catch (e) {
        console.warn('Could not initialize drag-and-drop:', e);
    }
}

function deleteBot(botId) {
    if (!confirm('Möchten Sie diesen Bot wirklich löschen?')) return;
    
    bots = bots.filter(b => b.id !== botId);
    
    if (currentBotId === botId) {
        closeBotDetails();
    }
    
    saveBots();
    renderBots();
    showNotification('Bot gelöscht!', 'success');
}

// ===============================
// FILE GENERATION
// ===============================

function generateBotFiles(bot) {
    if (bot.commandMode === 'single') {
        generateSingleFileBot(bot);
    } else {
        generateMultiFileBot(bot);
    }
    
    // Always generate config and requirements
    bot.files['config.json'] = generateConfigFile(bot);
    bot.files['requirements.txt'] = generateRequirementsFile();
    bot.files['.env.example'] = `# Discord Bot Token\nDISCORD_TOKEN=${bot.token}\n\n# Bot Configuration\nCOMMAND_PREFIX=${bot.prefix}\nCLIENT_ID=${bot.clientId}`;
    
    bot.fileCount = Object.keys(bot.files).length;
}

function generateSingleFileBot(bot) {
    let commandsCode = '';
    
    // Add custom commands
    if (bot.commands && bot.commands.length > 0) {
        commandsCode = bot.commands.map(cmd => cmd.code).join('\n\n');
    }
    
    bot.files['main.py'] = `# ${bot.name} - Created by headx and the psychon
import discord
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ config.json not found!")
    exit(1)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=config.get('prefix', '${bot.prefix}'),
    intents=intents,
    description=config.get('description', '${bot.name} - Discord Bot')
)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ist jetzt online!")
    print(f"Bot ID: {bot.user.id}")
    print(f"Servers: {len(bot.guilds)}")
    print(f"Users: {len(set(bot.get_all_members()))}")
    print("Created by headx and the psychon")
    print("-" * 40)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Command nicht gefunden! Nutze \`{bot.command_prefix}help\` für alle Commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Fehlende Argumente! Nutze \`{bot.command_prefix}help {ctx.command}\`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Du hast nicht die nötigen Berechtigungen!")
    else:
        print(f"Error in {ctx.command}: {error}")
        await ctx.send(f"❌ Ein Fehler ist aufgetreten: {str(error)}")

# Basic Commands
@bot.command(name='ping')
async def ping(ctx):
    """Zeigt die Bot-Latenz an"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Latenz: **{latency}ms**",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

@bot.command(name='info')
async def info(ctx):
    """Bot Informationen anzeigen"""
    embed = discord.Embed(
        title=f"ℹ️ {bot.user.name}",
        description="Discord Bot created by headx and the psychon",
        color=discord.Color.blue()
    )
    embed.add_field(name="Servers", value=len(bot.guilds), inline=True)
    embed.add_field(name="Users", value=len(set(bot.get_all_members())), inline=True)
    embed.add_field(name="Latenz", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="Prefix", value=bot.command_prefix, inline=True)
    embed.set_footer(text="Created by headx and the psychon")
    await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx, *, command=None):
    """Zeigt alle verfügbaren Commands"""
    if command:
        # Show specific command help
        cmd = bot.get_command(command)
        if cmd:
            embed = discord.Embed(
                title=f"📖 Help: {cmd.name}",
                description=cmd.help or "Keine Beschreibung verfügbar",
                color=discord.Color.blue()
            )
            embed.add_field(name="Usage", value=f"\`{bot.command_prefix}{cmd.name} {cmd.signature}\`", inline=False)
        else:
            embed = discord.Embed(
                title="❌ Command nicht gefunden",
                description=f"Command \`{command}\` existiert nicht!",
                color=discord.Color.red()
            )
    else:
        # Show all commands
        embed = discord.Embed(
            title=f"📖 {bot.user.name} - Commands",
            description=f"Prefix: \`{bot.command_prefix}\`",
            color=discord.Color.blue()
        )
        
        for cog_name, cog in bot.cogs.items():
            commands_list = [cmd.name for cmd in cog.get_commands()]
            if commands_list:
                embed.add_field(
                    name=cog_name,
                    value=", ".join(f"\`{cmd}\`" for cmd in commands_list),
                    inline=False
                )
        
        # Add uncategorized commands
        uncategorized = [cmd.name for cmd in bot.commands if not cmd.cog]
        if uncategorized:
            embed.add_field(
                name="Allgemein",
                value=", ".join(f"\`{cmd}\`" for cmd in uncategorized),
                inline=False
            )
        
        embed.set_footer(text=f"Nutze {bot.command_prefix}help <command> für Details")
    
    await ctx.send(embed=embed)

# Custom Commands
${commandsCode}

# Bot Token und Start
if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN') or config.get('token')
    
    if not token:
        print("❌ Kein Bot Token gefunden!")
        print("Setze DISCORD_TOKEN in .env oder token in config.json")
        exit(1)
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ Ungültiger Bot Token!")
    except Exception as e:
        print(f"❌ Fehler beim Starten: {e}")
`;
}

function generateMultiFileBot(bot) {
    // Main file for multi-file structure
    bot.files['main.py'] = `# ${bot.name} - Main File
# Created by headx and the psychon
import discord
from discord.ext import commands
import json
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load configuration
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ config.json not found!")
    exit(1)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=config.get('prefix', '${bot.prefix}'),
    intents=intents,
    description=config.get('description', '${bot.name} - Discord Bot')
)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ist jetzt online!")
    print(f"Bot ID: {bot.user.id}")
    print(f"Servers: {len(bot.guilds)}")
    print(f"Users: {len(set(bot.get_all_members()))}")
    print("Created by headx and the psychon")
    print("-" * 40)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Command nicht gefunden! Nutze \`{bot.command_prefix}help\`")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Fehlende Argumente! Nutze \`{bot.command_prefix}help {ctx.command}\`")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Du hast nicht die nötigen Berechtigungen!")
    else:
        print(f"Error in {ctx.command}: {error}")

# Load Cogs
async def load_cogs():
    """Load all cog files from the cogs directory"""
    if not os.path.exists('./cogs'):
        os.makedirs('./cogs')
        print("📁 Created cogs directory")
        return
    
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'✅ Loaded cog: {filename}')
            except Exception as e:
                print(f'❌ Failed to load {filename}: {e}')

async def main():
    """Main async function"""
    await load_cogs()
    
    token = os.getenv('DISCORD_TOKEN') or config.get('token')
    
    if not token:
        print("❌ Kein Bot Token gefunden!")
        print("Setze DISCORD_TOKEN in .env oder token in config.json")
        return
    
    try:
        await bot.start(token)
    except discord.LoginFailure:
        print("❌ Ungültiger Bot Token!")
    except Exception as e:
        print(f"❌ Fehler beim Starten: {e}")

if __name__ == "__main__":
    asyncio.run(main())
`;

    // Create cogs directory structure
    bot.files['cogs/__init__.py'] = '# Cogs Package';
    
    // Basic commands cog
    bot.files['cogs/basic.py'] = `# Basic Commands Cog - Created by headx and the psychon
import discord
from discord.ext import commands

class BasicCommands(commands.Cog):
    """Grundlegende Bot Commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Zeigt die Bot-Latenz an"""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latenz: **{latency}ms**",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='info')
    async def info(self, ctx):
        """Bot Informationen anzeigen"""
        embed = discord.Embed(
            title=f"ℹ️ {self.bot.user.name}",
            description="Discord Bot created by headx and the psychon",
            color=discord.Color.blue()
        )
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=len(set(self.bot.get_all_members())), inline=True)
        embed.add_field(name="Latenz", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.set_footer(text="Created by headx and the psychon")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(BasicCommands(bot))
`;

    // Add custom command cogs
    if (bot.commands && bot.commands.length > 0) {
        bot.commands.forEach(cmd => {
            if (cmd.category) {
                const cogName = cmd.category.toLowerCase();
                const cogFile = `cogs/${cogName}.py`;
                
                if (!bot.files[cogFile]) {
                    bot.files[cogFile] = generateCogTemplate(cmd.category, bot.name);
                }
                
                // Add command to existing cog
                bot.files[cogFile] += `\n${cmd.code}\n`;
            }
        });
    }
}

function generateCogTemplate(categoryName, botName) {
    return `# ${categoryName} Commands Cog - Created by headx and the psychon
import discord
from discord.ext import commands

class ${categoryName}Commands(commands.Cog):
    """${categoryName} Commands für ${botName}"""
    
    def __init__(self, bot):
        self.bot = bot
`;
}

function generateConfigFile(bot) {
    return JSON.stringify({
        token: "PLACE_TOKEN_IN_ENV_FILE",
        prefix: bot.prefix,
        client_id: bot.clientId,
        description: `${bot.name} - Discord Bot created by headx and the psychon`,
        owner_id: "YOUR_USER_ID_HERE",
        debug: false
    }, null, 2);
}

function generateRequirementsFile() {
    return `discord.py>=2.3.0
python-dotenv>=1.0.0
aiohttp>=3.8.0
asyncio`;
}

// ===============================
// COMMAND BUILDER
// ===============================

function openCommandBuilder(mode) {
    showModal('command-builder-modal');
    
    // Set mode
    commandMode = mode;
    
    // Reset form
    const form = document.getElementById('command-form');
    if (form) {
        form.reset();
    }
}

function closeCommandBuilder() {
    hideModal('command-builder-modal');
}

function addCustomCommand() {
    const name = document.getElementById('cmd-name')?.value;
    const description = document.getElementById('cmd-description')?.value;
    const code = document.getElementById('cmd-code')?.value;
    const category = document.getElementById('cmd-category')?.value;
    
    if (!name || !code) {
        showNotification('Name und Code sind erforderlich!', 'error');
        return;
    }
    
    const newCommand = {
        id: Date.now().toString(),
        name: name,
        description: description,
        code: code,
        category: category || 'Custom',
        mode: commandMode
    };
    
    currentCommands.push(newCommand);
    updateCommandPreview();
    closeCommandBuilder();
    
    showNotification(`Command "${name}" hinzugefügt!`, 'success');
}

function removeCommand(commandId) {
    currentCommands = currentCommands.filter(cmd => cmd.id !== commandId);
    updateCommandPreview();
    showNotification('Command entfernt!', 'success');
}

function updateCommandPreview() {
    const preview = document.getElementById('preview-commands');
    if (!preview) return;
    
    if (currentCommands.length === 0) {
        preview.innerHTML = '<p>Keine Commands hinzugefügt</p>';
        return;
    }
    
    preview.innerHTML = currentCommands.map(cmd => `
        <div class="command-item">
            <div class="command-header">
                <strong>${cmd.name}</strong>
                <button class="btn-small btn-danger" onclick="removeCommand('${cmd.id}')">❌</button>
            </div>
            <p>${cmd.description || 'Keine Beschreibung'}</p>
            <small>Kategorie: ${cmd.category}</small>
        </div>
    `).join('');
}

// ===============================
// TEMPLATE SYSTEM
// ===============================

function loadCommandTemplates() {
    commandTemplates = {
        basic: [
            {
                name: 'ping',
                description: 'Zeigt Bot-Latenz',
                category: 'Basic',
                code: `@bot.command(name='ping')
async def ping(ctx):
    """Zeigt die Bot-Latenz an"""
    latency = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Latenz: {latency}ms')`
            },
            {
                name: 'hello',
                description: 'Begrüßung',
                category: 'Basic',
                code: `@bot.command(name='hello')
async def hello(ctx):
    """Begrüßt den User"""
    await ctx.send(f'👋 Hallo {ctx.author.mention}!')`
            }
        ],
        moderation: [
            {
                name: 'kick',
                description: 'User kicken',
                category: 'Moderation',
                code: `@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Kickt einen User vom Server"""
    await member.kick(reason=reason)
    await ctx.send(f'✅ {member.mention} wurde gekickt!')`
            },
            {
                name: 'clear',
                description: 'Nachrichten löschen',
                category: 'Moderation',
                code: `@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    """Löscht Nachrichten"""
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'✅ {amount} Nachrichten gelöscht!', delete_after=5)`
            }
        ],
        fun: [
            {
                name: '8ball',
                description: 'Magic 8-Ball',
                category: 'Fun',
                code: `@bot.command(name='8ball')
async def eight_ball(ctx, *, question):
    """Magic 8-Ball Antworten"""
    import random
    responses = ['Ja!', 'Nein!', 'Vielleicht...', 'Auf jeden Fall!', 'Niemals!']
    await ctx.send(f'🎱 {random.choice(responses)}')`
            },
            {
                name: 'dice',
                description: 'Würfeln',
                category: 'Fun',
                code: `@bot.command(name='dice')
async def dice(ctx, sides: int = 6):
    """Würfelt einen Würfel"""
    import random
    result = random.randint(1, sides)
    await ctx.send(f'🎲 Du hast eine {result} gewürfelt!')`
            }
        ],
        music: [
            {
                name: 'play',
                description: 'Musik abspielen',
                category: 'Music',
                code: `@bot.command(name='play')
async def play(ctx, *, query):
    """Spielt Musik ab (YouTube-dl erforderlich)"""
    # Hinweis: Requires youtube-dl and PyNaCl
    await ctx.send('🎵 Musik-Feature benötigt zusätzliche Dependencies!')`
            }
        ]
    };
}

function useTemplate(templateName) {
    if (!commandTemplates[templateName]) {
        showNotification('Template nicht gefunden!', 'error');
        return;
    }
    
    // Add all commands from template
    commandTemplates[templateName].forEach(cmd => {
        currentCommands.push({
            id: Date.now().toString() + Math.random(),
            name: cmd.name,
            description: cmd.description,
            category: cmd.category,
            code: cmd.code,
            mode: commandMode
        });
    });
    
    updateCommandPreview();
    showNotification(`Template "${templateName}" hinzugefügt!`, 'success');
    
    // Switch to add-bot tab
    showTab('add-bot');
}

// ===============================
// BOT DETAILS MODAL
// ===============================

function openBotDetails(botId) {
    currentBotId = botId;
    const bot = bots.find(b => b.id === botId);
    if (!bot) return;
    
    showModal('bot-details-modal', {
        title: `Bot Details: ${bot.name}`,
        size: 'large',
        preventEscapeClose: true,
        content: generateBotDetailsContent(bot)
    });

    // Initialize form with bot data
    document.getElementById('edit-bot-name').value = bot.name;
    document.getElementById('edit-bot-folder').value = bot.folder;
    document.getElementById('edit-bot-token').value = bot.token;
    document.getElementById('edit-client-id').value = bot.clientId;
    document.getElementById('edit-start-file').value = bot.start;
    document.getElementById('edit-invite-url').value = bot.invite;
    
    // Load file tree
    loadFileTree(bot);
}

function closeBotDetails() {
    currentBotId = null;
    currentFile = null;
}

// ===============================
// DOWNLOAD FUNCTIONS
// ===============================

function downloadScript(botId, type) {
    const bot = bots.find(b => b.id === botId);
    if (!bot) return;
    
    let content = '';
    let filename = '';
    
    if (type === 'python') {
        filename = `start_${bot.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}.py`;
        content = generatePythonStartScript(bot);
    } else if (type === 'batch') {
        filename = `start_${bot.name.toLowerCase().replace(/[^a-z0-9]/g, '_')}.bat`;
        content = generateBatchStartScript(bot);
    }
    
    downloadFile(filename, content);
}

function generatePythonStartScript(bot) {
    return `#!/usr/bin/env python3
# Start Script für ${bot.name} - Created by headx and the psychon
import os
import sys
import subprocess
import time

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def start_bot():
    """Start the Discord bot"""
    print(f"Starting ${bot.name}...")
    print("Created by headx and the psychon")
    print("-" * 40)
    
    try:
        subprocess.run([sys.executable, "${bot.start}"])
    except KeyboardInterrupt:
        print("\\n⏹️ Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

def main():
    print("=" * 50)
    print(f"  ${bot.name} - Discord Bot Starter")
    print("  Created by headx and the psychon")
    print("=" * 50)
    
    # Change to bot directory
    if "${bot.folder}" != ".":
        if os.path.exists("${bot.folder}"):
            os.chdir("${bot.folder}")
            print(f"📁 Changed to directory: ${bot.folder}")
        else:
            print(f"❌ Directory not found: ${bot.folder}")
            return
    
    # Install requirements if needed
    if os.path.exists("requirements.txt"):
        if not install_requirements():
            input("Press Enter to exit...")
            return
    
    # Start the bot
    while True:
        start_bot()
        
        print("\\n" + "=" * 30)
        print("Bot has stopped!")
        choice = input("Restart? (y/n): ").lower().strip()
        
        if choice != 'y':
            break
        
        print("Restarting in 3 seconds...")
        time.sleep(3)
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
`;
}

function generateBatchStartScript(bot) {
    return `@echo off
REM Start Script für ${bot.name} - Created by headx and the psychon

title ${bot.name} - Discord Bot Starter

echo ================================================
echo   ${bot.name} - Discord Bot Starter
echo   Created by headx and the psychon
echo ================================================
echo.

REM Change to bot directory
if not "${bot.folder}"=="." (
    if exist "${bot.folder}" (
        cd /d "${bot.folder}"
        echo 📁 Changed to directory: ${bot.folder}
    ) else (
        echo ❌ Directory not found: ${bot.folder}
        pause
        exit /b 1
    )
)

REM Install requirements if needed
if exist requirements.txt (
    echo Installing requirements...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error installing requirements!
        pause
        exit /b 1
    )
    echo ✅ Requirements installed successfully!
    echo.
)

:start
echo Starting ${bot.name}...
echo Created by headx and the psychon
echo ----------------------------------------

python ${bot.start}

echo.
echo ==============================
echo Bot has stopped!
set /p restart="Restart? (y/n): "

if /i "%restart%"=="y" (
    echo Restarting in 3 seconds...
    timeout /t 3 /nobreak >nul
    goto start
)

echo 👋 Goodbye!
pause
`;
}

// ===============================
// UTILITY FUNCTIONS
// ===============================

function generateInviteUrl(clientId) {
    if (!clientId) return '';
    return `https://discord.com/api/oauth2/authorize?client_id=${clientId}&permissions=8&scope=bot%20applications.commands`;
}

function updateInvitePreview(clientId) {
    const inviteInput = document.getElementById('bot_invite');
    if (inviteInput && clientId) {
        inviteInput.value = generateInviteUrl(clientId);
    }
}

function saveBots() {
    try {
        localStorage.setItem('discord-bots', JSON.stringify(bots));
    } catch (e) {
        console.error('Error saving bots:', e);
        showNotification('Fehler beim Speichern!', 'error');
    }
}

function downloadFile(filename, content) {
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content));
    element.setAttribute('download', filename);
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    
    showNotification(`${filename} wurde heruntergeladen!`, 'success');
}

// Utility Functions
function getStatusIcon(status) {
    const icons = {
        'online': '🟢',
        'offline': '⚪',
        'error': '🔴',
        'starting': '🟡',
        'stopping': '🟠'
    };
    return icons[status] || '⚪';
}

function getTimeAgo(date) {
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // difference in seconds

    if (diff < 60) return 'Gerade eben';
    if (diff < 3600) return `Vor ${Math.floor(diff / 60)} Minuten`;
    if (diff < 86400) return `Vor ${Math.floor(diff / 3600)} Stunden`;
    if (diff < 2592000) return `Vor ${Math.floor(diff / 86400)} Tagen`;
    return date.toLocaleDateString();
}

function showNotification(message, type = 'info', duration = 3000) {
    let notification = document.getElementById('notification');
    
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.className = 'notification';
        document.body.appendChild(notification);
    }
    
    // Clear any existing timeouts
    if (notification.timeout) {
        clearTimeout(notification.timeout);
    }
    
    // Support for HTML in notifications
    const icon = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    }[type] || 'ℹ️';
    
    notification.innerHTML = `
        <span class="notification-icon">${icon}</span>
        <span class="notification-message">${message}</span>
        ${duration > 3000 ? '<button class="notification-close" onclick="this.parentElement.classList.remove(\'show\')">×</button>' : ''}
    `;
    
    notification.className = `notification ${type} show`;
    
    if (duration !== Infinity) {
        notification.timeout = setTimeout(() => {
            notification.classList.remove('show');
        }, duration);
    }
}

function showModal(modalId, options = {}) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    // Create or update modal content
    if (options.title || options.content) {
        modal.innerHTML = `
            <div class="modal-content ${options.size || ''}">
                <div class="modal-header">
                    <h2>${options.title || ''}</h2>
                    <button class="modal-close" onclick="hideModal('${modalId}')">&times;</button>
                </div>
                <div class="modal-body">
                    ${options.content || ''}
                </div>
                ${options.footer ? `
                    <div class="modal-footer">
                        ${options.footer}
                    </div>
                ` : ''}
            </div>
        `;
    }

    // Add event listeners for custom buttons
    if (options.buttons) {
        options.buttons.forEach(btn => {
            const button = modal.querySelector(`#${btn.id}`);
            if (button) {
                button.addEventListener('click', btn.onClick);
            }
        });
    }

    // Show modal with animation
    modal.style.display = 'flex';
    requestAnimationFrame(() => {
        modal.classList.add('active');
        modal.querySelector('.modal-content')?.classList.add('show');
    });

    // Add close on escape and outside click
    const handleEscape = (e) => {
        if (e.key === 'Escape' && !options.preventEscapeClose) {
            hideModal(modalId);
        }
    };
    
    const handleOutsideClick = (e) => {
        if (!options.preventOutsideClose && e.target === modal) {
            hideModal(modalId);
        }
    };

    document.addEventListener('keydown', handleEscape);
    modal.addEventListener('click', handleOutsideClick);

    // Store cleanup function
    modal.cleanup = () => {
        document.removeEventListener('keydown', handleEscape);
        modal.removeEventListener('click', handleOutsideClick);
    };
}

function hideModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;

    // Run cleanup if exists
    if (modal.cleanup) {
        modal.cleanup();
    }

    // Hide with animation
    modal.querySelector('.modal-content')?.classList.remove('show');
    modal.classList.remove('active');
    
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// Bot Process Management
// ===============================
// LOG VIEWER
// ===============================

async function showBotLogs(botId) {
    const bot = bots.find(b => b.id === botId);
    if (!bot) {
        handleError({
            code: 'LOG_ERROR',
            message: 'Bot nicht gefunden',
            title: 'Log Fehler',
            solution: 'Bitte aktualisieren Sie die Seite und versuchen Sie es erneut.'
        });
        return;
    }

    try {
        const response = await fetch(`server/bot_manager.php?action=logs&botId=${botId}`);
        if (!response.ok) {
            throw {
                code: 'LOG_ERROR',
                message: `Server antwortet mit Status ${response.status}`,
                title: 'Server Fehler',
                solution: 'Überprüfen Sie die Serververbindung und Berechtigungen.'
            };
        }

        const result = await response.json();
        
        if (result.success) {
            if (!result.logs || result.logs.length === 0) {
                showModal('log-viewer-modal', {
                    title: `📝 Logs: ${bot.name}`,
                    size: 'large',
                    content: generateErrorDisplay({
                        title: 'Keine Logs verfügbar',
                        message: 'Für diesen Bot wurden noch keine Logs erstellt.',
                        solution: 'Logs werden erstellt, sobald der Bot gestartet wird.'
                    }),
                    preventEscapeClose: true
                });
                return;
            }

            showModal('log-viewer-modal', {
                title: `📝 Logs: ${bot.name}`,
                size: 'large',
                content: generateLogViewer(result.logs, bot),
                preventEscapeClose: true
            });
            
            // Start auto-refresh for current log if bot is online
            if (bot.status === 'online') {
                startLogAutoRefresh(botId);
            }
        } else {
            throw {
                code: 'LOG_ERROR',
                message: result.message || 'Unbekannter Fehler beim Laden der Logs',
                title: 'Log Fehler',
                solution: 'Überprüfen Sie die Log-Dateiberechtigungen und den Log-Pfad.'
            };
        }
    } catch (error) {
        handleError(error, 'showBotLogs');
        
        showModal('log-viewer-modal', {
            title: `📝 Logs: ${bot.name}`,
            size: 'large',
            content: generateErrorDisplay({
                title: 'Fehler beim Laden der Logs',
                message: error.message || 'Die Logs konnten nicht geladen werden.',
                details: error.stack,
                solution: 'Versuchen Sie die folgenden Schritte:\n1. Überprüfen Sie die Serververbindung\n2. Stellen Sie sicher, dass der Bot-Ordner existiert\n3. Überprüfen Sie die Dateiberechtigungen'
            }),
            preventEscapeClose: true
        });
    }
}

function generateLogViewer(logs, bot) {
    const currentLog = logs.find(log => log.isCurrent);
    const otherLogs = logs.filter(log => !log.isCurrent);
    
    return `
        <div class="log-viewer">
            <div class="log-controls">
                <div class="log-info">
                    <span class="bot-status ${bot.status}">
                        ${getStatusIcon(bot.status)} ${bot.status}
                    </span>
                    <select id="log-file-selector" onchange="changeLogFile('${bot.id}', this.value)">
                        ${currentLog ? `
                            <option value="${currentLog.path}" selected>
                                Aktuelles Log (${currentLog.date})
                            </option>
                        ` : ''}
                        ${otherLogs.map(log => `
                            <option value="${log.path}">
                                ${log.file} (${log.date})
                            </option>
                        `).join('')}
                    </select>
                </div>
                <div class="log-actions">
                    <button class="btn btn-secondary" onclick="downloadLog('${currentLog?.path}')">
                        📥 Download
                    </button>
                    <button class="btn btn-warning" onclick="clearLog('${bot.id}', '${currentLog?.path}')">
                        🗑️ Leeren
                    </button>
                    <div class="auto-scroll">
                        <input type="checkbox" id="auto-scroll" checked>
                        <label for="auto-scroll">Auto-Scroll</label>
                    </div>
                </div>
            </div>
            <div class="log-content" id="log-content">
                <pre>${currentLog ? formatLogContent(currentLog.content) : 'Keine Logs verfügbar'}</pre>
            </div>
        </div>
    `;
}

function formatLogContent(content) {
    if (!content) return '';
    
    // Colorize log levels
    return content
        .replace(/\[ERROR\]/g, '<span class="log-error">[ERROR]</span>')
        .replace(/\[WARN\]/g, '<span class="log-warn">[WARN]</span>')
        .replace(/\[INFO\]/g, '<span class="log-info">[INFO]</span>')
        .replace(/\[DEBUG\]/g, '<span class="log-debug">[DEBUG]</span>');
}

let logRefreshInterval = null;

function startLogAutoRefresh(botId) {
    if (logRefreshInterval) {
        clearInterval(logRefreshInterval);
    }
    
    logRefreshInterval = setInterval(async () => {
        const response = await fetch(`server/bot_manager.php?action=logs&botId=${botId}&limit=100`);
        const result = await response.json();
        
        if (result.success) {
            const currentLog = result.logs.find(log => log.isCurrent);
            if (currentLog) {
                const logContent = document.querySelector('#log-content pre');
                if (logContent) {
                    logContent.innerHTML = formatLogContent(currentLog.content);
                    
                    // Auto-scroll if enabled
                    const autoScroll = document.getElementById('auto-scroll');
                    if (autoScroll?.checked) {
                        logContent.scrollTop = logContent.scrollHeight;
                    }
                }
            }
        }
    }, 1000);
}

async function changeLogFile(botId, logPath) {
    try {
        const response = await fetch(`server/bot_manager.php?action=logs&botId=${botId}&file=${logPath}`);
        const result = await response.json();
        
        if (result.success) {
            const logContent = document.querySelector('#log-content pre');
            if (logContent) {
                logContent.innerHTML = formatLogContent(result.logs[0].content);
            }
        }
    } catch (error) {
        console.error('Error changing log file:', error);
        showNotification('Fehler beim Laden der Log-Datei', 'error');
    }
}

function downloadLog(logPath) {
    if (!logPath) return;
    
    fetch(`server/bot_manager.php?action=download&file=${encodeURIComponent(logPath)}`)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = logPath.split('/').pop();
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        })
        .catch(error => {
            console.error('Error downloading log:', error);
            showNotification('Fehler beim Herunterladen der Log-Datei', 'error');
        });
}

async function clearLog(botId, logPath) {
    if (!confirm('Möchten Sie wirklich die Log-Datei leeren?')) return;
    
    try {
        const formData = new FormData();
        formData.append('botId', botId);
        formData.append('logPath', logPath);
        
        const response = await fetch('server/bot_manager.php?action=clear_log', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            const logContent = document.querySelector('#log-content pre');
            if (logContent) {
                logContent.innerHTML = '';
            }
            showNotification('Log-Datei geleert', 'success');
        } else {
            showNotification(`Fehler beim Leeren der Log-Datei: ${result.message}`, 'error');
        }
    } catch (error) {
        console.error('Error clearing log:', error);
        showNotification('Fehler beim Leeren der Log-Datei', 'error');
    }
}

// Error Handling
function handleError(error, context = '') {
    console.error(`Error in ${context}:`, error);
    
    let errorMessage = 'Ein Fehler ist aufgetreten';
    
    if (error.response) {
        // Server returned an error response
        errorMessage = `Server Fehler: ${error.response.data?.message || error.response.statusText}`;
    } else if (error.request) {
        // Request was made but no response received
        errorMessage = 'Keine Antwort vom Server erhalten';
    } else if (error.code === 'INVALID_ACTION') {
        // Invalid action error
        errorMessage = `Ungültige Aktion: ${error.message}`;
    } else if (error.code === 'LOG_ERROR') {
        // Log-related error
        errorMessage = `Fehler beim Laden der Logs: ${error.message}`;
    } else {
        // Other errors
        errorMessage = error.message || 'Unbekannter Fehler';
    }
    
    showNotification(errorMessage, 'error', 5000);
}

// Generate Error Display
function generateErrorDisplay(error) {
    return `
        <div class="error-message">
            <i class="error-icon">❌</i>
            <div class="error-content">
                <div class="error-title">${error.title || 'Fehler'}</div>
                <div class="error-description">${error.message}</div>
                ${error.details ? `
                    <div class="error-details">
                        <pre>${error.details}</pre>
                    </div>
                ` : ''}
                ${error.solution ? `
                    <div class="error-solution">
                        💡 ${error.solution}
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Clean up on modal close
document.addEventListener('closeModal', (event) => {
    if (event.detail.modalId === 'log-viewer-modal') {
        if (logRefreshInterval) {
            clearInterval(logRefreshInterval);
            logRefreshInterval = null;
        }
    }
});

// ===============================
// BOT PROCESS MANAGEMENT
// ===============================

async function toggleBotStatus(botId) {
    const bot = bots.find(b => b.id === botId);
    if (!bot) return;

    if (bot.status === 'online') {
        // Stop the bot
        stopBot(bot);
    } else {
        // Start the bot
        startBot(bot);
    }
}

async function startBot(bot) {
    if (bot.status === 'starting' || bot.status === 'online') return;
    
    try {
        // Update status to starting
        bot.status = 'starting';
        bot.lastUpdated = new Date().toISOString();
        saveBots();
        renderBots();

        // Save bots data to server
        const formData = new FormData();
        formData.append('botId', bot.id);
        
        const response = await fetch('server/bot_manager.php?action=start', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();

        if (result.success) {
            bot.status = 'online';
            bot.processId = result.pid;
            bot.currentLog = result.logFile;
            showNotification(`Bot ${bot.name} gestartet!`, 'success');
        } else {
            bot.status = 'error';
            showNotification(`Fehler beim Starten von ${bot.name}: ${result.message}`, 'error');
        }
    } catch (error) {
        console.error('Error starting bot:', error);
        bot.status = 'error';
        showNotification(`Fehler beim Starten von ${bot.name}: ${error.message}`, 'error');
    }

    bot.lastUpdated = new Date().toISOString();
    saveBots();
    renderBots();
}

async function stopBot(bot) {
    if (bot.status === 'stopping' || bot.status === 'offline') return;

    try {
        // Update status to stopping
        bot.status = 'stopping';
        bot.lastUpdated = new Date().toISOString();
        saveBots();
        renderBots();

        const formData = new FormData();
        formData.append('botId', bot.id);
        
        const response = await fetch('server/bot_manager.php?action=stop', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.success) {
            bot.processId = null;
            bot.status = 'offline';
            showNotification(`Bot ${bot.name} gestoppt!`, 'success');
        } else {
            bot.status = 'error';
            showNotification(`Fehler beim Stoppen von ${bot.name}: ${result.message}`, 'error');
        }
    } catch (error) {
        console.error('Error stopping bot:', error);
        bot.status = 'error';
        showNotification(`Fehler beim Stoppen von ${bot.name}: ${error.message}`, 'error');
    }

    bot.lastUpdated = new Date().toISOString();
    saveBots();
    renderBots();
}

function showConfirmModal(message, onConfirm, onCancel = null) {
    showModal('confirm-modal', {
        title: 'Bestätigung',
        content: `<p>${message}</p>`,
        footer: `
            <button id="confirm-yes" class="btn btn-danger">Ja</button>
            <button id="confirm-no" class="btn btn-secondary">Nein</button>
        `,
        buttons: [
            {
                id: 'confirm-yes',
                onClick: () => {
                    hideModal('confirm-modal');
                    onConfirm();
                }
            },
            {
                id: 'confirm-no',
                onClick: () => {
                    hideModal('confirm-modal');
                    if (onCancel) onCancel();
                }
            }
        ]
    });
}

// ===============================
// MODAL MANAGEMENT
// ===============================

function openAddBot() {
    showModal('add-bot-modal');
}

function closeAddBot() {
    hideModal('add-bot-modal');
    
    // Reset form
    const form = document.getElementById('add-bot-form');
    if (form) {
        form.reset();
    }
    
    // Clear current commands
    currentCommands = [];
    updateCommandPreview();
}

// ===============================
// FILE MANAGEMENT (for bot details)
// ===============================

function loadFileTree(bot) {
    const fileTree = document.getElementById('file-tree');
    if (!fileTree) return;
    
    fileTree.innerHTML = '';
    
    Object.keys(bot.files).forEach(filename => {
        const fileItem = document.createElement('div');
        fileItem.classList.add('file-item');
        fileItem.innerHTML = `
            <span onclick="loadFile('${filename}')" class="file-name">
                📄 ${filename}
            </span>
            <button onclick="deleteFile('${filename}')" class="btn-small btn-danger">
                ❌
            </button>
        `;
        fileTree.appendChild(fileItem);
    });
}

function loadFile(filename) {
    if (!currentBotId) return;
    
    const bot = bots.find(b => b.id === currentBotId);
    if (!bot || !bot.files[filename]) return;
    
    currentFile = filename;
    const currentFileSpan = document.getElementById('current-file-name');
    const fileEditor = document.getElementById('file-editor');
    
    if (currentFileSpan) {
        currentFileSpan.textContent = filename;
    }
    
    if (fileEditor) {
        fileEditor.value = bot.files[filename];
    }
    
    // Highlight selected file
    document.querySelectorAll('.file-item').forEach(item => {
        item.classList.remove('selected');
    });
    
    event.target.closest('.file-item')?.classList.add('selected');
}

function saveFile() {
    if (!currentBotId || !currentFile) {
        showNotification('Keine Datei ausgewählt!', 'error');
        return;
    }
    
    const bot = bots.find(b => b.id === currentBotId);
    const fileEditor = document.getElementById('file-editor');
    
    if (!bot || !fileEditor) return;
    
    bot.files[currentFile] = fileEditor.value;
    saveBots();
    
    showNotification(`Datei ${currentFile} gespeichert!`, 'success');
}

function createNewFile() {
    if (!currentBotId) return;
    
    const filenameInput = document.getElementById('new-file-name');
    if (!filenameInput) return;
    
    const filename = filenameInput.value.trim();
    if (!filename) {
        showNotification('Dateiname eingeben!', 'error');
        return;
    }
    
    const bot = bots.find(b => b.id === currentBotId);
    if (!bot) return;
    
    if (bot.files[filename]) {
        showNotification('Datei existiert bereits!', 'error');
        return;
    }
    
    bot.files[filename] = `# ${filename} - Created by headx and the psychon\n# Neue Datei\n`;
    bot.fileCount = Object.keys(bot.files).length;
    
    loadFileTree(bot);
    loadFile(filename);
    
    filenameInput.value = '';
    saveBots();
    
    showNotification(`Datei ${filename} erstellt!`, 'success');
}

function deleteFile(filename) {
    if (!currentBotId) return;
    if (!confirm(`Datei ${filename} wirklich löschen?`)) return;
    
    const bot = bots.find(b => b.id === currentBotId);
    if (!bot) return;
    
    delete bot.files[filename];
    bot.fileCount = Object.keys(bot.files).length;
    
    if (currentFile === filename) {
        currentFile = null;
        const currentFileSpan = document.getElementById('current-file-name');
        const fileEditor = document.getElementById('file-editor');
        
        if (currentFileSpan) {
            currentFileSpan.textContent = 'Keine Datei ausgewählt';
        }
        
        if (fileEditor) {
            fileEditor.value = '';
        }
    }
    
    loadFileTree(bot);
    saveBots();
    
    showNotification(`Datei ${filename} gelöscht!`, 'success');
}

// ===============================
// TOKEN VALIDATION
// ===============================

function validateBotToken(token) {
    // Accept any token input
    return true;
}

function validateClientId(clientId) {
    // Discord client ID is typically 17-19 digits
    const clientIdRegex = /^\d{17,19}$/;
    return clientIdRegex.test(clientId);
}

// ===============================
// ADVANCED COMMAND BUILDER
// ===============================

function createCommandFromTemplate(template) {
    return {
        id: Date.now().toString() + Math.random(),
        name: template.name,
        description: template.description,
        category: template.category,
        code: template.code,
        mode: commandMode
    };
}

function editCommand(commandId) {
    const command = currentCommands.find(cmd => cmd.id === commandId);
    if (!command) return;
    
    // Populate edit form
    document.getElementById('cmd-name').value = command.name;
    document.getElementById('cmd-description').value = command.description;
    document.getElementById('cmd-code').value = command.code;
    document.getElementById('cmd-category').value = command.category;
    
    // Remove from current commands (will be re-added when saved)
    removeCommand(commandId);
    
    openCommandBuilder(commandMode);
}

// ===============================
// EXPORT FUNCTIONS
// ===============================

function exportBot(botId) {
    const bot = bots.find(b => b.id === botId);
    if (!bot) return;
    
    const exportData = {
        ...bot,
        exportedAt: new Date().toISOString(),
        exportedBy: 'headx and the psychon Discord Bot Manager'
    };
    
    const jsonString = JSON.stringify(exportData, null, 2);
    downloadFile(`${bot.name}_export.json`, jsonString);
}

function importBot(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const importedBot = JSON.parse(e.target.result);
            
            // Generate new ID to avoid conflicts
            importedBot.id = Date.now().toString();
            importedBot.imported = true;
            importedBot.importedAt = new Date().toISOString();
            
            bots.push(importedBot);
            saveBots();
            renderBots();
            
            showNotification(`Bot "${importedBot.name}" importiert!`, 'success');
        } catch (error) {
            showNotification('Fehler beim Importieren!', 'error');
        }
    };
    reader.readAsText(file);
}

// ===============================
// GLOBAL EXPORT
// ===============================

// Export functions for global access
window.DiscordBotManager = {
    // Core functions
    bots,
    renderBots,
    showTab,
    
    // Bot management
    openAddBot,
    closeAddBot,
    deleteBot,
    openBotDetails,
    closeBotDetails,
    toggleBotStatus,
    
    // Command management
    switchCommandMode,
    openCommandBuilder,
    closeCommandBuilder,
    addCustomCommand,
    removeCommand,
    useTemplate,
    
    // File management
    loadFile,
    saveFile,
    createNewFile,
    deleteFile,
    
    // Download functions
    downloadScript,
    exportBot,
    importBot,
    
    // Utilities
    showNotification,
    saveBots
};

console.log("Enhanced Discord Bot Manager loaded successfully!");
console.log("Created by headx and the psychon");