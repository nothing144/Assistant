# import playsound
# import eel


# @eel.expose
# def playAssistantSound():
#     music_dir = "frontend\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)
import threading 
from backend.browser_controller import BrowserController
import speech_recognition as sr 
import google.generativeai as genai
from compileall import compile_path
import os
import re
from shlex import quote
import struct
import subprocess
import time
import webbrowser
import eel
from hugchat import hugchat 
import pvporcupine
import pyaudio
import pyautogui
import pywhatkit as kit
import pygame
from backend.command import speak
from backend.config import ASSISTANT_NAME
import sqlite3
import requests

from backend.helper import extract_yt_term, remove_words
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()
# Initialize pygame mixer
pygame.mixer.init()

#when using gemini api
# genai.configure(api_key="AIzaSyBQau2W1-Ur8YZk5WmcEK2sCemlm_3dnys")
# model = genai.GenerativeModel("gemini-1.5-pro")





# Define the function to play sound
@eel.expose
def play_assistant_sound():
    sound_file = r"D:\Jarvis-2025-master\frontend\assets\audio\start_sound.mp3"
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    return None
    
    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()
    app_name = query.strip()
    if app_name != "":
        try:
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()
            if len(results) != 0:
                speak("Opening " + app_name)
                os.startfile(results[0][0])
                return "Opened " + app_name
            else:
                cursor.execute('SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                if len(results) != 0:
                    speak("Opening " + app_name)
                    webbrowser.open(results[0][0])
                    return "Opened " + app_name
                else:
                    speak("Opening " + app_name)
                    try:
                        os.system('start ' + app_name)
                        return "Tried to open " + app_name
                    except Exception as e:
                        speak("not found")
                        return "Not found: " + str(e)
        except Exception as e:
            speak("something went wrong")
            return "Error: " + str(e)
    return "No app name provided"


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)




def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Yaha apna Picovoice access key daalna 🔑
        porcupine = pvporcupine.create(
            access_key="YsKVSwPGhnEJC7FfzbbhhOW/XtpU/N/mTKyIEWK9CX6G1bqRjMi4+w==",
            keywords=["jarvis", "alexa"]
        )

        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("🎙 Waiting for hotword...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("🔥 Hotword detected!")

                # Example: press Win+J shortcut
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(1)
                pyautogui.keyUp("win")

    except Exception as e:
        print(f"Error in hotword: {e}")

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT Phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
    
def whatsApp(Phone, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={Phone}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# // this is for gemini api 
# def chatBot(query):
#     try:
#         user_input = query.lower()
#         response = model.generate_content(user_input)

#         reply = response.text
#         print(reply)
#         speak(reply)
#         return reply

#     except Exception as e:
#         print(f"Error in chatBot: {e}")
#         speak("Sorry, I am unable to respond right now.")
#         return "Error" 
def chatBot(query):
    try:
        # Import conversation manager
        from backend.conversation_manager import add_conversation, get_context_for_ai
        
        # Get conversation context
        context = get_context_for_ai(limit=5)
        
        # Enhanced JARVIS persona prompt
        system_prompt = """
You are JARVIS — an intelligent, helpful, and sophisticated AI assistant.
You are knowledgeable, efficient, and have a friendly personality.
You remember previous conversations and provide contextual responses.
You help with tasks, answer questions, and engage in meaningful conversations.
Keep responses concise but informative.
"""
        
        # Combine system prompt with context and user query
        if context:
            full_prompt = system_prompt.strip() + "\n\n" + context + "\nUser: " + query + "\nJARVIS:"
        else:
            full_prompt = system_prompt.strip() + "\n\nUser: " + query + "\nJARVIS:"
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": full_prompt,
            "stream": True
        }
        response = requests.post(url, json=payload, stream=True)
        reply = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if '"response":"' in data:
                    part = data.split('"response":"')[1].split('"')[0]
                    reply += part
        
        final_reply = reply.strip()
        final_reply = clean_reply(final_reply)
        print(final_reply)
        
        # Save conversation to history
        if final_reply and final_reply != "Error":
            add_conversation(query, final_reply)
        
        # Browser integration
        if final_reply.startswith('[BROWSER:') and final_reply.endswith(']'):
            try:
                command = final_reply[len('[BROWSER:'): -1].strip()
                parts = command.split(' ', 1)
                if len(parts) == 2:
                    action, value = parts
                    browser = BrowserController()
                    page = browser.launch_browser()
                    if action.lower() == 'open':
                        page.goto(value)
                        speak(f"Opened {value} in browser.")
                    elif action.lower() == 'click':
                        page.click(value)
                        speak(f"Clicked {value} in browser.")
                    elif action.lower() == 'fill':
                        selector_and_text = value.split(' ', 1)
                        if len(selector_and_text) == 2:
                            selector, text = selector_and_text
                            page.fill(selector, text)
                            speak(f"Filled {selector} with {text}.")
                    browser.close_browser()
                    return f"Browser action performed: {command}"
                else:
                    speak("Sorry, I couldn't understand the browser command.")
                    return "Error"
            except Exception as e:
                speak(f"Browser error: {e}")
                return f"Browser error: {e}"
        else:
            speak(final_reply)
            return final_reply
    except Exception as e:
        print(f"Ollama Error: {e}")
        speak("Sorry, I couldn't respond right now.")
        return "Error"
    
# Initialize recognizer and microphone

recognizer = sr.Recognizer()
mic = sr.Microphone()
# Function to listen user continuously
def listen_user():
    with mic as source:
        print("🎙 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("⌛ Timeout, no speech detected")
            return ""

    try:
        query = recognizer.recognize_google(audio, language="en-IN")
        print(f"👉 User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("😶 Could not understand audio")
        return ""
    except sr.RequestError as e:
        print(f"🌐 API Error: {e}")
        return ""
    except Exception as e:
        print(f"⚠️ Unexpected Error: {e}")
        return ""


@eel.expose
def start_live_conversation():
    speak("Live conversation started, I am listening...")

    while True:
        query = listen_user()

        if query in ["exit", "stop", "quit", "bye"]:
            speak("Okay, exiting live mode 👋")
            break

        if query.strip() == "":
            continue  

        reply = chatBot(query)

    speak("Back to initial state ✅")
    return None

 

def clean_reply(text: str) -> str:
    # Markdown / formatting characters remove karna
    text = re.sub(r"[*_`#~>|]", "", text)
    # Extra backslashes remove
    text = text.replace("\\", "")
    # Multiple spaces/newlines ko normalize karna
    text = re.sub(r"\s+", " ", text)
    return text.strip()