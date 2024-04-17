import platform

from .bash import Bash
from .cmd import CommandPrompt
from .default import Default
from .powershell import PowerShell
from .python import Python

SHELLS = {
    "Default": Default,
    "Powershell": PowerShell,
    "Python": Python
}

if platform.system() == "Windows":
    SHELLS["Command Prompt"] = CommandPrompt
elif platform.system() == "Linux":
    SHELLS["Bash"] = Bash

def get_available_shells():
    return SHELLS

def get_shell_from_name(name):
    return SHELLS.get(name, Default)

def register_shell(name, shell):
    SHELLS[name] = shell
    
def is_shell_registered(name):
    return name in SHELLS
