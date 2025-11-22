import time
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices)
    engine.setProperty('voice', voices[2].id)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()
    engine.setProperty('rate', 174)
    eel.receiverText(text)

# Expose the Python function to JavaScript

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening...")
        eel.DisplayMessage("I'm listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 8)

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}\n")
        eel.DisplayMessage(query)
        
        
        speak(query)
    except Exception as e:
        print(f"Error: {str(e)}\n")
        return None

    return query.lower()



@eel.expose
def takeAllCommands(message=None):
    if message is None:
        query = takecommand()  # If no message is passed, listen for voice input
        if not query:
            return None  # Exit if no query is received
        print(query)
        eel.senderText(query)
    else:
        query = message  # If there's a message, use it
        print(f"Message received: {query}")
        eel.senderText(query)
    
    try:
        if query:
            query_lower = query.lower()
            
            # System Control Commands
            if "volume up" in query_lower or "increase volume" in query_lower:
                from backend.system_control import increase_volume
                result = increase_volume()
                return result
            elif "volume down" in query_lower or "decrease volume" in query_lower:
                from backend.system_control import decrease_volume
                result = decrease_volume()
                return result
            elif "mute" in query_lower and "volume" in query_lower:
                from backend.system_control import mute_volume
                result = mute_volume()
                return result
            elif "unmute" in query_lower:
                from backend.system_control import unmute_volume
                result = unmute_volume()
                return result
            elif "current volume" in query_lower or "what is the volume" in query_lower:
                from backend.system_control import get_current_volume
                result = get_current_volume()
                return result
            
            # Brightness Control
            elif "brightness up" in query_lower or "increase brightness" in query_lower:
                from backend.system_control import increase_brightness
                result = increase_brightness()
                return result
            elif "brightness down" in query_lower or "decrease brightness" in query_lower:
                from backend.system_control import decrease_brightness
                result = decrease_brightness()
                return result
            
            # Screenshot
            elif "screenshot" in query_lower or "take screenshot" in query_lower:
                from backend.system_control import take_screenshot
                result = take_screenshot()
                return result
            
            # Power Commands
            elif "lock" in query_lower and ("computer" in query_lower or "pc" in query_lower):
                from backend.system_control import lock_computer
                result = lock_computer()
                return result
            elif "sleep" in query_lower and ("computer" in query_lower or "pc" in query_lower):
                from backend.system_control import sleep_computer
                result = sleep_computer()
                return result
            elif "shutdown" in query_lower or "shut down" in query_lower:
                from backend.system_control import shutdown_computer
                result = shutdown_computer()
                return result
            elif "restart" in query_lower or "reboot" in query_lower:
                from backend.system_control import restart_computer
                result = restart_computer()
                return result
            elif "cancel shutdown" in query_lower or "abort shutdown" in query_lower:
                from backend.system_control import cancel_shutdown
                result = cancel_shutdown()
                return result
            
            # Battery & System Info
            elif "battery" in query_lower:
                from backend.system_control import get_battery_status
                result = get_battery_status()
                return result
            elif "wifi" in query_lower or "wi-fi" in query_lower:
                from backend.system_control import get_wifi_status
                result = get_wifi_status()
                return result
            elif "system info" in query_lower or "system status" in query_lower:
                from backend.system_control import get_system_info
                result = get_system_info()
                return result
            elif "empty recycle bin" in query_lower:
                from backend.system_control import empty_recycle_bin
                result = empty_recycle_bin()
                return result
            
            # Time & Date Commands
            elif "time" in query_lower and ("what" in query_lower or "current" in query_lower or "tell" in query_lower):
                from backend.time_utilities import get_current_time
                result = get_current_time()
                return result
            elif "date" in query_lower and ("what" in query_lower or "current" in query_lower or "today" in query_lower or "tell" in query_lower):
                from backend.time_utilities import get_current_date
                result = get_current_date()
                return result
            elif "day" in query_lower and ("what" in query_lower or "today" in query_lower):
                from backend.time_utilities import get_day
                result = get_day()
                return result
            
            # Timer & Alarm
            elif "set timer" in query_lower or "timer for" in query_lower:
                import re
                match = re.search(r'(\d+)\s*(minute|minutes|min)', query_lower)
                if match:
                    minutes = match.group(1)
                    from backend.time_utilities import set_timer
                    result = set_timer(minutes)
                    return result
                else:
                    speak("Please specify the duration in minutes")
                    return "Duration not specified"
            elif "set alarm" in query_lower:
                import re
                match = re.search(r'(\d{1,2}):(\d{2})', query_lower)
                if match:
                    time_str = f"{match.group(1)}:{match.group(2)}"
                    from backend.time_utilities import set_alarm
                    result = set_alarm(time_str)
                    return result
                else:
                    speak("Please specify the time in HH:MM format")
                    return "Time not specified"
            
            # Calculator
            elif "calculate" in query_lower or "what is" in query_lower and any(op in query_lower for op in ["+", "-", "*", "/", "plus", "minus", "times", "divided"]):
                from backend.time_utilities import calculate
                result = calculate(query)
                return result
            
            # Fun Commands
            elif "joke" in query_lower or "tell me a joke" in query_lower:
                from backend.time_utilities import tell_joke
                result = tell_joke()
                return result
            elif "fact" in query_lower or "fun fact" in query_lower:
                from backend.time_utilities import tell_fact
                result = tell_fact()
                return result
            
            # File Operations
            elif "search file" in query_lower or "find file" in query_lower:
                filename = query_lower.replace("search file", "").replace("find file", "").strip()
                from backend.file_operations import search_file
                result = search_file(filename)
                return result
            elif "open folder" in query_lower:
                folder = query_lower.replace("open folder", "").replace("open", "").strip()
                from backend.file_operations import open_folder
                result = open_folder(folder)
                return result
            elif "create folder" in query_lower:
                folder = query_lower.replace("create folder", "").replace("create", "").strip()
                from backend.file_operations import create_folder
                result = create_folder(folder)
                return result
            elif "delete file" in query_lower:
                filename = query_lower.replace("delete file", "").strip()
                from backend.file_operations import delete_file
                result = delete_file(filename)
                return result
            elif "delete folder" in query_lower:
                folder = query_lower.replace("delete folder", "").strip()
                from backend.file_operations import delete_folder
                result = delete_folder(folder)
                return result
            elif "open file" in query_lower:
                filename = query_lower.replace("open file", "").strip()
                from backend.file_operations import open_file
                result = open_file(filename)
                return result
            
            # Music & Entertainment
            elif "play music" in query_lower or "play song" in query_lower:
                song_name = query_lower.replace("play music", "").replace("play song", "").strip()
                from backend.entertainment import play_music
                result = play_music(song_name if song_name else None)
                return result
            elif "pause" in query_lower and ("music" in query_lower or "song" in query_lower or "media" in query_lower):
                from backend.entertainment import pause_media
                result = pause_media()
                return result
            elif "next track" in query_lower or "next song" in query_lower:
                from backend.entertainment import next_track
                result = next_track()
                return result
            elif "previous track" in query_lower or "previous song" in query_lower:
                from backend.entertainment import previous_track
                result = previous_track()
                return result
            elif "stop music" in query_lower or "stop media" in query_lower:
                from backend.entertainment import stop_media
                result = stop_media()
                return result
            elif "play video" in query_lower:
                video_name = query_lower.replace("play video", "").strip()
                from backend.entertainment import play_video
                result = play_video(video_name if video_name else None)
                return result
            
            # Web Search
            elif "google search" in query_lower or "search google" in query_lower:
                from backend.entertainment import search_google
                result = search_google(query)
                return result
            elif "wikipedia" in query_lower or "search wikipedia" in query_lower:
                from backend.entertainment import search_wikipedia
                result = search_wikipedia(query)
                return result
            elif "open website" in query_lower:
                url = query_lower.replace("open website", "").strip()
                from backend.entertainment import open_website
                result = open_website(url)
                return result
            
            # Social Media
            elif any(platform in query_lower for platform in ["facebook", "twitter", "instagram", "linkedin", "reddit"]):
                for platform in ["facebook", "twitter", "instagram", "linkedin", "reddit", "tiktok"]:
                    if platform in query_lower:
                        from backend.entertainment import open_social_media
                        result = open_social_media(platform)
                        return result
            
            # Notes
            elif "remember" in query_lower or "note" in query_lower or "save this" in query_lower:
                note_text = query_lower.replace("remember", "").replace("note", "").replace("save this", "").strip()
                if note_text:
                    from backend.notes import remember_note
                    result = remember_note(note_text)
                    return result
            elif "recall notes" in query_lower or "show notes" in query_lower or "my notes" in query_lower:
                from backend.notes import recall_notes
                result = recall_notes()
                return result
            elif "last note" in query_lower:
                from backend.notes import recall_last_note
                result = recall_last_note()
                return result
            elif "clear notes" in query_lower:
                from backend.notes import clear_notes
                result = clear_notes()
                return result
            
            # Original Commands
            elif "open" in query:
                # Try enhanced app launcher first
                from backend.app_launcher import open_any_app
                from backend.feature import openCommand
                
                app_name = query.replace("open", "").strip()
                result = open_any_app(app_name)
                
                # If enhanced launcher fails, try original method
                if "not found" in result.lower():
                    result = openCommand(query)
                
                return result
            
            elif "send message" in query or "call" in query or "video call" in query:
                from backend.feature import findContact, whatsApp
                flag = ""
                Phone, name = findContact(query)
                if Phone != 0:
                    if "send message" in query:
                        flag = 'message'
                        speak("What message to send?")
                        query = takecommand()  # Ask for the message text
                    elif "call" in query:
                        flag = 'call'
                    else:
                        flag = 'video call'
                    whatsApp(Phone, query, flag, name)
                    return "WhatsApp action completed"
                return "Contact not found"
            
            elif "on youtube" in query:
                from backend.feature import PlayYoutube
                PlayYoutube(query)
                return "YouTube action completed"
            
            else:
                from backend.feature import chatBot
                result = chatBot(query)
                return result
        else:
            speak("No command was given.")
            return "No command given"
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, something went wrong.")
        return f"Error: {str(e)}"
    finally:
        eel.ShowHood()
        return None
