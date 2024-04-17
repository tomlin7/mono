import tkinter as tk
from ..terminal import Terminal


class Python(Terminal):
    """Python - Looks for Python executable in path and opens that in terminal. 
    Shows Not Available in case variable is not set."""

    shell = "python"
    name = "Python"
    icon = "python"
    
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)

        if not self.shell:
            tk.Label(self, text="Python not available, report an issue otherwise.").grid()
            self.name = "Not Available"
            self.icon = "error"
            return

        self.start_service()
