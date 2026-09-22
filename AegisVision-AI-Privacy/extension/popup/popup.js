document.addEventListener("DOMContentLoaded", () => {
    const statusIndicator = document.getElementById("backend-status");
    const sendBtn = document.getElementById("send-ai-btn");
    const resultsDiv = document.getElementById("results");
    const protectedCount = document.getElementById("protected-count");
    const classificationEl = document.getElementById("classification");
    const aiViewText = document.getElementById("ai-view-text");

    const API_URL = "http://127.0.0.1:8000";

    function resetBtn() {
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.textContent = "SEND SANITIZED PAGE TO AI";
        }
    }

    // Check backend status
    fetch(API_URL + "/")
        .then(response => response.json())
        .then(data => {
            if (data && data.status === "running") {
                if (statusIndicator) {
                    statusIndicator.textContent = "Connected";
                    statusIndicator.className = "status-indicator connected";
                }
                if (sendBtn) {
                    sendBtn.disabled = false;
                }
            } else {
                if (statusIndicator) {
                    statusIndicator.textContent = "Disconnected";
                    statusIndicator.className = "status-indicator disconnected";
                }
                if (sendBtn) {
                    sendBtn.disabled = true;
                }
            }
        })
        .catch(err => {
            if (statusIndicator) {
                statusIndicator.textContent = "Disconnected";
                statusIndicator.className = "status-indicator disconnected";
            }
            if (sendBtn) {
                sendBtn.disabled = true;
            }
        });

    if (sendBtn) {
        sendBtn.addEventListener("click", () => {
            sendBtn.disabled = true;
            sendBtn.textContent = "PROCESSING...";
            
            // 1. Get webpage text
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (!tabs || tabs.length === 0) {
                    alert("SentriVision: Cannot find active tab.");
                    resetBtn();
                    return;
                }
                let activeTab = tabs[0];
                
                const processText = (response) => {
                    if (!response || !response.success) {
                        const errMsg = response && response.error ? response.error : "Unknown extraction error";
                        alert("SentriVision: " + errMsg);
                        resetBtn();
                        return;
                    }
                    
                    const rawText = response.text;
                    if (!rawText) {
                        alert("SentriVision: No readable page text found");
                        resetBtn();
                        return;
                    }
                    
                    // 2. Send to local privacy gateway for sanitization
                    fetch(API_URL + "/sanitize", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ text: rawText })
                    })
                    .then(res => {
                        if (!res.ok) throw new Error("Sanitization failed with status: " + res.status);
                        return res.json();
                    })
                    .then(sanitizeData => {
                        // Update UI
                        if (protectedCount) {
                            protectedCount.textContent = sanitizeData.protected_count;
                        }
                        if (classificationEl) {
                            classificationEl.textContent = sanitizeData.classification;
                        }
                        
                        const sanitizedText = sanitizeData.sanitized_text;
                        
                        // 3. Send sanitized text to AI backend
                        return fetch(API_URL + "/ai/process", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ text: sanitizedText })
                        });
                    })
                    .then(res => {
                        if (!res.ok) throw new Error("AI API Error with status: " + res.status);
                        return res.json();
                    })
                    .then(aiData => {
                        // Display what the AI received
                        if (aiViewText) {
                            aiViewText.value = aiData.received_by_ai;
                        }
                        if (resultsDiv) {
                            resultsDiv.classList.remove("hidden");
                        }
                        resetBtn();
                    })
                    .catch(err => {
                        console.error("Error during privacy flow:", err);
                        alert("SentriVision Backend Error: " + err.message);
                        resetBtn();
                    });
                };

                const handleExtractionResponse = (response) => {
                    if (chrome.runtime.lastError || !response) {
                        const lastError = chrome.runtime.lastError ? chrome.runtime.lastError.message : "No response";
                        
                        // If content script is disconnected or hasn't loaded
                        if (lastError.includes("Receiving end does not exist") || lastError.includes("Could not establish connection")) {
                            chrome.scripting.executeScript({
                                target: { tabId: activeTab.id },
                                files: ["content/content.js"]
                            }, () => {
                                if (chrome.runtime.lastError) {
                                    alert("SentriVision: Cannot extract text. " + chrome.runtime.lastError.message);
                                    resetBtn();
                                    return;
                                }
                                // Retry extraction after injection
                                chrome.tabs.sendMessage(activeTab.id, { action: "extract_page_text" }, (retryResponse) => {
                                    if (chrome.runtime.lastError || !retryResponse) {
                                        alert("SentriVision: Cannot extract text. " + (chrome.runtime.lastError ? chrome.runtime.lastError.message : "No response"));
                                        resetBtn();
                                        return;
                                    }
                                    processText(retryResponse);
                                });
                            });
                            return;
                        }
                        
                        alert("SentriVision: Cannot extract text. " + lastError);
                        resetBtn();
                        return;
                    }
                    processText(response);
                };

                chrome.tabs.sendMessage(activeTab.id, { action: "extract_page_text" }, handleExtractionResponse);
            });
        });
    }
});
