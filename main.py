import os
import eel
from backend.auth import recoganize
from backend.auth.recoganize import AuthenticateFace
from backend.feature import *
from backend.command import *



def start():
    try:
        eel.init("frontend") 
        
        @eel.expose
        def init():
            try:
                eel.hideLoader()
                speak("Welcome to Jarvis")
                speak("Ready for Face Authentication")
                flag = recoganize.AuthenticateFace()
                if flag == 1:
                    speak("Face recognized successfully")
                    eel.hideFaceAuth()
                    eel.hideFaceAuthSuccess()
                    speak("Welcome to Your Assistant")
                    eel.hideStart()
                    play_assistant_sound()
                    return True
                else:
                    speak("Face not recognized. Please try again")
                    return False
            except Exception as e:
                print(f"Error in init: {e}")
                return False

        os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
        eel.start("index.html", mode=None, host="localhost", block=True)
    except Exception as e:
        print(f"Error starting Eel: {e}")
        return False
    os.system('start msedge.exe --app="http://127.0.0.1:8000/index.html"')
    
    
    
    eel.start("index.html", mode=None, host="localhost", block=True) 

