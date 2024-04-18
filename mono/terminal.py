import os
import re
import tkinter as tk
from threading import Thread
from tkinter import ttk

if os.name == 'nt':
    from winpty import PtyProcess as PTY
else:
    from ptyprocess import PtyProcessUnicode as PTY

from mono.ansi import OutputParser
from mono.theme import Theme
from mono.utils import Scrollbar

from .text import TerminalText


class Terminal(ttk.Frame):
    """Terminal abstract class. All shell types should inherit from this class.
    The inherited class should implement following attributes:
        name (str): Name of the terminal.
        shell (str): command / path to shell executable.
        
    Args:
        master (tk.Tk): Main window.
        cwd (str): Working directory."""
    
    name: str
    shell: str

    def __init__(self, master, cwd=".", theme: Theme=None, standalone=True, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.standalone = standalone
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.alive = False
        self.cwd = cwd
        self.p = None

        if self.standalone:
            self.base = self

            from .styles import Styles
            from .theme import Theme
            self.theme = theme or Theme()
            self.style = Styles(self, self.theme)
        else:
            self.base = master.base
            self.theme = self.base.theme

        self.text = TerminalText(self, relief=tk.FLAT, padx=10, pady=10, font=("Consolas", 11))
        self.text.config(bg=self.theme.terminal[0], fg=self.theme.terminal[1], insertbackground=self.theme.terminal[1])
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        self.text.bind("<Return>", self.enter)

        self.parser = OutputParser(self)

        self.terminal_scrollbar = Scrollbar(self, style="MonoScrollbar")
        self.terminal_scrollbar.grid(row=0, column=1, sticky='NSW')

        self.text.config(yscrollcommand=self.terminal_scrollbar.set)
        self.terminal_scrollbar.config(command=self.text.yview, orient=tk.VERTICAL)

        self.text.tag_config("prompt", foreground="orange")
        self.text.tag_config("command", foreground="yellow")

        self.bind("<Destroy>", self.stop_service)
    
    def check_shell(self):
        """Check if the shell is available in the system path."""
        
        import shutil
        self.shell = shutil.which(self.shell)
        return self.shell
    
    def start_service(self, *_) -> None:
        """Start the terminal service."""

        self.alive = True
        self.last_command = None
        
        self.p = PTY.spawn([self.shell])
        Thread(target=self._write_loop, daemon=True).start()

    def stop_service(self, *_) -> None:
        """Stop the terminal service."""

        self.alive = False

    def run_command(self, command: str) -> None:
        """Run a command in the terminal.
        TODO: Implement a queue for running multiple commands."""

        self.text.insert("end", command, "command")
        self.enter()

    def clear(self) -> None:
        """Clear the terminal."""
        
        self.text.clear()

    def enter(self, *_) -> None:
        """Enter key event handler for running commands."""

        command = self.text.get('input', 'end')
        self.last_command = command
        self.text.register_history(command)
        if command.strip():
            self.text.delete('input', 'end')

        self.p.write(command + "\r\n")
        return "break"

    def _write_loop(self) -> None:
        while self.alive:
            if buf := self.p.read():
                self._insert('\n'.join(self.parser.parse(buf)))

    def _insert(self, output: str, tag='') -> None:
        self.text.insert(tk.END, output, tag)
        #self.terminal.tag_add("prompt", "insert linestart", "insert")
        self.text.see(tk.END)
        self.text.mark_set('input', 'insert')
    
    def _newline(self):
        self._insert('\n')

    # TODO: Implement a better way to handle key events.
    def _ctrl_key(self, key: str) -> None:
        if key == 'c':
            self.run_command('\x03')
            
    def __str__(self) -> str:
        return self.name
