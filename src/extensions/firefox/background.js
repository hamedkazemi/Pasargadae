// Firefox-specific adaptations
const browser = window.browser;

// Replace chrome API calls with browser API calls
function initializeFirefoxAPIs() {
    // Replace chrome.action with browser.browserAction
    if (typeof chrome !== 'undefined') {
        chrome.action = browser.browserAction;
    }
    
    // Add Firefox-specific download interception
    browser.webRequest.onBeforeRequest.addListener(
        function(details) {
            if (!captureEnabled) return;
            
            // Check if this is a download request
            if (details.type === 'other' && 
                !details.url.startsWith('blob:') && 
                !details.url.startsWith('data:')) {
                
                // Get content type from headers
                browser.webRequest.getHeader(
                    details.requestId,
                    'content-type',
                    function(contentType) {
                        if (shouldInterceptContentType(contentType)) {
                            sendDownloadRequest(details.url, details.originUrl);
                            return { cancel: true };
                        }
                    }
                );
            }
            return { cancel: false };
        },
        { urls: ["<all_urls>"] },
        ["blocking"]
    );
}

// Initialize Firefox-specific features
initializeFirefoxAPIs();

// Rest of the common background.js code here...
// [Previous background.js content]
