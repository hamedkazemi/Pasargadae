class MediaDialog {
    constructor() {
        this.mediaInfo = null;
        this.selectedQuality = null;
        this.setupEventListeners();
        this.loadMediaInfo();
    }
    
    setupEventListeners() {
        document.getElementById('download-button').addEventListener('click', () => {
            this.startDownload();
        });
        
        document.getElementById('cancel-button').addEventListener('click', () => {
            window.close();
        });
        
        document.getElementById('download-subtitles').addEventListener('change', (e) => {
            this.updateSubtitleOptions(e.target.checked);
        });
        
        document.getElementById('download-queue').addEventListener('change', (e) => {
            chrome.storage.local.set({ 'preferred_queue': e.target.value });
        });
    }
    
    async loadMediaInfo() {
        // Get media info from background script
        const params = new URLSearchParams(window.location.search);
        const mediaId = params.get('id');
        
        chrome.runtime.sendMessage(
            { type: 'get_media_info', mediaId },
            (response) => {
                if (response) {
                    this.mediaInfo = response;
                    this.updateUI();
                }
            }
        );
        
        // Load saved preferences
        chrome.storage.local.get(['preferred_queue', 'download_path'], (items) => {
            if (items.preferred_queue) {
                document.getElementById('download-queue').value = items.preferred_queue;
            }
            if (items.download_path) {
                document.getElementById('save-path').value = items.download_path;
            }
        });
    }
    
    updateUI() {
        // Update media info
        document.getElementById('media-title').textContent = this.mediaInfo.title;
        document.getElementById('media-details').textContent = 
            `Source: ${new URL(this.mediaInfo.url).hostname}`;
        
        // Add quality options
        const container = document.getElementById('quality-options');
        container.innerHTML = '';
        
        const template = document.getElementById('quality-option-template');
        
        // Sort qualities by resolution
        const qualities = this.mediaInfo.qualities.sort((a, b) => {
            return b.height - a.height;
        });
        
        qualities.forEach((quality, index) => {
            const option = template.content.cloneNode(true);
            const div = option.querySelector('.quality-option');
            const radio = option.querySelector('.quality-radio');
            const label = option.querySelector('.quality-label');
            const details = option.querySelector('.quality-details');
            
            radio.id = `quality-${index}`;
            radio.value = index;
            
            if (index === 0) {
                radio.checked = true;
                div.classList.add('selected');
                this.selectedQuality = quality;
            }
            
            // Add format badge
            const formatBadge = document.createElement('span');
            formatBadge.className = `format-badge format-${quality.type}`;
            formatBadge.textContent = quality.type.toUpperCase();
            
            label.textContent = this.formatQualityLabel(quality);
            label.appendChild(formatBadge);
            
            details.textContent = this.formatQualityDetails(quality);
            
            div.addEventListener('click', () => {
                document.querySelector('.quality-option.selected')?.classList.remove('selected');
                div.classList.add('selected');
                radio.checked = true;
                this.selectedQuality = quality;
                this.updateSubtitleOptions(
                    document.getElementById('download-subtitles').checked
                );
            });
            
            container.appendChild(option);
        });
        
        // Update subtitle checkbox visibility
        const subtitleCheck = document.getElementById('download-subtitles');
        subtitleCheck.parentElement.style.display = 
            this.mediaInfo.subtitles?.length ? '' : 'none';
    }
    
    formatQualityLabel(quality) {
        if (quality.type === 'video') {
            return `${quality.height}p${quality.fps > 30 ? quality.fps : ''}`;
        } else if (quality.type === 'audio') {
            return `${quality.bitrate}kbps Audio`;
        }
        return quality.label || 'Unknown Quality';
    }
    
    formatQualityDetails(quality) {
        const parts = [];
        
        if (quality.codec) {
            parts.push(quality.codec);
        }
        
        if (quality.size) {
            parts.push(this.formatSize(quality.size));
        }
        
        if (quality.bitrate) {
            parts.push(`${quality.bitrate}kbps`);
        }
        
        return parts.join(' • ');
    }
    
    formatSize(bytes) {
        const units = ['B', 'KB', 'MB', 'GB'];
        let size = bytes;
        let unit = 0;
        while (size >= 1024 && unit < units.length - 1) {
            size /= 1024;
            unit++;
        }
        return `${size.toFixed(1)} ${units[unit]}`;
    }
    
    updateSubtitleOptions(checked) {
        // Update UI based on subtitle selection
        if (!this.mediaInfo.subtitles?.length) return;
        
        const subtitles = checked ? this.mediaInfo.subtitles : [];
        
        // Update selected quality size estimation
        if (this.selectedQuality) {
            const subtitleSize = subtitles.reduce((total, sub) => total + (sub.size || 0), 0);
            const totalSize = this.selectedQuality.size + subtitleSize;
            
            const details = document.querySelector('.quality-option.selected .quality-details');
            details.textContent = this.formatQualityDetails({
                ...this.selectedQuality,
                size: totalSize
            });
        }
    }
    
    startDownload() {
        if (!this.selectedQuality) return;
        
        const options = {
            mediaId: this.mediaInfo.id,
            qualityId: this.selectedQuality.id,
            queue: document.getElementById('download-queue').value,
            savePath: document.getElementById('save-path').value,
            downloadSubtitles: document.getElementById('download-subtitles').checked
        };
        
        chrome.runtime.sendMessage(
            { type: 'start_media_download', options },
            () => window.close()
        );
    }
}

// Initialize dialog
const dialog = new MediaDialog();
