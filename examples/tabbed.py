"""Example of using the Terminals class to create a tabbed terminal interface.

The `Terminals` class is a container for multiple terminals. It provides a simple
interface for managing multiple terminals in a tabbed interface.

This example demonstrates how to create a tabbed terminal interface with a menu
for opening new terminals. All the registered shells are available in the menu.
The by-default registered shells are determined wrt the platform."""

import tkinter as tk

from mono import Terminals, get_available_shells, get_shell_from_name

root = tk.Tk()
root.geometry('800x300')

terminals = Terminals(root)
terminals.add_default_terminal()
terminals.pack(fill='both', expand=True)


# A menu for opening terminals
# ----------------------------
mbtn = tk.Menubutton(root, text="Open Terminal", relief=tk.RAISED)
menu = tk.Menu(mbtn)
for i in get_available_shells():
    menu.add_command(label=i, command=lambda i=i: terminals.open_shell(get_shell_from_name(i)))


mbtn.config(menu=menu)
mbtn.pack()
root.mainloop()
