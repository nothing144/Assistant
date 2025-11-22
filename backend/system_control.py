"""
System Control Features for JARVIS
Handles volume, brightness, power, screenshots, etc.
"""
import os
import subprocess
import time
import pyautogui
from datetime import datetime
from backend.command import speak
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
import psutil


def take_screenshot():
    """Take a screenshot and save it"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(os.path.expanduser("~"), "Pictures", filename)
        
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        speak(f"Screenshot saved as {filename}")
        return f"Screenshot saved: {screenshot_path}"
    except Exception as e:
        speak("Failed to take screenshot")
        return f"Error: {str(e)}"


def set_volume(level):
    """Set system volume to specific level (0-100)"""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        # Convert percentage to scalar (0.0 to 1.0)
        volume_scalar = level / 100.0
        volume.SetMasterVolumeLevelScalar(volume_scalar, None)
        
        speak(f"Volume set to {level} percent")
        return f"Volume set to {level}%"
    except Exception as e:
        speak("Failed to set volume")
        return f"Error: {str(e)}"


def increase_volume():
    """Increase system volume by 10%"""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(1.0, current_volume + 0.1)
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        
        percentage = int(new_volume * 100)
        speak(f"Volume increased to {percentage} percent")
        return f"Volume: {percentage}%"
    except Exception as e:
        speak("Failed to increase volume")
        return f"Error: {str(e)}"


def decrease_volume():
    """Decrease system volume by 10%"""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = max(0.0, current_volume - 0.1)
        volume.SetMasterVolumeLevelScalar(new_volume, None)
        
        percentage = int(new_volume * 100)
        speak(f"Volume decreased to {percentage} percent")
        return f"Volume: {percentage}%"
    except Exception as e:
        speak("Failed to decrease volume")
        return f"Error: {str(e)}"


def mute_volume():
    """Mute system volume"""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        volume.SetMute(1, None)
        speak("Volume muted")
        return "Volume muted"
    except Exception as e:
        speak("Failed to mute volume")
        return f"Error: {str(e)}"


def unmute_volume():
    """Unmute system volume"""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        volume.SetMute(0, None)
        speak("Volume unmuted")
        return "Volume unmuted"
    except Exception as e:
        speak("Failed to unmute volume")
        return f"Error: {str(e)}"


def get_current_volume():
    """Get current system volume"""
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        current_volume = volume.GetMasterVolumeLevelScalar()
        percentage = int(current_volume * 100)
        
        speak(f"Current volume is {percentage} percent")
        return f"Volume: {percentage}%"
    except Exception as e:
        speak("Failed to get volume")
        return f"Error: {str(e)}"


def increase_brightness():
    """Increase screen brightness by 10%"""
    try:
        current = sbc.get_brightness()[0]
        new_brightness = min(100, current + 10)
        sbc.set_brightness(new_brightness)
        
        speak(f"Brightness increased to {new_brightness} percent")
        return f"Brightness: {new_brightness}%"
    except Exception as e:
        speak("Failed to increase brightness")
        return f"Error: {str(e)}"


def decrease_brightness():
    """Decrease screen brightness by 10%"""
    try:
        current = sbc.get_brightness()[0]
        new_brightness = max(0, current - 10)
        sbc.set_brightness(new_brightness)
        
        speak(f"Brightness decreased to {new_brightness} percent")
        return f"Brightness: {new_brightness}%"
    except Exception as e:
        speak("Failed to decrease brightness")
        return f"Error: {str(e)}"


def set_brightness(level):
    """Set brightness to specific level (0-100)"""
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent")
        return f"Brightness: {level}%"
    except Exception as e:
        speak("Failed to set brightness")
        return f"Error: {str(e)}"


def lock_computer():
    """Lock the computer"""
    try:
        speak("Locking computer")
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Computer locked"
    except Exception as e:
        speak("Failed to lock computer")
        return f"Error: {str(e)}"


def sleep_computer():
    """Put computer to sleep"""
    try:
        speak("Putting computer to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Computer going to sleep"
    except Exception as e:
        speak("Failed to put computer to sleep")
        return f"Error: {str(e)}"


def shutdown_computer():
    """Shutdown the computer"""
    try:
        speak("Shutting down computer in 10 seconds")
        os.system("shutdown /s /t 10")
        return "Computer shutting down"
    except Exception as e:
        speak("Failed to shutdown computer")
        return f"Error: {str(e)}"


def restart_computer():
    """Restart the computer"""
    try:
        speak("Restarting computer in 10 seconds")
        os.system("shutdown /r /t 10")
        return "Computer restarting"
    except Exception as e:
        speak("Failed to restart computer")
        return f"Error: {str(e)}"


def cancel_shutdown():
    """Cancel scheduled shutdown/restart"""
    try:
        os.system("shutdown /a")
        speak("Shutdown cancelled")
        return "Shutdown cancelled"
    except Exception as e:
        speak("Failed to cancel shutdown")
        return f"Error: {str(e)}"


def get_battery_status():
    """Get battery status"""
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            
            if battery.power_plugged:
                speak(f"Battery is at {percent} percent and charging")
            else:
                hours, remainder = divmod(battery.secsleft, 3600)
                minutes = remainder // 60
                speak(f"Battery is at {percent} percent. {hours} hours and {minutes} minutes remaining")
            
            return f"Battery: {percent}% ({plugged})"
        else:
            speak("No battery detected")
            return "No battery detected"
    except Exception as e:
        speak("Failed to get battery status")
        return f"Error: {str(e)}"


def get_wifi_status():
    """Get WiFi status"""
    try:
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], 
                              capture_output=True, text=True)
        output = result.stdout
        
        if 'State' in output and 'connected' in output.lower():
            # Extract SSID
            for line in output.split('\n'):
                if 'SSID' in line and 'BSSID' not in line:
                    ssid = line.split(':')[1].strip()
                    speak(f"Connected to {ssid}")
                    return f"Connected to: {ssid}"
        else:
            speak("WiFi is disconnected")
            return "WiFi disconnected"
    except Exception as e:
        speak("Failed to get WiFi status")
        return f"Error: {str(e)}"


def empty_recycle_bin():
    """Empty recycle bin"""
    try:
        speak("Emptying recycle bin")
        os.system("rd /s /q %systemdrive%\\$Recycle.bin")
        speak("Recycle bin emptied")
        return "Recycle bin emptied"
    except Exception as e:
        speak("Failed to empty recycle bin")
        return f"Error: {str(e)}"


def get_system_info():
    """Get system information"""
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"CPU usage is {cpu_usage} percent. "
        info += f"Memory usage is {memory.percent} percent. "
        info += f"Disk usage is {disk.percent} percent."
        
        speak(info)
        return info
    except Exception as e:
        speak("Failed to get system information")
        return f"Error: {str(e)}"
