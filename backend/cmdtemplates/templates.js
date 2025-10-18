// Command Templates Manager
let activeTab = 'overview';
const templates = {
    moderation: [
        { name: 'kick', description: 'Kick user from server' },
        { name: 'ban', description: 'Ban user from server' },
        { name: 'mute', description: 'Mute user in server' }
    ],
    fun: [
        { name: 'dice', description: 'Roll a dice' },
        { name: '8ball', description: 'Magic 8-ball answers' },
        { name: 'meme', description: 'Get random meme' }
    ],
    utility: [
        { name: 'userinfo', description: 'Show user information' },
        { name: 'serverinfo', description: 'Show server information' },
        { name: 'weather', description: 'Show weather information' }
    ],
    music: [
        { name: 'play', description: 'Play a song' },
        { name: 'queue', description: 'Show current queue' },
        { name: 'skip', description: 'Skip current song' }
    ]
};

function initializeTemplates() {
    // Hide all template sections initially
    Object.keys(templates).forEach(category => {
        const section = document.getElementById(`${category}-templates`);
        if (section) {
            section.style.display = 'none';
        }
    });

    // Show only the active tab's templates
    showTemplateSection(activeTab);

    // Add click handlers to all tab buttons
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const tabName = tab.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Update active tab
    activeTab = tabName;

    // Update tab button states
    document.querySelectorAll('.nav-tab').forEach(tab => {
        if (tab.getAttribute('data-tab') === tabName) {
            tab.classList.add('active');
        } else {
            tab.classList.remove('active');
        }
    });

    // Show corresponding template section
    showTemplateSection(tabName);
}

function showTemplateSection(tabName) {
    // Hide all template sections first
    Object.keys(templates).forEach(category => {
        const section = document.getElementById(`${category}-templates`);
        if (section) {
            section.style.display = 'none';
        }
    });

    // Show only the templates for the active tab
    const activeSection = document.getElementById(`${tabName}-templates`);
    if (activeSection) {
        activeSection.style.display = 'block';
        
        // Add animation
        activeSection.style.animation = 'fadeIn 0.3s ease-in-out forwards';
    }
}

// Initialize when the document is loaded
document.addEventListener('DOMContentLoaded', initializeTemplates);
