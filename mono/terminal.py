import os
import queue
import tkinter as tk
from threading import Thread
from tkinter import font as tkfont
from tkinter import ttk

if os.name == "nt":
    from winpty import PtyProcess as PTY
else:
    from ptyprocess import PtyProcessUnicode as PTY

from mono.queue import TerminalCommandQueue
from mono.theme import Theme
from mono.utils import Scrollbar

from .ansi import (
    clean_ansi,
    parse_ansi_styled,
    replace_newline,
    strip_ansi_escape_sequences,
    xterm_to_hex,
)
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

    def __init__(
        self, master, cwd=".", theme: Theme = None, standalone=True, *args, **kwargs
    ) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.standalone = standalone
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.alive = False
        self.cwd = cwd
        self.p = None
        self._output_queue = queue.Queue()
        self.command_queue = TerminalCommandQueue(self._execute_command)
        self._last_cols = 80
        self._last_rows = 24

        if self.standalone:
            self.base = self

            from .styles import Styles
            from .theme import Theme

            self.theme = theme or Theme()
            self.style = Styles(self, self.theme)
        else:
            self.base = master.base
            self.theme = self.base.theme

        self._font = tkfont.Font(family="Consolas", size=11)
        self.text = TerminalText(
            self, relief=tk.FLAT, padx=10, pady=10, font=self._font
        )
        self.text.config(
            bg=self.theme.terminal[0],
            fg=self.theme.terminal[1],
            insertbackground=self.theme.terminal[1],
        )
        self.text.grid(row=0, column=0, sticky=tk.NSEW)
        self.text.bind("<Return>", self.enter)
        self.text.bind("<Control-c>", lambda e: self._ctrl_c())
        self.text.bind("<Control-l>", lambda e: self._ctrl_l())
        self.text.bind("<Control-u>", lambda e: self._ctrl_u())

        self.terminal_scrollbar = Scrollbar(self, style="MonoScrollbar")
        self.terminal_scrollbar.grid(row=0, column=1, sticky="NSW")

        self.text.config(yscrollcommand=self.terminal_scrollbar.set)
        self.terminal_scrollbar.config(command=self.text.yview, orient=tk.VERTICAL)

        self._init_tags()

        self.bind("<Destroy>", self.stop_service)
        self.bind("<Configure>", self._on_resize)
        self.after(20, self._process_queue)

    def _init_tags(self) -> None:
        """Configures font styling and standard 16-color ANSI tags."""
        self.text.tag_config("prompt", foreground="orange")
        self.text.tag_config("command", foreground="yellow")
        self.text.tag_config("bold", font=("Consolas", 11, "bold"))
        self.text.tag_config("underline", underline=True)

        # Standard foreground colors
        fg_map = {
            "fg_black": "#000000",
            "fg_red": "#cd3131",
            "fg_green": "#0dbc79",
            "fg_yellow": "#e5e510",
            "fg_blue": "#2472c8",
            "fg_magenta": "#bc3fbc",
            "fg_cyan": "#11a8cd",
            "fg_white": "#e5e5e5",
            "fg_bright_black": "#666666",
            "fg_bright_red": "#f14c4c",
            "fg_bright_green": "#23d18b",
            "fg_bright_yellow": "#f5f543",
            "fg_bright_blue": "#3b8eea",
            "fg_bright_magenta": "#d670d6",
            "fg_bright_cyan": "#29b8db",
            "fg_bright_white": "#ffffff",
        }
        for tag, color in fg_map.items():
            self.text.tag_config(tag, foreground=color)

        # Background colors
        bg_map = {
            "bg_black": "#000000",
            "bg_red": "#cd3131",
            "bg_green": "#0dbc79",
            "bg_yellow": "#e5e510",
            "bg_blue": "#2472c8",
            "bg_magenta": "#bc3fbc",
            "bg_cyan": "#11a8cd",
            "bg_white": "#e5e5e5",
            "bg_bright_black": "#666666",
            "bg_bright_red": "#f14c4c",
            "bg_bright_green": "#23d18b",
            "bg_bright_yellow": "#f5f543",
            "bg_bright_blue": "#3b8eea",
            "bg_bright_magenta": "#d670d6",
            "bg_bright_cyan": "#29b8db",
            "bg_bright_white": "#ffffff",
        }
        for tag, color in bg_map.items():
            self.text.tag_config(tag, background=color)

    def check_shell(self):
        """Check if the shell is available in the system path."""

        import shutil

        self.shell = shutil.which(self.shell)
        return self.shell

    def start_service(self, *_) -> None:
        """Start the terminal service."""

        self.alive = True
        self.last_command = None

        cmd = self.shell if isinstance(self.shell, list) else [self.shell]
        self.p = PTY.spawn(cmd, cwd=self.cwd)
        Thread(target=self._write_loop, daemon=True).start()

    def stop_service(self, *_) -> None:
        """Stop the terminal service and terminate child PTY process."""

        self.alive = False
        if self.p is not None:
            try:
                self.p.close()
            except Exception:
                pass
            self.p = None

    def run_command(self, command: str) -> None:
        """Enqueues and runs a command in the terminal."""
        self.command_queue.put(command)

    def _execute_command(self, command: str) -> None:
        """Directly writes a command to the terminal."""
        self.text.insert("end", command, "command")
        self.enter()

    def enter(self, *_) -> None:
        """Enter key event handler for running commands."""

        command = self.text.get("input", "end")
        self.last_command = command
        self.text.register_history(command)
        if command.strip():
            self.text.delete("input", "end")

        if self.p is not None:
            self.p.write(command + "\r\n")
        return "break"

    def _ctrl_c(self) -> str:
        """Handles Ctrl+C interruption."""
        if self.text.tag_ranges("sel"):
            # If user has text selected, let standard copy proceed
            return ""

        if self.p is not None:
            try:
                self.p.sendintr()
            except Exception:
                self.p.write("\x03")
        return "break"

    def _ctrl_l(self) -> str:
        """Handles Ctrl+L to clear the terminal."""
        self.clear()
        return "break"

    def _ctrl_u(self) -> str:
        """Handles Ctrl+U to clear current input line."""
        self.text.delete("input", "end")
        return "break"

    def _on_resize(self, event: tk.Event) -> None:
        """Synchronizes PTY window size when the widget is resized."""
        if not self.alive or self.p is None:
            return

        char_w = self._font.measure("M")
        char_h = self._font.metrics("linespace")
        if char_w <= 0 or char_h <= 0:
            return

        # Subtract padding
        usable_w = max(event.width - 20, char_w)
        usable_h = max(event.height - 20, char_h)

        cols = max(10, usable_w // char_w)
        rows = max(4, usable_h // char_h)

        if (cols, rows) != (self._last_cols, self._last_rows):
            self._last_cols = cols
            self._last_rows = rows
            try:
                self.p.setwinsize(rows, cols)
            except Exception:
                pass

    def _write_loop(self) -> None:
        while self.alive:
            try:
                if buf := self.p.read():
                    should_clear, segments = parse_ansi_styled(buf)
                    if should_clear:
                        self._output_queue.put(("clear", ""))
                    if segments:
                        self._output_queue.put(("insert_segments", segments))
            except Exception:
                break

    def _process_queue(self) -> None:
        """Processes pending output chunks in the Tkinter main thread."""
        try:
            while not self._output_queue.empty():
                action, payload = self._output_queue.get_nowait()
                if action == "clear":
                    self.clear()
                elif action == "insert_segments":
                    self._insert_segments(payload)
                elif action == "insert":
                    self._insert(payload)
        finally:
            if self.alive or not self._output_queue.empty():
                self.after(20, self._process_queue)

    def _ensure_tag(self, tag: str) -> None:
        """Ensures dynamic color tags (256-color or 24-bit RGB) are registered on the Text widget."""
        if tag.startswith("fg_c"):
            try:
                c_idx = int(tag[4:])
                self.text.tag_config(tag, foreground=xterm_to_hex(c_idx))
            except ValueError:
                pass
        elif tag.startswith("bg_c"):
            try:
                c_idx = int(tag[4:])
                self.text.tag_config(tag, background=xterm_to_hex(c_idx))
            except ValueError:
                pass
        elif tag.startswith("fg_rgb_"):
            try:
                parts = [int(p) for p in tag[7:].split("_")]
                if len(parts) == 3:
                    self.text.tag_config(tag, foreground=f"#{parts[0]:02x}{parts[1]:02x}{parts[2]:02x}")
            except ValueError:
                pass
        elif tag.startswith("bg_rgb_"):
            try:
                parts = [int(p) for p in tag[7:].split("_")]
                if len(parts) == 3:
                    self.text.tag_config(tag, background=f"#{parts[0]:02x}{parts[1]:02x}{parts[2]:02x}")
            except ValueError:
                pass

    def _insert_segments(self, segments: list[tuple[str, tuple[str, ...]]]) -> None:
        """Inserts styled segments into the text widget."""
        for text, tags in segments:
            if tags:
                for tag in tags:
                    self._ensure_tag(tag)
                self.text.insert(tk.END, text, tags)
            else:
                self.text.insert(tk.END, text)
        self.text.see(tk.END)
        self.text.mark_set("input", "insert")

    def _insert(self, output: str, tag="") -> None:
        self.text.insert(tk.END, output, tag)
        self.text.see(tk.END)
        self.text.mark_set("input", "insert")

    def _newline(self):
        self._insert("\n")

    def clear(self) -> None:
        """Clear the terminal."""

        self.text.clear()

    def _ctrl_key(self, key: str) -> None:
        if key == "c":
            self._ctrl_c()
        elif key == "l":
            self._ctrl_l()
        elif key == "u":
            self._ctrl_u()

    def __str__(self) -> str:
        return self.name
