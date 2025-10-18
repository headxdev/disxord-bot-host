// Error handling and notification system
class ErrorHandler {
    constructor() {
        this.notificationTimeout = null;
    }
    
    /**
     * Display an error message to the user
     * @param {Object} error - Error object from server
     * @param {string} context - Context where the error occurred
     */
    handleError(error, context = '') {
        console.error(`Error in ${context}:`, error);
        
        // Clear any existing notification
        if (this.notificationTimeout) {
            clearTimeout(this.notificationTimeout);
        }
        
        let errorMessage = error.message || 'Ein unbekannter Fehler ist aufgetreten';
        let errorDetails = error.details || '';
        let errorSuggestion = error.suggestion || '';
        
        // Create error notification content
        const content = `
            <div class="error-notification">
                <div class="error-header">
                    <i class="error-icon">❌</i>
                    <span class="error-title">${errorMessage}</span>
                </div>
                ${errorDetails ? `
                    <div class="error-details">
                        ${errorDetails}
                    </div>
                ` : ''}
                ${errorSuggestion ? `
                    <div class="error-suggestion">
                        <i class="suggestion-icon">💡</i>
                        ${errorSuggestion}
                    </div>
                ` : ''}
            </div>
        `;
        
        // Show error in notification
        this.showNotification(content, 'error');
        
        // For critical errors, show in modal
        if (error.code === 'CRITICAL_ERROR') {
            this.showErrorModal(error);
        }
    }
    
    /**
     * Show a notification message
     * @param {string} message - Message to display
     * @param {string} type - Type of notification (success, error, warning, info)
     * @param {number} duration - How long to show the notification (ms)
     */
    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('notification-container') || this.createNotificationContainer();
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = message;
        
        // Add close button
        const closeBtn = document.createElement('button');
        closeBtn.className = 'notification-close';
        closeBtn.innerHTML = '✕';
        closeBtn.onclick = () => notification.remove();
        notification.appendChild(closeBtn);
        
        container.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        });
        
        // Auto remove after duration
        this.notificationTimeout = setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, duration);
    }
    
    /**
     * Create notification container if it doesn't exist
     */
    createNotificationContainer() {
        const container = document.createElement('div');
        container.id = 'notification-container';
        document.body.appendChild(container);
        return container;
    }
    
    /**
     * Show error in modal for critical errors
     * @param {Object} error - Error object
     */
    showErrorModal(error) {
        showModal('error-modal', {
            title: 'Kritischer Fehler',
            content: `
                <div class="error-modal-content">
                    <div class="error-icon-large">❌</div>
                    <h3>${error.message}</h3>
                    ${error.details ? `<p class="error-details">${error.details}</p>` : ''}
                    ${error.suggestion ? `
                        <div class="error-suggestion">
                            <strong>Vorschlag zur Behebung:</strong>
                            <p>${error.suggestion}</p>
                        </div>
                    ` : ''}
                    ${error.code ? `<code class="error-code">Fehlercode: ${error.code}</code>` : ''}
                    <div class="error-actions">
                        <button class="btn btn-primary" onclick="location.reload()">
                            🔄 Seite neu laden
                        </button>
                        <button class="btn btn-secondary" onclick="closeModal('error-modal')">
                            Schließen
                        </button>
                    </div>
                </div>
            `,
            preventEscapeClose: true,
            size: 'medium'
        });
    }
    
    /**
     * Format error details for display
     * @param {string} details - Error details
     * @returns {string} Formatted HTML
     */
    formatErrorDetails(details) {
        if (!details) return '';
        
        // Check if it's a stack trace
        if (details.includes('\n')) {
            return `<pre class="error-stack">${details}</pre>`;
        }
        
        return `<p>${details}</p>`;
    }
}

// Create global error handler instance
const errorHandler = new ErrorHandler();

// Add global error catching
window.addEventListener('error', (event) => {
    errorHandler.handleError({
        code: 'RUNTIME_ERROR',
        message: 'JavaScript Fehler',
        details: event.error?.stack || event.message,
        suggestion: 'Bitte laden Sie die Seite neu und versuchen Sie es erneut'
    });
});

// Add global promise rejection handling
window.addEventListener('unhandledrejection', (event) => {
    errorHandler.handleError({
        code: 'PROMISE_ERROR',
        message: 'Unbehandelte Promise-Ablehnung',
        details: event.reason?.stack || event.reason,
        suggestion: 'Ein asynchroner Vorgang ist fehlgeschlagen'
    });
});