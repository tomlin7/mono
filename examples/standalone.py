"""A simple example of using the `mono.shells.Default` 
class to create a standalone terminal application.

There are more shells available in the `mono.shells` module.
Custom shells can be created by subclassing the `mono.Terminal` class.
See the `examples/customshell.py` file for more information."""

from mono.shells import Default
import tkinter as tk

root = tk.Tk()
terminals = Default(root)
terminals.pack(fill='both', expand=True)

root.mainloop()
