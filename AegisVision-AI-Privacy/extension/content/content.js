function extractText() {
    if (!document.body) {
        return { success: false, error: "No readable page text found" };
    }

    let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    let node;
    let textContent = [];

    while (node = walker.nextNode()) {
        let parentNode = node.parentNode;
        let parentName = parentNode ? parentNode.nodeName.toUpperCase() : '';
        
        if (parentName !== 'SCRIPT' && parentName !== 'STYLE' && parentName !== 'NOSCRIPT') {
            // Check if the element is hidden to avoid extracting duplicate screen-reader/responsive text
            let isHidden = false;
            if (parentNode && parentNode.nodeType === 1) { // Node.ELEMENT_NODE
                if (typeof parentNode.checkVisibility === 'function') {
                    isHidden = !parentNode.checkVisibility();
                } else {
                    const style = window.getComputedStyle(parentNode);
                    isHidden = (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0');
                }
            }
            
            if (isHidden) continue;

            let txt = node.nodeValue.trim();
            if (txt.length > 0) {
                textContent.push(txt);
            }
        }
    }
    
    if (textContent.length === 0) {
        return { success: false, error: "No readable page text found" };
    }
    
    return { success: true, text: textContent.join('\n') };
}

// Listen for messages from popup
if (typeof window.sentriVisionListenerAdded === 'undefined') {
    window.sentriVisionListenerAdded = true;
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
        if (request.action === "extract_page_text") {
            sendResponse(extractText());
        }
    });
}
