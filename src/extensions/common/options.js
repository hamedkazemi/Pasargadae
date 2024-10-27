// Default options
const DEFAULT_OPTIONS = {
    captureMode: 'all',
    mediaCapture: true,
    fileExtensions: ['.zip', '.rar', '.pdf', '.doc', '.mp4', '.mp3'],
    blockedUrls: [],
    showNotifications: true,
    notificationSound: true
};

// Load options
async function loadOptions() {
    const options = await chrome.storage.sync.get(DEFAULT_OPTIONS);
    
    // Set form values
    document.getElementById('capture-mode').value = options.captureMode;
    document.getElementById('media-capture').checked = options.mediaCapture;
    document.getElementById('show-notifications').checked = options.showNotifications;
    document.getElementById('notification-sound').checked = options.notificationSound;
    
    // Load file extensions
    const extensionList = document.getElementById('extension-list');
    extensionList.innerHTML = '';
    options.fileExtensions.forEach(ext => {
        addFilterItem(extensionList, ext);
    });
    
    // Load blocked URLs
    const blockedUrlList = document.getElementById('blocked-url-list');
    blockedUrlList.innerHTML = '';
    options.blockedUrls.forEach(url => {
        addFilterItem(blockedUrlList, url);
    });
}

// Save options
async function saveOptions() {
    const options = {
        captureMode: document.getElementById('capture-mode').value,
        mediaCapture: document.getElementById('media-capture').checked,
        showNotifications: document.getElementById('show-notifications').checked,
        notificationSound: document.getElementById('notification-sound').checked,
        fileExtensions: getFilterItems('extension-list'),
        blockedUrls: getFilterItems('blocked-url-list')
    };
    
    await chrome.storage.sync.set(options);
    
    // Show save confirmation
    const saveButton = document.getElementById('save');
    const originalText = saveButton.textContent;
    saveButton.textContent = 'Saved!';
    saveButton.disabled = true;
    
    setTimeout(() => {
        saveButton.textContent = originalText;
        saveButton.disabled = false;
    }, 1500);
}

// Reset options
async function resetOptions() {
    await chrome.storage.sync.set(DEFAULT_OPTIONS);
    await loadOptions();
}

// Helper functions
function addFilterItem(list, value) {
    const item = document.createElement('div');
    item.className = 'filter-item';
    
    const text = document.createElement('span');
    text.textContent = value;
    
    const removeButton = document.createElement('button');
    removeButton.textContent = '×';
    removeButton.onclick = () => item.remove();
    
    item.appendChild(text);
    item.appendChild(removeButton);
    list.appendChild(item);
}

function getFilterItems(listId) {
    const list = document.getElementById(listId);
    return Array.from(list.querySelectorAll('.filter-item span'))
                .map(span => span.textContent);
}

// Event listeners
document.addEventListener('DOMContentLoaded', loadOptions);

document.getElementById('save').addEventListener('click', saveOptions);
document.getElementById('reset').addEventListener('click', resetOptions);

document.getElementById('add-extension').addEventListener('click', () => {
    const input = document.getElementById('extension-input');
    const value = input.value.trim();
    
    if (value && !value.includes(' ')) {
        const list = document.getElementById('extension-list');
        addFilterItem(list, value.startsWith('.') ? value : '.' + value);
        input.value = '';
    }
});

document.getElementById('add-blocked-url').addEventListener('click', () => {
    const input = document.getElementById('blocked-url-input');
    const value = input.value.trim();
    
    if (value) {
        const list = document.getElementById('blocked-url-list');
        addFilterItem(list, value);
        input.value = '';
    }
});
