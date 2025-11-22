import multiprocessing
import threading
import signal
import sys

def signal_handler(sig, frame):
    print("\nExiting gracefully...")
    sys.exit(0)

def startJarvis():
    print("Process 1 Starting...")
    from main import start
    start()
    
def listenHotword():
    print("Process 2 Starting...")
    from backend.feature import hotword
    hotword()

def run_hotword():
    try:
        hotword_thread = threading.Thread(target=listenHotword)
        hotword_thread.daemon = True  # This ensures the thread exits when the main program does
        hotword_thread.start()
    except Exception as e:
        print(f"Error starting hotword thread: {e}")
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start hotword detection in a background thread
        run_hotword()
        
        # Run Jarvis (Eel) in the main thread
        startJarvis()
    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        print("System is terminated.")