// Media sniffer for detecting video and audio streams
class MediaSniffer {
    constructor() {
        this.mediaElements = new Map();  // element -> MediaInfo
        this.mediaStreams = new Map();   // url -> StreamInfo
        this.observers = new Map();      // element -> MutationObserver
    }
    
    start() {
        // Observe DOM for new media elements
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeName === 'VIDEO' || node.nodeName === 'AUDIO') {
                        this.attachMediaElement(node);
                    }
                });
            });
        });
        
        observer.observe(document.documentElement, {
            childList: true,
            subtree: true
        });
        
        // Find existing media elements
        document.querySelectorAll('video, audio').forEach((element) => {
            this.attachMediaElement(element);
        });
    }
    
    attachMediaElement(element) {
        if (this.mediaElements.has(element)) return;
        
        const mediaInfo = {
            element,
            type: element.nodeName.toLowerCase(),
            sources: new Set(),
            currentSource: null
        };
        
        this.mediaElements.set(element, mediaInfo);
        
        // Watch for source changes
        const observer = new MutationObserver(() => {
            this.updateMediaSources(mediaInfo);
        });
        
        observer.observe(element, {
            attributes: true,
            childList: true,
            subtree: true,
            attributeFilter: ['src', 'currentSrc']
        });
        
        this.observers.set(element, observer);
        
        // Initial source check
        this.updateMediaSources(mediaInfo);
        
        // Listen for play events to detect dynamic sources
        element.addEventListener('play', () => {
            this.updateMediaSources(mediaInfo);
        });
    }
    
    updateMediaSources(mediaInfo) {
        const element = mediaInfo.element;
        const sources = new Set();
        
        // Check src attribute
        if (element.src) {
            sources.add(element.src);
        }
        
        // Check currentSrc
        if (element.currentSrc) {
            sources.add(element.currentSrc);
        }
        
        // Check source elements
        element.querySelectorAll('source').forEach((source) => {
            if (source.src) {
                sources.add(source.src);
            }
        });
        
        // Update sources
        mediaInfo.sources = sources;
        mediaInfo.currentSource = element.currentSrc || element.src;
        
        // Notify about new sources
        this.notifyNewSources(mediaInfo);
    }
    
    notifyNewSources(mediaInfo) {
        mediaInfo.sources.forEach((url) => {
            if (!this.mediaStreams.has(url)) {
                const streamInfo = {
                    url,
                    type: mediaInfo.type,
                    title: this.getMediaTitle(mediaInfo.element),
                    quality: this.getMediaQuality(mediaInfo.element),
                    duration: mediaInfo.element.duration
                };
                
                this.mediaStreams.set(url, streamInfo);
                this.notifyBackground(streamInfo);
            }
        });
    }
    
    getMediaTitle(element) {
        // Try to find title from various sources
        const candidates = [
            // aria-label attribute
            element.getAttribute('aria-label'),
            // title attribute
            element.getAttribute('title'),
            // closest video container
            element.closest('[class*="video"]')?.getAttribute('aria-label'),
            // page title
            document.title
        ];
        
        return candidates.find(title => title) || 'Untitled Media';
    }
    
    getMediaQuality(element) {
        return {
            width: element.videoWidth,
            height: element.videoHeight,
            duration: element.duration,
            codecs: this.getMediaCodecs(element)
        };
    }
    
    getMediaCodecs(element) {
        const codecs = [];
        
        if (element.mediaKeys) {
            codecs.push('DRM Protected');
        }
        
        if (element instanceof HTMLVideoElement) {
            const video = element.captureStream().getVideoTracks()[0];
            if (video) {
                const settings = video.getSettings();
                codecs.push(`${settings.width}x${settings.height}`);
            }
        }
        
        return codecs.join(', ');
    }
    
    notifyBackground(streamInfo) {
        chrome.runtime.sendMessage({
            type: 'media_detected',
            stream: streamInfo
        });
    }
    
    stop() {
        // Cleanup observers
        this.observers.forEach((observer) => {
            observer.disconnect();
        });
        
        this.mediaElements.clear();
        this.mediaStreams.clear();
        this.observers.clear();
    }
}

// Create and start sniffer
const sniffer = new MediaSniffer();
sniffer.start();

// Listen for messages from background
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'get_media_info' && message.url) {
        const streamInfo = sniffer.mediaStreams.get(message.url);
        sendResponse(streamInfo);
    }
    return true;
});
