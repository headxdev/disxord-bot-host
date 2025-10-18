// Draggable Widgets System
// Created by headx & the psychon

function initWidgetDragAndDrop() {
    // Target containers that should support draggable widgets
    const containers = [
        document.getElementById('bot-list'),
        document.querySelector('.template-grid'),
        document.querySelector('.editor-area')
    ].filter(container => container);

    containers.forEach(container => {
        // Get all draggable widgets in this container
        const widgets = container.querySelectorAll('.bot-card, .template-card, .editor-panel');
        
        widgets.forEach(widget => {
            // Only initialize drag handlers for widgets that haven't been initialized
            if (widget.dataset.dragInitialized) return;

            // Find or create drag handle
            let dragHandle = widget.querySelector('.widget-drag-handle');
            if (!dragHandle) {
                dragHandle = document.createElement('div');
                dragHandle.className = 'widget-drag-handle';
                dragHandle.innerHTML = '☰';
                dragHandle.title = 'Verschieben';
                widget.insertBefore(dragHandle, widget.firstChild);
            }

            // Store initial position
            let startX, startY, initialX, initialY;
            let isDragging = false;

            // Track current position
            let currentX = 0;
            let currentY = 0;

            // Create a placeholder element
            const placeholder = document.createElement('div');
            placeholder.className = 'drag-placeholder';
            placeholder.style.display = 'none';
            placeholder.style.width = widget.offsetWidth + 'px';
            placeholder.style.height = widget.offsetHeight + 'px';

            dragHandle.addEventListener('mousedown', startDragging);
            dragHandle.addEventListener('touchstart', startDragging);

            function startDragging(e) {
                // Ignore if this is a button
                if (e.target.tagName === 'BUTTON') return;
                
                isDragging = true;
                widget.classList.add('dragging');
                
                // Get initial cursor/touch position
                if (e.type === 'mousedown') {
                    startX = e.clientX;
                    startY = e.clientY;
                } else {
                    startX = e.touches[0].clientX;
                    startY = e.touches[0].clientY;
                }
                
                // Initial element position
                const rect = widget.getBoundingClientRect();
                initialX = rect.left;
                initialY = rect.top;
                
                // Insert placeholder
                widget.parentNode.insertBefore(placeholder, widget.nextSibling);
                placeholder.style.display = 'block';
                
                // Set absolute positioning
                widget.style.position = 'fixed';
                widget.style.zIndex = '1000';
                widget.style.width = rect.width + 'px';
                widget.style.left = rect.left + 'px';
                widget.style.top = rect.top + 'px';
                
                // Add move and end event listeners
                document.addEventListener('mousemove', drag);
                document.addEventListener('touchmove', drag);
                document.addEventListener('mouseup', stopDragging);
                document.addEventListener('touchend', stopDragging);
            }

            function drag(e) {
                if (!isDragging) return;
                e.preventDefault();

                // Calculate new position
                let currentClientX, currentClientY;
                if (e.type === 'mousemove') {
                    currentClientX = e.clientX;
                    currentClientY = e.clientY;
                } else {
                    currentClientX = e.touches[0].clientX;
                    currentClientY = e.touches[0].clientY;
                }

                // Calculate movement
                const dx = currentClientX - startX;
                const dy = currentClientY - startY;

                // Update element position
                currentX = initialX + dx;
                currentY = initialY + dy;
                
                widget.style.left = currentX + 'px';
                widget.style.top = currentY + 'px';

                // Find the element we're hovering over
                const elements = document.elementsFromPoint(currentClientX, currentClientY);
                const droppableContainer = elements.find(el => 
                    containers.includes(el) || 
                    containers.some(container => container.contains(el))
                );

                // Clear previous drop targets
                document.querySelectorAll('.drag-over').forEach(el => 
                    el.classList.remove('drag-over')
                );

                if (droppableContainer) {
                    droppableContainer.classList.add('drag-over');
                    updatePlaceholderPosition(currentClientX, currentClientY, droppableContainer);
                }
            }

            function updatePlaceholderPosition(x, y, container) {
                // Get all draggable items in the container
                const items = [...container.children].filter(child => 
                    child !== widget && 
                    child !== placeholder &&
                    !child.classList.contains('drag-placeholder')
                );

                // Find the closest item to insert before/after
                let closestItem = null;
                let closestDistance = Infinity;
                let insertBefore = true;

                items.forEach(item => {
                    const rect = item.getBoundingClientRect();
                    const centerX = rect.left + rect.width / 2;
                    const centerY = rect.top + rect.height / 2;
                    
                    const distance = Math.hypot(x - centerX, y - centerY);
                    
                    if (distance < closestDistance) {
                        closestDistance = distance;
                        closestItem = item;
                        insertBefore = y < centerY;
                    }
                });

                // Move placeholder
                if (closestItem) {
                    if (insertBefore) {
                        container.insertBefore(placeholder, closestItem);
                    } else {
                        container.insertBefore(placeholder, closestItem.nextSibling);
                    }
                } else {
                    container.appendChild(placeholder);
                }
            }

            function stopDragging() {
                if (!isDragging) return;
                isDragging = false;

                // Remove dragging class and reset position
                widget.classList.remove('dragging');
                widget.style.position = '';
                widget.style.zIndex = '';
                widget.style.left = '';
                widget.style.top = '';
                widget.style.width = '';

                // Get the final container we're dropping into
                const dropContainer = document.querySelector('.drag-over');
                if (dropContainer) {
                    dropContainer.insertBefore(widget, placeholder);
                    dropContainer.classList.remove('drag-over');
                    
                    // Save new order to localStorage if needed
                    if (dropContainer.id === 'bot-list') {
                        saveWidgetOrder();
                    }
                } else {
                    // Return to original position
                    placeholder.parentNode.insertBefore(widget, placeholder);
                }

                // Remove placeholder
                placeholder.style.display = 'none';
                if (placeholder.parentNode) {
                    placeholder.parentNode.removeChild(placeholder);
                }

                // Remove move and end event listeners
                document.removeEventListener('mousemove', drag);
                document.removeEventListener('touchmove', drag);
                document.removeEventListener('mouseup', stopDragging);
                document.removeEventListener('touchend', stopDragging);
            }

            // Mark widget as initialized
            widget.dataset.dragInitialized = 'true';
        });
    });
}

function saveWidgetOrder() {
    const botList = document.getElementById('bot-list');
    if (!botList) return;

    // Get the order of bot IDs
    const order = [...botList.children]
        .filter(el => el.dataset.botId)
        .map(el => el.dataset.botId);

    // Reorder bots array to match
    const reorderedBots = [];
    order.forEach(id => {
        const bot = bots.find(b => b.id === id);
        if (bot) reorderedBots.push(bot);
    });

    // Add any bots that weren't in the list
    bots.forEach(bot => {
        if (!reorderedBots.includes(bot)) {
            reorderedBots.push(bot);
        }
    });

    // Update bots array and save
    bots = reorderedBots;
    saveBots();
}

// Initialize drag and drop when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initWidgetDragAndDrop();
});

// Re-initialize when bots are rendered
document.addEventListener('botsRendered', () => {
    initWidgetDragAndDrop();
});