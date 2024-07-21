"""Example of using a custom theme with the Terminals widget.

Both the `Terminals` and `Terminal` widgets support custom theming.
Note that the themes are subclasses of the `Theme` class; it provides 
a simple interface for customizing the appearance of the terminals."""

import tkinter as tk

from mono import Terminals, Theme

root = tk.Tk()
root.geometry("800x300")


class Light(Theme):
    bg = "#FFFFFF"
    fg = "#000000"
    abg = "#CCCCCC"
    afg = "#000000"
    border = "#DDDDDD"

    # further overriding the __init__ will give more control over specific widgets:
    #
    #    def __init__(self, master=None, **kwargs):
    #        super().__init__(master, **kwargs)
    #        self.tabs = (self.bg, 'red')


terminals = Terminals(root, theme=Light())
terminals.pack(fill="both", expand=True)

terminals.open_python()
terminals.open_another_terminal()

root.mainloop()
