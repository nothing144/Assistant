# JARVIS AI Assistant - Installation Guide

## 🚀 Windows Installation Instructions

### Prerequisites
- Windows 10/11
- Python 3.8 or higher
- pip (Python package manager)
- Microsoft Edge browser

### Step 1: Install Python Dependencies

Open Command Prompt as Administrator and run:

```bash
pip install eel
pip install opencv-python
pip install numpy
pip install Pillow
pip install SpeechRecognition
pip install pyttsx3
pip install PyAudio
pip install pygame
pip install pvporcupine
pip install pycaw
pip install comtypes
pip install screen-brightness-control
pip install psutil
pip install pyautogui
pip install pywhatkit
pip install playwright
pip install requests
pip install google-generativeai
pip install hugchat
```

### Step 2: Install Playwright Browsers

```bash
playwright install
```

### Step 3: Install Ollama (for AI Chatbot)

1. Download Ollama from: https://ollama.ai/download
2. Install Ollama on Windows
3. Open Command Prompt and run:
```bash
ollama pull llama3
```

### Step 4: Run JARVIS

Navigate to your JARVIS folder and run:

```bash
python run.py
```

## ✨ Available Commands

### System Control
- "Volume up" / "Volume down"
- "Mute volume" / "Unmute volume"
- "What is the current volume"
- "Brightness up" / "Brightness down"
- "Take screenshot"
- "Lock computer"
- "Sleep computer"
- "Shutdown computer" / "Restart computer"
- "Cancel shutdown"
- "Battery status"
- "WiFi status"
- "System info"
- "Empty recycle bin"

### Time & Utilities
- "What time is it"
- "What is the date"
- "What day is today"
- "Set timer for 5 minutes"
- "Set alarm for 07:30"
- "Calculate 25 plus 30"
- "Tell me a joke"
- "Tell me a fact"

### File Operations
- "Search file [filename]"
- "Open folder desktop/documents/downloads"
- "Create folder [foldername]"
- "Delete file [filename]"
- "Delete folder [foldername]"
- "Open file [filename]"

### Entertainment
- "Play music" / "Play music [songname]"
- "Pause music"
- "Next track" / "Previous track"
- "Stop music"
- "Play video" / "Play video [videoname]"
- "Google search [query]"
- "Wikipedia [topic]"
- "Open website [url]"
- "Open Facebook/Twitter/Instagram"

### Application Control
- "Open [any app name]"
  - Examples: "Open notepad", "Open calculator", "Open Chrome"
  - "Open Visual Studio Code", "Open Spotify"

### Notes
- "Remember [note text]"
- "Recall notes" / "Show notes"
- "Last note"
- "Clear notes"

### WhatsApp (Original Feature)
- "Send message to [contact]"
- "Call [contact]"
- "Video call [contact]"

### YouTube (Original Feature)
- "Play [song name] on YouTube"

### AI Chat (Original Feature)
- Ask any question to chat with AI

## 🔧 Troubleshooting

### PyAudio Installation Issues
If PyAudio fails to install, download the wheel file:
1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
2. Download the appropriate .whl file for your Python version
3. Install using: `pip install [downloaded_file].whl`

### Voice Recognition Not Working
- Check microphone permissions
- Ensure internet connection (Google Speech Recognition needs internet)

### Face Authentication Issues
- Ensure good lighting
- Train face samples first using `sample.py` and `trainer.py` in the auth folder

### Ollama Connection Error
- Make sure Ollama is running in the background
- Verify llama3 model is installed: `ollama list`

## 📝 Notes

- Some features require administrator privileges
- Face authentication needs to be trained with your face first
- Ollama must be running for AI chatbot features
- Internet connection required for speech recognition and web features
