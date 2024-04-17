# NOTE: Due to the improper ANSI handling, NodeJS shell 
# does not work properly. The issue is being fixed.

import tkinter as tk
from mono import Terminal, register_shell, Terminals

class NodeJS(Terminal):
    name = "NodeJS"
    shell = "node"

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        if not self.shell:
            tk.Label(self, text="Node not available, report an issue otherwise.").grid()
            self.name = "Not Available"
            self.icon = "error"
            return

        self.start_service()

root = tk.Tk()
root.geometry('800x500')

terminals = Terminals(root)
terminals.open_shell(NodeJS)
terminals.pack(fill=tk.BOTH, expand=True)

root.mainloop()
