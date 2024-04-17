from mono import Terminals, Theme
import tkinter as tk

root = tk.Tk()
root.geometry('800x300')

class Light(Theme):
    bg = "#FFFFFF"
    fg = "#000000"
    abg = "#CCCCCC"
    afg = "#000000"
    border = "#DDDDDD"

terminals = Terminals(root, theme=Light())
terminals.pack(fill='both', expand=True)

terminals.add_default_terminal()

root.mainloop()
