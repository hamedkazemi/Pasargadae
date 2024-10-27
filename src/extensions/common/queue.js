// Queue management
class QueueManager {
    constructor() {
        this.downloads = new Map();
        this.activeTab = 'all';
        this.setupEventListeners();
        this.connectToBackground();
    }
    
    connectToBackground() {
        // Connect to background script
        this.port = chrome.runtime.connect({ name: 'queue' });
        
        this.port.onMessage.addListener((message) => {
            switch (message.type) {
                case 'download_update':
                    this.updateDownload(message.download);
                    break;
                    
                case 'download_added':
                    this.addDownload(message.download);
                    break;
                    
                case 'download_removed':
                    this.removeDownload(message.downloadId);
                    break;
                    
                case 'queue_update':
                    this.updateStats(message.stats);
                    break;
            }
        });
        
        // Request initial queue state
        this.port.postMessage({ type: 'get_queue' });
    }
    
    setupEventListeners() {
        // Tab switching
        document.querySelectorAll('.queue-tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelector('.queue-tab.active').classList.remove('active');
                tab.classList.add('active');
                this.activeTab = tab.dataset.queue;
                this.filterQueue();
            });
        });
        
        // Queue actions
        document.getElementById('clear-completed').addEventListener('click', () => {
            this.port.postMessage({ type: 'clear_completed' });
        });
        
        document.getElementById('start-all').addEventListener('click', () => {
            this.port.postMessage({ type: 'start_all' });
        });
        
        // Drag and drop reordering
        const queueList = document.getElementById('queue-list');
        
        queueList.addEventListener('dragstart', (e) => {
            e.target.classList.add('dragging');
            e.dataTransfer.setData('text/plain', e.target.dataset.downloadId);
        });
        
        queueList.addEventListener('dragend', (e) => {
            e.target.classList.remove('dragging');
        });
        
        queueList.addEventListener('dragover', (e) => {
            e.preventDefault();
            const draggingItem = document.querySelector('.dragging');
            const siblings = [...queueList.querySelectorAll('.queue-item:not(.dragging)')];
            const nextSibling = siblings.find(sibling => {
                const box = sibling.getBoundingClientRect();
                const offset = e.clientY - box.top - box.height / 2;
                return offset < 0;
            });
            
            if (nextSibling) {
                queueList.insertBefore(draggingItem, nextSibling);
            } else {
                queueList.appendChild(draggingItem);
            }
        });
        
        queueList.addEventListener('drop', (e) => {
            e.preventDefault();
            const downloadId = e.dataTransfer.getData('text/plain');
            const newPosition = Array.from(queueList.children).findIndex(
                item => item.dataset.downloadId === downloadId
            );
            
            this.port.postMessage({
                type: 'reorder_queue',
                downloadId,
                newPosition
            });
        });
    }
    
    addDownload(download) {
        if (this.downloads.has(download.id)) {
            this.updateDownload(download);
            return;
        }
        
        const template = document.getElementById('queue-item-template');
        const item = template.content.cloneNode(true).firstElementChild;
        
        item.dataset.downloadId = download.id;
        item.dataset.status = download.status;
        
        const title = item.querySelector('.item-title');
        title.textContent = this.getDownloadName(download);
        
        this.setupItemActions(item, download.id);
        this.downloads.set(download.id, download);
        
        const queueList = document.getElementById('queue-list');
        queueList.appendChild(item);
        
        this.updateDownloadItem(item, download);
        this.filterQueue();
    }
    
    updateDownload(download) {
        const item = document.querySelector(`[data-download-id="${download.id}"]`);
        if (!item) return;
        
        this.downloads.set(download.id, download);
        this.updateDownloadItem(item, download);
        this.filterQueue();
    }
    
    removeDownload(downloadId) {
        const item = document.querySelector(`[data-download-id="${downloadId}"]`);
        if (item) {
            item.remove();
        }
        this.downloads.delete(downloadId);
        this.filterQueue();
    }
    
    updateDownloadItem(item, download) {
        item.dataset.status = download.status;
        
        const size = item.querySelector('.item-size');
        size.textContent = this.formatSize(download.total_size);
        
        const speed = item.querySelector('.item-speed');
        speed.textContent = download.status === 'downloading' 
            ? this.formatSpeed(download.speed)
            : '';
        
        const eta = item.querySelector('.item-eta');
        eta.textContent = download.status === 'downloading'
            ? this.formatETA(download.eta)
            : download.status.toUpperCase();
        
        const progress = item.querySelector('.progress-fill');
        progress.style.width = `${download.progress}%`;
        
        // Update action buttons
        const pauseBtn = item.querySelector('[data-action="pause"]');
        pauseBtn.textContent = download.status === 'downloading' ? '⏸' : '▶';
        pauseBtn.disabled = download.status === 'completed';
    }
    
    setupItemActions(item, downloadId) {
        item.querySelectorAll('.item-action').forEach(button => {
            button.addEventListener('click', () => {
                this.port.postMessage({
                    type: 'download_action',
                    action: button.dataset.action,
                    downloadId
                });
            });
        });
    }
    
    filterQueue() {
        const items = document.querySelectorAll('.queue-item');
        items.forEach(item => {
            const status = item.dataset.status;
            const visible = this.activeTab === 'all' || 
                          (this.activeTab === 'active' && status === 'downloading') ||
                          (this.activeTab === 'waiting' && status === 'queued') ||
                          (this.activeTab === 'completed' && status === 'completed');
            
            item.style.display = visible ? '' : 'none';
        });
        
        // Show empty state if needed
        const hasVisibleItems = Array.from(items).some(
            item => item.style.display !== 'none'
        );
        
        const emptyState = document.querySelector('.empty-queue');
        if (!hasVisibleItems) {
            if (!emptyState) {
                const empty = document.createElement('div');
                empty.className = 'empty-queue';
                empty.textContent = 'No downloads in this queue';
                document.getElementById('queue-list').appendChild(empty);
            }
        } else if (emptyState) {
            emptyState.remove();
        }
    }
    
    updateStats(stats) {
        document.getElementById('active-count').textContent = stats.active;
        document.getElementById('waiting-count').textContent = stats.waiting;
        document.getElementById('completed-count').textContent = stats.completed;
    }
    
    // Helper functions
    getDownloadName(download) {
        return download.filename || download.url.split('/').pop() || 'Unknown';
    }
    
    formatSize(bytes) {
        if (!bytes) return 'Unknown';
        const units = ['B', 'KB', 'MB', 'GB'];
        let size = bytes;
        let unit = 0;
        while (size >= 1024 && unit < units.length - 1) {
            size /= 1024;
            unit++;
        }
        return `${size.toFixed(1)} ${units[unit]}`;
    }
    
    formatSpeed(bytesPerSecond) {
        return `${this.formatSize(bytesPerSecond)}/s`;
    }
    
    formatETA(seconds) {
        if (!seconds) return '';
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        }
        const secs = Math.floor(seconds % 60);
        return `${minutes}:${secs.toString().padStart(2, '0')}`;
    }
}

// Initialize queue manager
const queueManager = new QueueManager();
