"""
Enhanced App Launcher for JARVIS
Auto-detects and opens any Windows application
"""
import os
import subprocess
import winreg
from backend.command import speak
from difflib import get_close_matches


class AppLauncher:
    def __init__(self):
        self.apps = {}
        self.load_installed_apps()
    
    def load_installed_apps(self):
        """Load all installed applications from Windows Registry"""
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        
        for hkey, path in registry_paths:
            try:
                key = winreg.OpenKey(hkey, path)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            if path.endswith("App Paths"):
                                app_path = winreg.QueryValue(hkey, f"{path}\\{subkey_name}")
                            else:
                                try:
                                    app_path = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    if not app_path:
                                        app_path = winreg.QueryValueEx(subkey, "DisplayIcon")[0]
                                except:
                                    continue
                            
                            if name and app_path:
                                self.apps[name.lower()] = app_path
                        except:
                            pass
                        
                        winreg.CloseKey(subkey)
                    except:
                        continue
                
                winreg.CloseKey(key)
            except:
                continue
        
        # Add common Windows apps
        common_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "paint": "mspaint.exe",
            "wordpad": "write.exe",
            "task manager": "taskmgr.exe",
            "control panel": "control.exe",
            "command prompt": "cmd.exe",
            "powershell": "powershell.exe",
            "file explorer": "explorer.exe",
            "settings": "ms-settings:",
            "snipping tool": "SnippingTool.exe",
            "camera": "microsoft.windows.camera:",
            "mail": "outlookmail:",
            "calendar": "outlookcal:",
            "photos": "ms-photos:",
            "maps": "bingmaps:",
            "store": "ms-windows-store:",
            "xbox": "xbox:",
            "spotify": "spotify.exe",
            "chrome": "chrome.exe",
            "edge": "msedge.exe",
            "firefox": "firefox.exe",
            "vlc": "vlc.exe",
            "vscode": "code.exe",
            "visual studio code": "code.exe",
            "discord": "discord.exe",
            "steam": "steam.exe",
            "obs": "obs64.exe",
            "obs studio": "obs64.exe",
        }
        
        self.apps.update(common_apps)
    
    def find_app(self, app_name):
        """Find app using fuzzy matching"""
        app_name = app_name.lower().strip()
        
        # Direct match
        if app_name in self.apps:
            return self.apps[app_name]
        
        # Partial match
        for name, path in self.apps.items():
            if app_name in name or name in app_name:
                return path
        
        # Fuzzy match
        close_matches = get_close_matches(app_name, self.apps.keys(), n=1, cutoff=0.6)
        if close_matches:
            return self.apps[close_matches[0]]
        
        return None
    
    def open_app(self, app_name):
        """Open an application"""
        try:
            app_path = self.find_app(app_name)
            
            if app_path:
                speak(f"Opening {app_name}")
                
                # Handle special protocols
                if app_path.startswith("ms-") or app_path.endswith(":"):
                    os.system(f'start {app_path}')
                else:
                    # Try to start the application
                    try:
                        subprocess.Popen(app_path)
                    except:
                        # If direct path fails, try with 'start' command
                        os.system(f'start "" "{app_path}"')
                
                return f"Opened: {app_name}"
            else:
                # Try to open with start command as fallback
                speak(f"Trying to open {app_name}")
                try:
                    os.system(f'start {app_name}')
                    return f"Attempting to open: {app_name}"
                except:
                    speak(f"Could not find {app_name}")
                    return "App not found"
        
        except Exception as e:
            speak(f"Failed to open {app_name}")
            return f"Error: {str(e)}"


# Create global instance
app_launcher = AppLauncher()


def open_any_app(app_name):
    """Open any application by name"""
    return app_launcher.open_app(app_name)
