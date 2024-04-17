from mono import Terminals
import tkinter as tk

root = tk.Tk()
root.geometry('800x300')

terminals = Terminals(root)
terminals.pack(fill='both', expand=True)

terminals.add_default_terminal()

root.mainloop()
