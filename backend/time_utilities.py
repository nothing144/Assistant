"""
Time and Utility Features for JARVIS
"""
import time
import threading
from datetime import datetime, timedelta
from backend.command import speak
import winsound


# Global variables for timer and alarm
timer_thread = None
alarm_thread = None


def get_current_time():
    """Get current time"""
    try:
        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        speak(f"The time is {time_str}")
        return time_str
    except Exception as e:
        speak("Failed to get time")
        return f"Error: {str(e)}"


def get_current_date():
    """Get current date"""
    try:
        now = datetime.now()
        date_str = now.strftime("%B %d, %Y")
        day_name = now.strftime("%A")
        speak(f"Today is {day_name}, {date_str}")
        return f"{day_name}, {date_str}"
    except Exception as e:
        speak("Failed to get date")
        return f"Error: {str(e)}"


def get_day():
    """Get current day"""
    try:
        day_name = datetime.now().strftime("%A")
        speak(f"Today is {day_name}")
        return day_name
    except Exception as e:
        speak("Failed to get day")
        return f"Error: {str(e)}"


def set_timer(minutes):
    """Set a timer for specified minutes"""
    global timer_thread
    
    try:
        minutes = int(minutes)
        speak(f"Timer set for {minutes} minutes")
        
        def timer_alarm():
            time.sleep(minutes * 60)
            speak(f"Timer of {minutes} minutes is up!")
            # Play beep sound
            for _ in range(3):
                winsound.Beep(1000, 500)
                time.sleep(0.5)
        
        timer_thread = threading.Thread(target=timer_alarm, daemon=True)
        timer_thread.start()
        
        return f"Timer set for {minutes} minutes"
    except Exception as e:
        speak("Failed to set timer")
        return f"Error: {str(e)}"


def set_alarm(time_str):
    """Set an alarm for specific time (24-hour format HH:MM)"""
    global alarm_thread
    
    try:
        alarm_time = datetime.strptime(time_str, "%H:%M").time()
        speak(f"Alarm set for {time_str}")
        
        def alarm_ring():
            while True:
                now = datetime.now().time()
                if now.hour == alarm_time.hour and now.minute == alarm_time.minute:
                    speak("Wake up! Your alarm is ringing!")
                    # Play beep sound
                    for _ in range(5):
                        winsound.Beep(1000, 500)
                        time.sleep(0.5)
                    break
                time.sleep(30)  # Check every 30 seconds
        
        alarm_thread = threading.Thread(target=alarm_ring, daemon=True)
        alarm_thread.start()
        
        return f"Alarm set for {time_str}"
    except Exception as e:
        speak("Failed to set alarm")
        return f"Error: {str(e)}"


def calculate(expression):
    """Calculate mathematical expression"""
    try:
        # Remove common words
        expression = expression.replace("what is", "").replace("calculate", "").strip()
        expression = expression.replace("plus", "+").replace("minus", "-")
        expression = expression.replace("times", "*").replace("multiply", "*")
        expression = expression.replace("divided by", "/").replace("divide", "/")
        expression = expression.replace("x", "*")
        
        # Evaluate the expression
        result = eval(expression)
        speak(f"The answer is {result}")
        return f"{expression} = {result}"
    except Exception as e:
        speak("Failed to calculate")
        return f"Error: {str(e)}"


def tell_joke():
    """Tell a random joke using Ollama"""
    try:
        import requests
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": "Tell me a short funny joke in one or two lines."
        }
        response = requests.post(url, json=payload, stream=True)
        joke = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if '"response":"' in data:
                    part = data.split('"response":"')[1].split('"')[0]
                    joke += part
        
        joke = joke.strip()
        if joke:
            speak(joke)
            return joke
        else:
            # Fallback jokes
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ]
            import random
            joke = random.choice(jokes)
            speak(joke)
            return joke
    except Exception as e:
        # Fallback jokes
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What do you call a bear with no teeth? A gummy bear!"
        ]
        import random
        joke = random.choice(jokes)
        speak(joke)
        return joke


def tell_fact():
    """Tell a random fun fact using Ollama"""
    try:
        import requests
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3",
            "prompt": "Tell me a short interesting fun fact in one or two sentences."
        }
        response = requests.post(url, json=payload, stream=True)
        fact = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                if '"response":"' in data:
                    part = data.split('"response":"')[1].split('"')[0]
                    fact += part
        
        fact = fact.strip()
        if fact:
            speak(fact)
            return fact
        else:
            # Fallback facts
            facts = [
                "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still perfectly edible!",
                "A group of flamingos is called a flamboyance!",
                "Bananas are berries, but strawberries aren't!",
                "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion!"
            ]
            import random
            fact = random.choice(facts)
            speak(fact)
            return fact
    except Exception as e:
        # Fallback facts
        facts = [
            "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still perfectly edible!",
            "A group of flamingos is called a flamboyance!",
            "Bananas are berries, but strawberries aren't!"
        ]
        import random
        fact = random.choice(facts)
        speak(fact)
        return fact
