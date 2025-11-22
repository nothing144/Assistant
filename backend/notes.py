"""
Notes Management for JARVIS
Remember and recall notes
"""
import json
import os
from datetime import datetime
from backend.command import speak


NOTES_FILE = "jarvis_notes.json"


def load_notes():
    """Load notes from file"""
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return []


def save_notes(notes):
    """Save notes to file"""
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)


def remember_note(note_text):
    """Save a note"""
    try:
        notes = load_notes()
        
        new_note = {
            "id": len(notes) + 1,
            "text": note_text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        notes.append(new_note)
        save_notes(notes)
        
        speak(f"I'll remember that")
        return f"Note saved: {note_text}"
    except Exception as e:
        speak("Failed to save note")
        return f"Error: {str(e)}"


def recall_notes():
    """Recall all notes"""
    try:
        notes = load_notes()
        
        if not notes:
            speak("I don't have any notes saved")
            return "No notes found"
        
        speak(f"You have {len(notes)} notes")
        
        for note in notes[-5:]:  # Last 5 notes
            speak(note['text'])
        
        return f"Total notes: {len(notes)}"
    except Exception as e:
        speak("Failed to recall notes")
        return f"Error: {str(e)}"


def recall_last_note():
    """Recall the last note"""
    try:
        notes = load_notes()
        
        if not notes:
            speak("I don't have any notes saved")
            return "No notes found"
        
        last_note = notes[-1]
        speak(f"Your last note was: {last_note['text']}")
        return last_note['text']
    except Exception as e:
        speak("Failed to recall last note")
        return f"Error: {str(e)}"


def clear_notes():
    """Clear all notes"""
    try:
        save_notes([])
        speak("All notes cleared")
        return "Notes cleared"
    except Exception as e:
        speak("Failed to clear notes")
        return f"Error: {str(e)}"
