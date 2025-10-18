// Discord OAuth2 Authentication Handler
// Created by headx & the psychon

let currentUser = null;
let isAuthenticated = false;

// ===============================
// AUTHENTICATION FUNCTIONS
// ===============================

async function checkAuthStatus() {
    try {
        const response = await fetch('/api/user');
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            isAuthenticated = true;
            updateUIForAuthenticatedUser(data.user);
        } else {
            currentUser = null;
            isAuthenticated = false;
            updateUIForUnauthenticatedUser();
        }
        
        return data.authenticated;
    } catch (error) {
        console.error('Error checking auth status:', error);
        return false;
    }
}

function updateUIForAuthenticatedUser(user) {
    // Show user info
    const userInfo = document.getElementById('user-info');
    const loginBtn = document.getElementById('login-btn');
    
    if (userInfo && loginBtn) {
        const avatarUrl = user.avatar 
            ? `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`
            : `https://cdn.discordapp.com/embed/avatars/${parseInt(user.discriminator) % 5}.png`;
        
        document.getElementById('user-avatar').src = avatarUrl;
        document.getElementById('user-name').textContent = `${user.username}#${user.discriminator}`;
        
        userInfo.style.display = 'flex';
        loginBtn.style.display = 'none';
    }
    
    // Show Discord apps tab content
    const authRequiredMessage = document.getElementById('auth-required-message');
    const discordAppsList = document.getElementById('discord-apps-list');
    
    if (authRequiredMessage && discordAppsList) {
        authRequiredMessage.style.display = 'none';
        discordAppsList.style.display = 'block';
        
        // Load Discord applications
        loadDiscordApplications();
    }
}

function updateUIForUnauthenticatedUser() {
    const userInfo = document.getElementById('user-info');
    const loginBtn = document.getElementById('login-btn');
    
    if (userInfo && loginBtn) {
        userInfo.style.display = 'none';
        loginBtn.style.display = 'inline-flex';
    }
    
    // Hide Discord apps list, show auth required message
    const authRequiredMessage = document.getElementById('auth-required-message');
    const discordAppsList = document.getElementById('discord-apps-list');
    
    if (authRequiredMessage && discordAppsList) {
        authRequiredMessage.style.display = 'flex';
        discordAppsList.style.display = 'none';
    }
}

async function loginWithDiscord() {
    try {
        // Show the button is working
        const loginButtons = document.querySelectorAll('.discord-login-button');
        loginButtons.forEach(btn => {
            btn.disabled = true;
            btn.innerHTML = `<svg class="spin" width="20" height="20" viewBox="0 0 71 55" fill="currentColor">...</svg> Verbinde...`;
        });

        // Try to fetch login URL from backend
        let authUrl = null;
        try {
            const response = await fetch('/auth/login');
            // First try parsing as JSON
            const data = await response.json();
            if (data.auth_url) {
                authUrl = data.auth_url;
            }
        } catch (e) {
            // If JSON parsing fails, try to get URL from response text
            try {
                const response2 = await fetch('/auth/login');
                const text = await response2.text();
                // Look for a URL in the text that contains "discord.com/oauth2/authorize"
                const match = text.match(/https:\/\/discord\.com\/oauth2\/authorize[^"'\s]*/);
                if (match) {
                    authUrl = match[0];
                } else if (text.startsWith('http')) {
                    // If it's just a URL directly
                    authUrl = text.trim();
                }
            } catch (e2) {
                console.warn('Could not parse auth URL from text response:', e2);
            }
        }

        // If we found a URL, redirect to it
        if (authUrl) {
            window.location.href = authUrl;
            return;
        }

        // Last resort: construct and try direct Discord OAuth2 URL
        const clientId = '123456789'; // This should match your Discord Application's client ID
        const redirectUri = encodeURIComponent(window.location.origin + '/auth/callback');
        const scope = encodeURIComponent('identify guilds applications.commands bot');
        const directAuthUrl = `https://discord.com/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}`;

        window.location.href = directAuthUrl;
    } catch (error) {
        console.error('Error in Discord login flow:', error);
        showNotification('Fehler beim Anmelden. Versuche es später erneut.', 'error');
    } finally {
        // Re-enable buttons if we somehow haven't redirected
        const loginButtons = document.querySelectorAll('.discord-login-button');
        loginButtons.forEach(btn => {
            btn.disabled = false;
            btn.innerHTML = `<svg width="20" height="20" viewBox="0 0 71 55" fill="currentColor">...</svg> Mit Discord anmelden`;
        });
    }
}

async function logout() {
    try {
        await fetch('/auth/logout');
        currentUser = null;
        isAuthenticated = false;
        updateUIForUnauthenticatedUser();
        showNotification('Erfolgreich abgemeldet', 'success');
        
        // Redirect to home
        window.location.href = '/';
    } catch (error) {
        console.error('Error logging out:', error);
        showNotification('Fehler beim Abmelden', 'error');
    }
}

// ===============================
// DISCORD APPLICATIONS
// ===============================

async function loadDiscordApplications() {
    try {
        showLoadingState();
        
        const response = await fetch('/api/discord/applications');
        const data = await response.json();
        
        if (data.error) {
            showNotification(data.error, 'error');
            return;
        }
        
        renderDiscordApplications(data.applications || []);
    } catch (error) {
        console.error('Error loading Discord applications:', error);
        showNotification('Fehler beim Laden der Discord-Anwendungen', 'error');
    }
}

function renderDiscordApplications(applications) {
    const appsGrid = document.getElementById('apps-grid');
    if (!appsGrid) return;
    
    if (applications.length === 0) {
        appsGrid.innerHTML = `
            <div class="no-apps">
                <h3>Keine Discord Applications gefunden</h3>
                <paragraph>Erstellen Sie eine neue Application im Discord Developer Portal:</paragraph>
                <a href="https://discord.com/developers/applications" target="_blank" class="button button-primary">
                    🔗 Discord Developer Portal öffnen
                </a>
            </div>
        `;
        return;
    }
    
    appsGrid.innerHTML = applications.map(app => {
        const iconUrl = app.icon 
            ? `https://cdn.discordapp.com/app-icons/${app.id}/${app.icon}.png`
            : 'https://cdn.discordapp.com/embed/avatars/0.png';
        
        const isBot = app.bot_public || app.bot_require_code_grant !== undefined;
        
        return `
            <div class="discord-app-card">
                <div class="app-icon">
                    <img src="${iconUrl}" alt="${app.name}" onerror="this.src='https://cdn.discordapp.com/embed/avatars/0.png'">
                </div>
                <div class="app-info">
                    <h4>${app.name}</h4>
                    <p class="app-id">ID: ${app.id}</p>
                    ${app.description ? `<p class="app-description">${app.description}</p>` : ''}
                    ${isBot ? '<span class="app-badge bot-badge">🤖 Bot</span>' : ''}
                </div>
                <div class="app-actions">
                    <button class="button button-success" onclick="importDiscordApp('${app.id}', '${app.name}')">
                        📥 Importieren
                    </button>
                    <a href="https://discord.com/developers/applications/${app.id}" target="_blank" class="button button-secondary">
                        ⚙️ Bearbeiten
                    </a>
                </div>
            </div>
        `;
    }).join('');
}

async function importDiscordApp(appId, appName) {
    try {
        showNotification('Bot wird importiert...', 'info', 2000);
        
        // Check if bot already exists
        const existingBot = bots.find(b => b.clientId === appId);
        if (existingBot) {
            showNotification(`Bot "${appName}" ist bereits vorhanden!`, 'warning');
            showTab('overview');
            return;
        }
        
        // Get bot token (this will require additional permission or manual input)
        const token = await promptForBotToken(appName);
        if (!token) {
            showNotification('Bot-Import abgebrochen', 'info');
            return;
        }
        
        // Create bot with Discord app data
        const newBot = {
            id: Date.now().toString(),
            name: appName,
            token: token,
            clientId: appId,
            folder: `bot_${Date.now()}`,
            start: 'main.py',
            invite: generateInviteUrl(appId),
            prefix: '!',
            commands: [],
            commandMode: 'single',
            files: {},
            created: new Date().toISOString(),
            status: 'offline',
            lastUpdated: new Date().toISOString(),
            settings: {
                autoRestart: false,
                logging: true,
                debug: false
            },
            importedFromDiscord: true
        };
        
        // Generate bot files
        generateBotFiles(newBot);
        
        // Add to bots array
        bots.push(newBot);
        saveBots();
        renderBots();
        
        showNotification(`Bot "${appName}" erfolgreich importiert!`, 'success');
        showTab('overview');
        
    } catch (error) {
        console.error('Error importing Discord app:', error);
        showNotification('Fehler beim Importieren des Bots', 'error');
    }
}

async function promptForBotToken(appName) {
    return new Promise((resolve) => {
        const modal = document.createElement('div');
        modal.className = 'modal active';
        modal.innerHTML = `
            <div class="modal-content show">
                <div class="modal-header">
                    <h2>🔐 Bot Token eingeben</h2>
                </div>
                <div class="modal-body">
                    <p>Bitte geben Sie den Bot-Token für <strong>${appName}</strong> ein:</p>
                    <p class="help-text">Den Token finden Sie im Discord Developer Portal unter "Bot" → "Token"</p>
                    
                    <div class="form-group">
                        <label for="import-token">Bot Token *</label>
                        <div class="input-group">
                            <input type="password" id="import-token" class="form-control" placeholder="MTE5..." autofocus>
                            <button type="button" class="button button-secondary" onclick="toggleImportTokenVisibility()">👁️</button>
                        </div>
                        <small>Ihr Token wird sicher lokal gespeichert</small>
                    </div>
                    
                    <div class="form-actions">
                        <button class="button button-secondary" onclick="this.closest('.modal').remove(); window.resolveTokenPrompt(null)">
                            Abbrechen
                        </button>
                        <button class="button button-primary" onclick="submitImportToken()">
                            Bot importieren
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        document.getElementById('import-token').focus();
        
        // Store resolve function globally for button access
        window.resolveTokenPrompt = (token) => {
            modal.remove();
            delete window.resolveTokenPrompt;
            delete window.submitImportToken;
            delete window.toggleImportTokenVisibility;
            resolve(token);
        };
        
        // Submit token
        window.submitImportToken = () => {
            const token = document.getElementById('import-token').value.trim();
            if (!token) {
                showNotification('Bitte geben Sie einen Token ein', 'error');
                return;
            }
            window.resolveTokenPrompt(token);
        };
        
        // Toggle visibility
        window.toggleImportTokenVisibility = () => {
            const input = document.getElementById('import-token');
            const button = event.target;
            if (input.type === 'password') {
                input.type = 'text';
                button.textContent = '👁️‍🗨️';
            } else {
                input.type = 'password';
                button.textContent = '👁️';
            }
        };
        
        // Allow Enter key to submit
        document.getElementById('import-token').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                window.submitImportToken();
            }
        });
    });
}

async function refreshDiscordApps() {
    showNotification('Aktualisiere Discord Applications...', 'info', 1000);
    await loadDiscordApplications();
    showNotification('Applications aktualisiert!', 'success');
}

// ===============================
// UTILITY FUNCTIONS
// ===============================

function showLoadingState() {
    const appsGrid = document.getElementById('apps-grid');
    if (appsGrid) {
        appsGrid.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>Lade Discord Applications...</p>
            </div>
        `;
    }
}

function getDiscordAvatarUrl(userId, avatarHash, discriminator) {
    if (avatarHash) {
        return `https://cdn.discordapp.com/avatars/${userId}/${avatarHash}.png`;
    }
    return `https://cdn.discordapp.com/embed/avatars/${parseInt(discriminator) % 5}.png`;
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAuthStatus);
} else {
    checkAuthStatus();
}

console.log("Discord OAuth2 Authentication Handler loaded - by headx & the psychon");
