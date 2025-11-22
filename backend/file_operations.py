"""
File Operations for JARVIS
Handles file and folder operations
"""
import os
import shutil
import subprocess
from backend.command import speak
from pathlib import Path


def search_file(filename):
    """Search for a file in common locations"""
    try:
        speak(f"Searching for {filename}")
        
        # Common search locations
        search_paths = [
            os.path.expanduser("~"),  # User home
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
            os.path.join(os.path.expanduser("~"), "Pictures"),
            os.path.join(os.path.expanduser("~"), "Videos"),
            os.path.join(os.path.expanduser("~"), "Music"),
        ]
        
        found_files = []
        
        for path in search_paths:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if filename.lower() in file.lower():
                        found_files.append(os.path.join(root, file))
                        if len(found_files) >= 5:  # Limit to 5 results
                            break
                if len(found_files) >= 5:
                    break
        
        if found_files:
            speak(f"Found {len(found_files)} file(s)")
            # Open first found file
            os.startfile(found_files[0])
            return f"Found: {', '.join(found_files)}"
        else:
            speak(f"File {filename} not found")
            return "File not found"
            
    except Exception as e:
        speak("Failed to search file")
        return f"Error: {str(e)}"


def open_folder(folder_name):
    """Open a folder"""
    try:
        # Common folders mapping
        folders = {
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
            "videos": os.path.join(os.path.expanduser("~"), "Videos"),
            "music": os.path.join(os.path.expanduser("~"), "Music"),
            "home": os.path.expanduser("~"),
        }
        
        folder_name = folder_name.lower().strip()
        
        if folder_name in folders:
            path = folders[folder_name]
            os.startfile(path)
            speak(f"Opening {folder_name} folder")
            return f"Opened: {path}"
        else:
            speak(f"Folder {folder_name} not found")
            return "Folder not found"
            
    except Exception as e:
        speak("Failed to open folder")
        return f"Error: {str(e)}"


def create_folder(folder_name, location="desktop"):
    """Create a new folder"""
    try:
        locations = {
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        }
        
        base_path = locations.get(location.lower(), locations["desktop"])
        folder_path = os.path.join(base_path, folder_name)
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            speak(f"Folder {folder_name} created on {location}")
            return f"Created: {folder_path}"
        else:
            speak(f"Folder {folder_name} already exists")
            return "Folder already exists"
            
    except Exception as e:
        speak("Failed to create folder")
        return f"Error: {str(e)}"


def delete_file(filename):
    """Delete a file (from Desktop)"""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop, filename)
        
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
                speak(f"File {filename} deleted")
                return f"Deleted: {file_path}"
            else:
                speak(f"{filename} is not a file")
                return "Not a file"
        else:
            speak(f"File {filename} not found on desktop")
            return "File not found"
            
    except Exception as e:
        speak("Failed to delete file")
        return f"Error: {str(e)}"


def delete_folder(folder_name):
    """Delete a folder (from Desktop)"""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_path = os.path.join(desktop, folder_name)
        
        if os.path.exists(folder_path):
            if os.path.isdir(folder_path):
                shutil.rmtree(folder_path)
                speak(f"Folder {folder_name} deleted")
                return f"Deleted: {folder_path}"
            else:
                speak(f"{folder_name} is not a folder")
                return "Not a folder"
        else:
            speak(f"Folder {folder_name} not found on desktop")
            return "Folder not found"
            
    except Exception as e:
        speak("Failed to delete folder")
        return f"Error: {str(e)}"


def copy_file(filename, destination="documents"):
    """Copy a file from Desktop to another location"""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        source = os.path.join(desktop, filename)
        
        destinations = {
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
        }
        
        dest_path = destinations.get(destination.lower(), destinations["documents"])
        dest_file = os.path.join(dest_path, filename)
        
        if os.path.exists(source):
            shutil.copy2(source, dest_file)
            speak(f"File {filename} copied to {destination}")
            return f"Copied to: {dest_file}"
        else:
            speak(f"File {filename} not found on desktop")
            return "File not found"
            
    except Exception as e:
        speak("Failed to copy file")
        return f"Error: {str(e)}"


def move_file(filename, destination="documents"):
    """Move a file from Desktop to another location"""
    try:
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        source = os.path.join(desktop, filename)
        
        destinations = {
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
        }
        
        dest_path = destinations.get(destination.lower(), destinations["documents"])
        dest_file = os.path.join(dest_path, filename)
        
        if os.path.exists(source):
            shutil.move(source, dest_file)
            speak(f"File {filename} moved to {destination}")
            return f"Moved to: {dest_file}"
        else:
            speak(f"File {filename} not found on desktop")
            return "File not found"
            
    except Exception as e:
        speak("Failed to move file")
        return f"Error: {str(e)}"


def open_file(filename):
    """Open a file with default application"""
    try:
        # Search in common locations
        search_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "Documents"),
            os.path.join(os.path.expanduser("~"), "Downloads"),
        ]
        
        for path in search_paths:
            file_path = os.path.join(path, filename)
            if os.path.exists(file_path):
                os.startfile(file_path)
                speak(f"Opening {filename}")
                return f"Opened: {file_path}"
        
        speak(f"File {filename} not found")
        return "File not found"
        
    except Exception as e:
        speak("Failed to open file")
        return f"Error: {str(e)}"
