import tkinter as tk


class TerminalText(tk.Text):
    """Text widget used to display the terminal output and to get the user input.

    Limits the editable area to text after the input mark and prevents deletion
    before the input mark. Also, it keeps a history of previously used commands.

    Args:
        master (tkinter.Tk, optional): The parent widget.
        proxy_enabled (bool, optional): Whether the proxy is enabled. Defaults to True.
    """

    def __init__(self, master=None, proxy_enabled: bool = True, **kw) -> None:
        super().__init__(master, **kw)
        self.master = master

        self.mark_set("input", "insert")
        self.mark_gravity("input", "left")

        self.proxy_enabled = proxy_enabled
        self.config(highlightthickness=0)

        self._history = []
        self._history_level = 0
        self.bind("<Up>", self.history_up)
        self.bind("<Down>", self.history_down)

        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def history_up(self, *_) -> None:
        """moves up the history and displays it"""

        if not self._history:
            return "break"

        self._history_level = max(self._history_level - 1, 0)
        self.mark_set("insert", "input")
        self.delete("input", "end")
        self.insert("input", self._history[self._history_level])

        return "break"

    def history_down(self, *_) -> None:
        """moves down the history and displays it"""

        if not self._history:
            return "break"

        self._history_level = min(self._history_level + 1, len(self._history) - 1)
        self.mark_set("insert", "input")
        self.delete("input", "end")
        self.insert("input", self._history[self._history_level])

        return "break"

    def register_history(self, command: str) -> None:
        """registers a command in the history"""

        # don't register empty commands or duplicates
        if command.strip() and (
            not self._history or command.strip() != self._history[-1]
        ):
            self._history.append(command.strip())
        self._history_level = len(self._history)

    def clear(self, *_) -> None:
        """clears the text"""

        self.proxy_enabled = False

        lastline = self.get("input linestart", "input")
        self.delete("1.0", "end")
        self.insert("end", lastline)

        self.proxy_enabled = True

    def _proxy(self, *args) -> None:
        """proxy limits the editable area to text after the input mark
        and prevents deletion before the input mark."""

        if not self.proxy_enabled:
            return self.tk.call((self._orig,) + args)

        try:
            largs = list(args)
            if args[0] == "insert":
                if self.compare("insert", "<", "input"):
                    self.mark_set("insert", "end")
            elif args[0] == "delete":
                if self.compare(largs[1], "<", "input"):
                    if len(largs) == 2:
                        return
                    largs[1] = "input"

            result = self.tk.call((self._orig,) + tuple(largs))
            return result
        except:
            # most probably some tkinter-unhandled exception
            pass
