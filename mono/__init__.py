__version__ = "0.35.0"
__version_info__ = tuple(map(int, __version__.split('.')))

import os
import platform
import subprocess
import tkinter as tk

from mono.styles import Styles
from mono.theme import Theme

from .shells import *
from .tabs import Tabs
from .terminal import Terminal


def get_home_directory() -> str:
    if os.name == 'nt':
        return os.path.expandvars("%USERPROFILE%")
    if os.name == 'posix':
        return os.path.expanduser("~")
    return '.'

class Terminals(tk.Frame):
    """Mono's tabbed terminal manager
    
    Args:
        master (tk.Tk): Main window.
        cwd (str): Working directory.
        theme (Theme): Custom theme instance."""
    
    def __init__(self, master, cwd: str=None, theme: Theme=None, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.base = self

        self.theme = theme or Theme()
        self.styles = Styles(self, self.theme)

        self.config(bg=self.theme.border)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        self.cwd = cwd

        self.tabs = Tabs(self)
        self.tabs.grid(row=0, column=1, padx=(1, 0), sticky=tk.NS)

        self.active_terminals = []

    def add_default_terminal(self, *_) -> Default:
        """Add a default terminal to the list. Create a tab for it.
        
        Returns:
            Default: Default terminal instance."""
        
        default_terminal = Default(self, cwd=self.cwd or get_home_directory(), standalone=False)
        self.add_terminal(default_terminal)
        return default_terminal

    def add_terminals(self, terminals) -> None:
        """Append multiple terminals to list. Create tabs for them.

        Args:
            terminals (list): List of Shell types to append."""

        for terminal in terminals:
            self.add_terminal(terminal)

    def add_terminal(self, terminal: Terminal) -> None:
        """Append terminal to list. Create tab for it.

        Args:
            terminal (Terminal): Shell type to append."""

        self.active_terminals.append(terminal)
        self.tabs.add_tab(terminal)
    
    def set_cwd(self, cwd: str) -> None:
        """Set current working directory for all terminals.
        
        Args:
            cwd (str): Directory path."""
        
        self.cwd = cwd

    def open_shell(self, shell: Terminal) -> None:
        """Creates an instance and opens a shell.

        Args:
            shell (Terminal): Shell type to open (not instance)
                use add_terminal() to add existing instance."""
        
        self.add_terminal(shell(self, cwd=self.cwd or get_home_directory(), standalone=False))

    def open_another_terminal(self, cwd: str=None) -> None:
        """Opens another instance of the active terminal.
        
        Args:
            cwd (str): Directory path."""
        
        self.add_terminal(self.active_terminal_type(self, cwd=cwd or self.cwd or get_home_directory(), standalone=False))

    def delete_all_terminals(self, *_) -> None:
        """Permanently delete all terminal instances."""

        for terminal in self.active_terminals:
            terminal.destroy()

        self.tabs.clear_all_tabs()
        self.active_terminals.clear()
        self.refresh()

    def delete_terminal(self, terminal: Terminal) -> None:
        """Permanently delete a terminal instance.
        
        Args:
            terminal (Terminal): Terminal instance to delete."""

        terminal.destroy()
        self.active_terminals.remove(terminal)

    def delete_active_terminal(self, *_) -> None:
        """Permanently delete the active terminal."""
        
        try:
            self.tabs.close_active_tab()
        except IndexError:
            pass

    def set_active_terminal(self, terminal: Terminal) -> None:
        """Switch tabs to the terminal.
        
        Args:
            terminal (Terminal): Terminal instance to switch to."""

        for tab in self.tabs.tabs:
            if tab.terminal == terminal:
                self.tabs.set_active_tab(tab)
    
    def set_active_terminal_by_name(self, name: str) -> None:
        """Switch tabs to the terminal by name.
        
        Args:
            name (str): Name of the terminal to switch to."""

        for tab in self.tabs.tabs:
            if tab.terminal.name == name:
                self.tabs.set_active_tab(tab)
                break

    def clear_terminal(self, *_) -> None:
        """Clear text in the active terminal."""

        if active := self.active_terminal:
            active.clear()
        
    def run_command(self, command: str) -> None:
        """Run a command in the active terminal. If there is no active terminal,
        create a default terminal and run the command.
        
        Args:
            command (str): Command to run."""

        if not self.active_terminal:
            default = self.add_default_terminal()
            default.run_command(command)
            # this won't work, TODO: implement a queue for commands
        else:
            self.active_terminal.run_command(command)
    
    @staticmethod
    def run_in_external_console(self, command: str) -> None:
        """Run a command in an external console.
        
        Args:
            command (str): Command to run."""

        match platform.system():
            case 'Windows':
                subprocess.Popen(['start', 'cmd', '/K', command], shell=True)
            case 'Linux':
                subprocess.Popen(['x-terminal-emulator', '-e', command])
            case 'Darwin':
                subprocess.Popen(['open', '-a', 'Terminal', command])
            case _:
                print("No terminal emulator detected.")

    def open_pwsh(self, *_):
        """Create a Powershell terminal instance and open it"""

        self.open_shell(get_shell_from_name("Powershell"))

    def open_cmd(self, *_):
        """Create a Command Prompt terminal instance and open it"""

        self.open_shell(get_shell_from_name("Command Prompt"))

    def open_bash(self, *_):
        """Create a Bash terminal instance and open it"""

        self.open_shell(get_shell_from_name("Bash"))

    def open_python(self, *_):
        """Create a Python terminal instance and open it"""

        self.open_shell(get_shell_from_name("Python"))

    @property
    def active_terminal_type(self) -> Terminal:
        """Get the type of the active terminal. If there is no active 
        terminal, return Default type."""

        if active := self.active_terminal:
            return type(active)

        return Default

    @property
    def active_terminal(self) -> Terminal:
        """Get the active terminal instance."""

        if not self.tabs.active_tab:
            return

        return self.tabs.active_tab.terminal

    def refresh(self, *_) -> None:
        """Generates <<Empty>> event that can be bound to hide the terminal 
        if there are no active terminals."""

        if not self.active_terminals:
            self.event_generate("<<Empty>>", when="tail")
