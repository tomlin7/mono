from __future__ import annotations

import platform
import typing

from .bash import Bash
from .cmd import CommandPrompt
from .default import Default
from .powershell import PowerShell
from .python import Python

if typing.TYPE_CHECKING:
    from mono import Terminal

SHELLS = {"Default": Default, "Powershell": PowerShell, "Python": Python}

if platform.system() == "Windows":
    SHELLS["Command Prompt"] = CommandPrompt
elif platform.system() == "Linux":
    SHELLS["Bash"] = Bash


def get_available_shells() -> dict[str, Terminal]:
    """Return a list of available shells."""

    return SHELLS


def get_shell_from_name(name: str) -> Terminal | Default:
    """Return the shell class from the name.

    If the shell is not found, return the default shell for the platform.

    Args:
        name (str): The name of the shell to get.

    Returns:
        Terminal: The shell class.
    """

    return SHELLS.get(name, Default)


def register_shell(name: str, shell: Terminal) -> None:
    """Register a new shell.

    Args:
        name (str): The name of the shell.
        shell (Terminal): The shell class.
    """

    SHELLS[name] = shell


def is_shell_registered(name: str) -> bool:
    """Check if a shell is registered.

    Args:
        name (str): The name of the shell.

    Returns:
        bool: True if the shell is registered, False otherwise.
    """

    return name in SHELLS
