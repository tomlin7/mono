"""For high resolution displays, to make the terminal more readable and less blurry.
NOTE: this is windows specific."""

import platform

from mono.shells import Default
import tkinter as tk

root = tk.Tk()

if platform.system() == "Windows":
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

    GWL_EXSTYLE=-20
    WS_EX_APPWINDOW=0x00040000
    WS_EX_TOOLWINDOW=0x00000080
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    
terminals = Default(root)
terminals.pack(fill='both', expand=True)

root.mainloop()
