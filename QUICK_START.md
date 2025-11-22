# JARVIS Quick Start Guide

## 🚀 Getting Started

### 1. First Time Setup
```bash
# Install all dependencies (see INSTALLATION_GUIDE.md)
pip install -r requirements.txt

# Install Ollama and pull llama3
ollama pull llama3

# Run JARVIS
python run.py
```

### 2. Basic Usage

#### Talk to JARVIS (Voice)
1. Click the **microphone button** 🎤
2. Wait for "Listening..." message
3. Speak your command
4. Wait for response

#### Type to JARVIS (Text)
1. Type in the input box at the bottom
2. Press **Enter** or click **Send button** 📤
3. See response immediately

#### Live Conversation Mode
1. Click the **broadcast button** 🔴
2. Keep talking naturally
3. JARVIS responds automatically
4. Say "**stop**" to exit

## 💬 View Conversation History

### Open History Panel
- Click **📜 button** (top-right corner)
- Or press **Ctrl + H**

### What You'll See
- All your past conversations
- Timestamps for each exchange
- User messages in **blue**
- AI responses in **dark gray**

### Clear History
- Click **"Clear History"** button at bottom of panel
- Confirm to delete all conversations

## 🎯 Common Commands

### System Control
```
"Volume up"
"Take screenshot"
"Lock computer"
"Battery status"
"What time is it"
```

### Open Apps
```
"Open Chrome"
"Open Calculator"
"Open Notepad"
"Open Visual Studio Code"
```

### Entertainment
```
"Play music"
"Next track"
"Google search AI technology"
"Open YouTube"
```

### Files
```
"Search file report.pdf"
"Open folder desktop"
"Create folder MyFolder"
```

### Fun
```
"Tell me a joke"
"Tell me a fact"
"Calculate 50 times 3"
```

### AI Chat
```
"What is artificial intelligence?"
"How does machine learning work?"
"Tell me about quantum computing"
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Send text message |
| **Ctrl + H** | Toggle chat history |
| **Ctrl + L** | Toggle live conversation |
| **Escape** | Close panels |

## 🎨 UI Elements

### Top Buttons
- **📜** (Top-Right): Chat history panel

### Bottom Buttons
- **🎤** Microphone: Voice input
- **📤** Send: Send text message
- **🔴** Broadcast: Live conversation mode
- **⚙️** Settings: Configuration
- **💬** (Bottom-Right): Toggle chat display

## 🔥 Pro Tips

### 1. Context-Aware Conversations
JARVIS remembers your last 5 conversations:
```
You: "Tell me about Python"
JARVIS: [Explains Python]
You: "What are its advantages?"
JARVIS: [Understands you're asking about Python]
```

### 2. Live Mode Best Practices
- Speak clearly
- Wait for response before next question
- Use in quiet environment
- Say "stop" to exit gracefully

### 3. Text Input Tips
- Type naturally
- Press Enter for quick send
- No need to clear input (auto-clears)
- Works simultaneously with voice

### 4. Manage History
- Review past conversations for reference
- Clear old conversations for privacy
- History helps AI understand context

## 🐛 Troubleshooting

### JARVIS Not Responding?
1. Check if Ollama is running
2. Verify microphone permissions
3. Ensure internet connection (for speech recognition)
4. Check backend logs

### Speech Recognition Issues?
1. Speak clearly and slowly
2. Reduce background noise
3. Check microphone volume
4. Try text input instead

### History Not Showing?
1. Restart JARVIS
2. Check if database file exists
3. Try clearing history and start fresh

### Live Mode Not Working?
1. Click broadcast button again
2. Check if already in live mode
3. Restart JARVIS if needed

## 📱 Interface Guide

```
┌─────────────────────────────────────────┐
│  📜 History                  [Status]   │ Top Bar
├─────────────────────────────────────────┤
│                                         │
│         [JARVIS Animation]              │ Center
│                                         │
│         Ask me Anything                 │
├─────────────────────────────────────────┤
│  [Type here...] 🎤 📤 🔴 ⚙️          │ Input Bar
│                              💬         │ Bottom
└─────────────────────────────────────────┘
```

## 🎯 What Makes JARVIS Special?

1. **Remembers Context**: Understands conversation flow
2. **100+ Commands**: Extensive feature set
3. **No API Keys**: Most features work offline
4. **Smart App Launcher**: Opens any Windows app
5. **Conversation History**: Never forget important chats
6. **Live Mode**: Natural conversation flow
7. **Beautiful UI**: Modern, sleek interface

## 🎓 Learning More

- **FEATURES.md**: Complete feature list
- **INSTALLATION_GUIDE.md**: Detailed setup
- **FRONTEND_IMPROVEMENTS.md**: UI enhancements details

## 🎊 Start Talking!

That's it! You're ready to use JARVIS. Just start talking or typing, and JARVIS will assist you with anything you need!

**Example First Command:**
```
"Hey JARVIS, what can you do?"
```

Enjoy your AI assistant! 🚀
