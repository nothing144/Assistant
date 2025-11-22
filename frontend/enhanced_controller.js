/**
 * Enhanced JARVIS Controller
 * Handles chat history, conversation management, and improved UI interactions
 */

$(document).ready(function () {
    // Initialize chat history on load
    loadChatHistory();
    
    // Check live conversation status periodically
    setInterval(checkLiveStatus, 2000);
    
    // Setup event listeners
    setupEventListeners();
});

// ===== EEL EXPOSED FUNCTIONS =====

// Display Speak Message
eel.expose(DisplayMessage);
function DisplayMessage(message) {
    $(".siri-message li:first").text(message);
    $(".siri-message").textillate("start");
    
    // Show status message
    showStatusMessage(message);
}

eel.expose(ShowHood);
function ShowHood() {
    $("#Oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
    hideListeningAnimation();
}

eel.expose(senderText);
function senderText(message) {
    addMessageToChat(message, 'user');
}

eel.expose(receiverText);
function receiverText(message) {
    addMessageToChat(message, 'ai');
}

eel.expose(hideLoader);
function hideLoader() {
    $("#Loader").attr("hidden", true);
    $("#FaceAuth").attr("hidden", false);
}

eel.expose(hideFaceAuth);
function hideFaceAuth() {
    $("#FaceAuth").attr("hidden", true);
    $("#FaceAuthSuccess").attr("hidden", false);
}

eel.expose(hideFaceAuthSuccess);
function hideFaceAuthSuccess() {
    $("#FaceAuthSuccess").attr("hidden", true);
    $("#HelloGreet").attr("hidden", false);
}

eel.expose(hideStart);
function hideStart() {
    $("#Start").attr("hidden", true);
    setTimeout(function () {
        $("#Oval").addClass("animate__animated animate__zoomIn");
    }, 1000);
    setTimeout(function () {
        $("#Oval").attr("hidden", false);
    }, 1000);
}

// ===== CHAT HISTORY FUNCTIONS =====

function loadChatHistory() {
    eel.getRecentConversations(50)(function(conversations) {
        displayChatHistory(conversations);
    });
}

function displayChatHistory(conversations) {
    const historyContent = document.getElementById('chatHistoryContent');
    
    if (!conversations || conversations.length === 0) {
        historyContent.innerHTML = '<div class="empty-history">No conversation history yet</div>';
        return;
    }
    
    historyContent.innerHTML = '';
    
    conversations.forEach(function(conv) {
        const historyItem = document.createElement('div');
        historyItem.className = 'chat-history-item';
        
        historyItem.innerHTML = `
            <div class="history-timestamp">${conv.timestamp}</div>
            <div class="history-user-msg">${escapeHtml(conv.user)}</div>
            <div class="history-ai-msg">${escapeHtml(conv.ai)}</div>
        `;
        
        historyContent.appendChild(historyItem);
    });
    
    // Scroll to bottom
    historyContent.scrollTop = historyContent.scrollHeight;
}

function clearChatHistory() {
    if (confirm('Are you sure you want to clear all conversation history?')) {
        eel.clearConversationHistory()(function(result) {
            if (result) {
                loadChatHistory();
                clearChatDisplay();
                showStatusMessage('Conversation history cleared');
            }
        });
    }
}

// ===== CHAT DISPLAY FUNCTIONS =====

function addMessageToChat(message, type) {
    const chatMessages = document.getElementById('chatMessages');
    
    if (!chatMessages) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.textContent = message;
    
    messageDiv.appendChild(bubble);
    chatMessages.appendChild(messageDiv);
    
    // Auto scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Show chat if hidden
    if (!chatMessages.classList.contains('active')) {
        chatMessages.classList.add('active');
    }
    
    // Reload history
    loadChatHistory();
}

function clearChatDisplay() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
    }
}

function toggleChatDisplay() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.classList.toggle('active');
    }
}

// ===== UI INTERACTION FUNCTIONS =====

function setupEventListeners() {
    // Toggle chat history panel
    const toggleHistoryBtn = document.getElementById('toggleHistoryBtn');
    if (toggleHistoryBtn) {
        toggleHistoryBtn.addEventListener('click', toggleHistoryPanel);
    }
    
    // Close chat history panel
    const closeHistoryBtn = document.getElementById('closeHistoryBtn');
    if (closeHistoryBtn) {
        closeHistoryBtn.addEventListener('click', toggleHistoryPanel);
    }
    
    // Clear history button
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', clearChatHistory);
    }
    
    // Toggle chat display
    const toggleChatBtn = document.getElementById('toggleChatBtn');
    if (toggleChatBtn) {
        toggleChatBtn.addEventListener('click', toggleChatDisplay);
    }
    
    // Enter key in text input
    const chatbox = document.getElementById('chatbox');
    if (chatbox) {
        chatbox.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendTextMessage();
            }
        });
    }
    
    // Chat button click
    const chatBtn = document.getElementById('ChatBtn');
    if (chatBtn) {
        chatBtn.addEventListener('click', sendTextMessage);
    }
    
    // Mic button click
    const micBtn = document.getElementById('MicBtn');
    if (micBtn) {
        micBtn.addEventListener('click', handleVoiceInput);
    }
    
    // Live conversation button (if exists)
    const liveBtn = document.getElementById('LiveBtn');
    if (liveBtn) {
        liveBtn.addEventListener('click', toggleLiveConversation);
    }
}

function toggleHistoryPanel() {
    const panel = document.getElementById('chatHistoryPanel');
    if (panel) {
        panel.classList.toggle('active');
        
        // Reload history when opening
        if (panel.classList.contains('active')) {
            loadChatHistory();
        }
    }
}

function sendTextMessage() {
    const chatbox = document.getElementById('chatbox');
    const message = chatbox.value.trim();
    
    if (message) {
        // Add to UI immediately
        addMessageToChat(message, 'user');
        
        // Clear input
        chatbox.value = '';
        
        // Show loading
        showStatusMessage('Processing...');
        
        // Send to backend
        eel.takeAllCommands(message)(function(response) {
            if (response) {
                addMessageToChat(response, 'ai');
            }
            hideStatusMessage();
        });
    }
}

function handleVoiceInput() {
    showListeningAnimation();
    showStatusMessage('Listening...');
    
    eel.takeAllCommands()(function(response) {
        hideListeningAnimation();
        if (response) {
            addMessageToChat(response, 'ai');
        }
        hideStatusMessage();
    });
}

function toggleLiveConversation() {
    eel.get_live_status()(function(isActive) {
        if (isActive) {
            eel.stop_live_conversation();
            hideLiveIndicator();
        } else {
            eel.start_live_conversation();
            showLiveIndicator();
        }
    });
}

function checkLiveStatus() {
    eel.get_live_status()(function(isActive) {
        if (isActive) {
            showLiveIndicator();
        } else {
            hideLiveIndicator();
        }
    });
}

// ===== UI FEEDBACK FUNCTIONS =====

function showLiveIndicator() {
    const indicator = document.getElementById('liveIndicator');
    if (indicator) {
        indicator.classList.add('active');
    }
}

function hideLiveIndicator() {
    const indicator = document.getElementById('liveIndicator');
    if (indicator) {
        indicator.classList.remove('active');
    }
}

function showListeningAnimation() {
    const animation = document.getElementById('listeningAnimation');
    if (animation) {
        animation.classList.add('active');
    }
}

function hideListeningAnimation() {
    const animation = document.getElementById('listeningAnimation');
    if (animation) {
        animation.classList.remove('active');
    }
}

function showStatusMessage(message) {
    const statusMsg = document.getElementById('statusMessage');
    if (statusMsg) {
        statusMsg.textContent = message;
        statusMsg.style.display = 'block';
    }
}

function hideStatusMessage() {
    const statusMsg = document.getElementById('statusMessage');
    if (statusMsg) {
        setTimeout(function() {
            statusMsg.style.display = 'none';
        }, 2000);
    }
}

// ===== UTILITY FUNCTIONS =====

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString();
}

// ===== KEYBOARD SHORTCUTS =====

document.addEventListener('keydown', function(e) {
    // Ctrl + H to toggle history
    if (e.ctrlKey && e.key === 'h') {
        e.preventDefault();
        toggleHistoryPanel();
    }
    
    // Ctrl + L to toggle live conversation
    if (e.ctrlKey && e.key === 'l') {
        e.preventDefault();
        toggleLiveConversation();
    }
    
    // Escape to close panels
    if (e.key === 'Escape') {
        const panel = document.getElementById('chatHistoryPanel');
        if (panel && panel.classList.contains('active')) {
            toggleHistoryPanel();
        }
    }
});
