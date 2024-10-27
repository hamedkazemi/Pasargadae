// Chrome-specific adaptations
import './common/background.js';

// Add Chrome-specific download interception
chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        if (!captureEnabled) return;
        
        // Check if this is a download request
        if (details.type === 'other' && 
            !details.url.startsWith('blob:') && 
            !details.url.startsWith('data:')) {
            
            // Get content type from headers
            chrome.webRequest.getResponseHeaders(
                details.requestId,
                function(headers) {
                    const contentType = headers.find(
                        h => h.name.toLowerCase() === 'content-type'
                    );
                    if (contentType && shouldInterceptContentType(contentType.value)) {
                        sendDownloadRequest(details.url, details.initiator);
                        return { cancel: true };
                    }
                }
            );
        }
        return { cancel: false };
    },
    { urls: ["<all_urls>"] },
    ["blocking", "responseHeaders"]
);

// Add media interception
chrome.webRequest.onHeadersReceived.addListener(
    function(details) {
        if (!captureEnabled) return;
        
        const contentType = details.responseHeaders.find(
            h => h.name.toLowerCase() === 'content-type'
        );
        
        if (contentType && isMediaContentType(contentType.value)) {
            // Check if this is a media file
            sendDownloadRequest(details.url, details.initiator);
            return { cancel: true };
        }
        
        return { responseHeaders: details.responseHeaders };
    },
    { urls: ["<all_urls>"] },
    ["blocking", "responseHeaders"]
);

// Helper functions
function isMediaContentType(contentType) {
    return contentType.startsWith('video/') || 
           contentType.startsWith('audio/') ||
           contentType.includes('mpegurl') ||
           contentType.includes('mp4') ||
           contentType.includes('webm');
}

function shouldInterceptContentType(contentType) {
    const downloadTypes = [
        'application/octet-stream',
        'application/zip',
        'application/x-rar-compressed',
        'application/pdf',
        'application/msword',
        'application/vnd.ms-excel',
        'application/vnd.ms-powerpoint'
    ];
    
    return downloadTypes.some(type => contentType.includes(type)) ||
           isMediaContentType(contentType);
}
