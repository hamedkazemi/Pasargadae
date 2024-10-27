// Get background page
const background = chrome.extension.getBackgroundPage();

// Elements
const statusEl = document.getElementById('status');
const statusTextEl = document.getElementById('status-text');
const captureToggle = document.getElementById('capture-toggle');
const toggleKey = document.getElementById('toggle-key');
const forceKey = document.getElementById('force-key');

// Update status
function updateStatus() {
    if (background.isConnected) {
        statusEl.className = 'status connected';
        statusTextEl.textContent = 'Connected to Download Manager';
    } else {
        statusEl.className = 'status disconnected';
        statusTextEl.textContent = 'Not Connected';
    }
}

// Update capture toggle
function updateCaptureToggle() {
    captureToggle.checked = background.captureEnabled;
}

// Handle capture toggle
captureToggle.addEventListener('change', () => {
    background.ws.send(JSON.stringify({
        type: 'capture_toggle',
        enabled: captureToggle.checked
    }));
});

// Get keyboard shortcuts
chrome.commands.getAll((commands) => {
    commands.forEach((command) => {
        if (command.name === 'toggle_capture') {
            toggleKey.textContent = command.shortcut || 'Not Set';
        } else if (command.name === 'force_download') {
            forceKey.textContent = command.shortcut || 'Not Set';
        }
    });
});

// Update UI when popup opens
updateStatus();
updateCaptureToggle();

// Update UI when connection status changes
background.ws.onopen = () => {
    updateStatus();
};

background.ws.onclose = () => {
    updateStatus();
};
