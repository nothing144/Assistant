"""
Entertainment Features for JARVIS
Music, media control, and web browsing
"""
import os
import webbrowser
import pyautogui
from backend.command import speak
import random


def play_music(song_name=None):
    """Play music from Music folder"""
    try:
        music_dir = os.path.join(os.path.expanduser("~"), "Music")
        
        if not os.path.exists(music_dir):
            speak("Music folder not found")
            return "Music folder not found"
        
        # Get all music files
        music_files = []
        for file in os.listdir(music_dir):
            if file.endswith(('.mp3', '.wav', '.m4a', '.flac', '.aac', '.wma')):
                music_files.append(os.path.join(music_dir, file))
        
        if not music_files:
            speak("No music files found")
            return "No music files found"
        
        if song_name:
            # Search for specific song
            for file in music_files:
                if song_name.lower() in os.path.basename(file).lower():
                    os.startfile(file)
                    speak(f"Playing {os.path.basename(file)}")
                    return f"Playing: {os.path.basename(file)}"
            
            speak(f"Song {song_name} not found")
            return "Song not found"
        else:
            # Play random song
            random_song = random.choice(music_files)
            os.startfile(random_song)
            speak(f"Playing {os.path.basename(random_song)}")
            return f"Playing: {os.path.basename(random_song)}"
        
    except Exception as e:
        speak("Failed to play music")
        return f"Error: {str(e)}"


def pause_media():
    """Pause/Play media using space key"""
    try:
        pyautogui.press('playpause')
        speak("Media paused")
        return "Media paused/played"
    except Exception as e:
        speak("Failed to pause media")
        return f"Error: {str(e)}"


def next_track():
    """Skip to next track"""
    try:
        pyautogui.press('nexttrack')
        speak("Next track")
        return "Next track"
    except Exception as e:
        speak("Failed to skip track")
        return f"Error: {str(e)}"


def previous_track():
    """Go to previous track"""
    try:
        pyautogui.press('prevtrack')
        speak("Previous track")
        return "Previous track"
    except Exception as e:
        speak("Failed to go to previous track")
        return f"Error: {str(e)}"


def stop_media():
    """Stop media playback"""
    try:
        pyautogui.press('stop')
        speak("Media stopped")
        return "Media stopped"
    except Exception as e:
        speak("Failed to stop media")
        return f"Error: {str(e)}"


def search_google(query):
    """Search Google"""
    try:
        query = query.replace("google search", "").replace("search", "").strip()
        speak(f"Searching Google for {query}")
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching: {query}"
    except Exception as e:
        speak("Failed to search Google")
        return f"Error: {str(e)}"


def search_wikipedia(query):
    """Search Wikipedia"""
    try:
        query = query.replace("wikipedia", "").replace("search", "").strip()
        speak(f"Searching Wikipedia for {query}")
        url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        webbrowser.open(url)
        return f"Searching Wikipedia: {query}"
    except Exception as e:
        speak("Failed to search Wikipedia")
        return f"Error: {str(e)}"


def open_website(url):
    """Open a website"""
    try:
        if not url.startswith("http"):
            url = "https://" + url
        
        speak(f"Opening website")
        webbrowser.open(url)
        return f"Opened: {url}"
    except Exception as e:
        speak("Failed to open website")
        return f"Error: {str(e)}"


def play_video(video_name):
    """Play video from Videos folder"""
    try:
        videos_dir = os.path.join(os.path.expanduser("~"), "Videos")
        
        if not os.path.exists(videos_dir):
            speak("Videos folder not found")
            return "Videos folder not found"
        
        # Get all video files
        video_files = []
        for file in os.listdir(videos_dir):
            if file.endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv')):
                video_files.append(os.path.join(videos_dir, file))
        
        if not video_files:
            speak("No video files found")
            return "No video files found"
        
        if video_name:
            # Search for specific video
            for file in video_files:
                if video_name.lower() in os.path.basename(file).lower():
                    os.startfile(file)
                    speak(f"Playing {os.path.basename(file)}")
                    return f"Playing: {os.path.basename(file)}"
            
            speak(f"Video {video_name} not found")
            return "Video not found"
        else:
            # Play random video
            random_video = random.choice(video_files)
            os.startfile(random_video)
            speak(f"Playing {os.path.basename(random_video)}")
            return f"Playing: {os.path.basename(random_video)}"
        
    except Exception as e:
        speak("Failed to play video")
        return f"Error: {str(e)}"


def open_social_media(platform):
    """Open social media platforms"""
    try:
        platforms = {
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            "tiktok": "https://www.tiktok.com",
            "youtube": "https://www.youtube.com",
            "whatsapp": "https://web.whatsapp.com",
            "telegram": "https://web.telegram.org",
        }
        
        platform = platform.lower().strip()
        
        if platform in platforms:
            speak(f"Opening {platform}")
            webbrowser.open(platforms[platform])
            return f"Opened: {platform}"
        else:
            speak(f"Platform {platform} not recognized")
            return "Platform not found"
        
    except Exception as e:
        speak("Failed to open social media")
        return f"Error: {str(e)}"
