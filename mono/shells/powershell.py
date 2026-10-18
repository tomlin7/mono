import shutil
import tkinter as tk

from ..terminal import Terminal


class PowerShell(Terminal):
    """PowerShell - Looks for powershell executable in path and opens that in terminal. 
    Shows Not Available in case variable is not set."""

    shell = "powershell"
    name = "PowerShell"
    icon = "powershell"
    
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        
        self.available = self.check_shell()
        if not self.available:
            tk.Label(self, text="PowerShell not available, report an issue otherwise.").grid()
            self.name = "Not Available"
            self.icon = "error"
            return

        self.start_service()

    def start_service(self, *_) -> None:
        """Start PowerShell service without PSReadLine escape code duplication."""
        # PSReadLine redraws whole command lines on every character typed in standard PTYs,
        # which causes duplicate characters in basic terminal emulators.
        # We disable PSReadLine on launch to keep clean line-based input.
        ps_path = shutil.which("powershell") or "powershell"
        self.shell = [
            ps_path,
            "-NoExit",
            "-Command",
            "Remove-Module PSReadLine -ErrorAction SilentlyContinue",
        ]
        super().start_service()
