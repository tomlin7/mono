from mono import Terminals, get_available_shells, get_shell_from_name
import tkinter as tk

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
