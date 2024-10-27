// WebSocket connection to native app
let ws = null;
let isConnected = false;
let captureEnabled = true;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 5;

// Connect to native app
function connect() {
    if (ws) {
        ws.close();
    }

    ws = new WebSocket('ws://localhost:8765');

    ws.onopen = () => {
        console.log('Connected to download manager');
        isConnected = true;
        reconnectAttempts = 0;
        
        // Update extension icon
        chrome.action.setIcon({
            path: {
                "16": "icons/icon16.png",
                "32": "icons/icon32.png",
                "48": "icons/icon48.png",
                "128": "icons/icon128.png"
            }
        });
    };

    ws.onclose = () => {
        console.log('Disconnected from download manager');
        isConnected = false;
        
        // Update extension icon to show disconnected state
        chrome.action.setIcon({
            path: {
                "16": "icons/icon16_disabled.png",
                "32": "icons/icon32_disabled.png",
                "48": "icons/icon48_disabled.png",
                "128": "icons/icon128_disabled.png"
            }
        });

        // Try to reconnect
        if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
            reconnectAttempts++;
            setTimeout(connect, 1000 * Math.pow(2, reconnectAttempts));
        }
    };

    ws.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            handleMessage(message);
        } catch (e) {
            console.error('Error handling message:', e);
        }
    };

    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
}

// Handle messages from native app
function handleMessage(message) {
    switch (message.type) {
        case 'capture_status':
            captureEnabled = message.enabled;
            updateExtensionState();
            break;
            
        case 'download_started':
            // Show notification
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icons/icon48.png',
                title: 'Download Started',
                message: 'Download has been added to the queue'
            });
            break;
            
        case 'error':
            // Show error notification
            chrome.notifications.create({
                type: 'basic',
                iconUrl: 'icons/icon48.png',
                title: 'Download Error',
                message: message.error
            });
            break;
    }
}

// Send download request to native app
function sendDownloadRequest(url, referrer = '') {
    if (!isConnected) {
        chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon48.png',
            title: 'Connection Error',
            message: 'Not connected to download manager'
        });
        return;
    }

    ws.send(JSON.stringify({
        type: 'download_request',
        url: url,
        referrer: referrer,
        headers: {
            'User-Agent': navigator.userAgent
        }
    }));
}

// Update extension state
function updateExtensionState() {
    chrome.action.setBadgeText({
        text: captureEnabled ? 'ON' : 'OFF'
    });
    
    chrome.action.setBadgeBackgroundColor({
        color: captureEnabled ? '#4CAF50' : '#F44336'
    });
}

// Listen for download events
chrome.downloads.onCreated.addListener((downloadItem) => {
    if (!captureEnabled) return;
    
    // Check if we should handle this download
    if (downloadItem.url.startsWith('blob:') || 
        downloadItem.url.startsWith('data:')) {
        return;
    }
    
    // Cancel browser download and send to our manager
    chrome.downloads.cancel(downloadItem.id, () => {
        sendDownloadRequest(downloadItem.url, downloadItem.referrer);
    });
});

// Listen for keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
    if (command === 'toggle_capture') {
        captureEnabled = !captureEnabled;
        ws.send(JSON.stringify({
            type: 'capture_toggle',
            enabled: captureEnabled
        }));
        updateExtensionState();
    }
});

// Context menu for links
chrome.contextMenus.create({
    id: 'download_with_manager',
    title: 'Download with Pasargadae',
    contexts: ['link']
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
    if (info.menuItemId === 'download_with_manager') {
        sendDownloadRequest(info.linkUrl, tab.url);
    }
});

// Connect when extension loads
connect();
