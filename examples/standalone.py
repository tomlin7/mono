from mono.shells import Default
import tkinter as tk

root = tk.Tk()
terminals = Default(root)
terminals.pack(fill='both', expand=True)

root.mainloop()
