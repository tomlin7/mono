## Mono: Embeddable Terminal Emulator

> [!IMPORTANT]
> See [PR #4](https://github.com/tomlin7/mono/pull/4) on new output parser under development

**Mono** is a terminal emulator that can be embedded in tkinter applications. See [examples](./examples) to see mono in action. The codebase was extracted from the [**Biscuit project**](https://github.com/billyeatcookies/biscuit) and published as an embeddable widget library.

- Supports handling **multiple instances** of terminals of different shells running simultaneously.
- Comes as a standalone terminal widget & a **tabbed widget** as well, for handling different terminal instances.
- **Custom terminals** can be made; most shells available on the platform are detected by mono. 
- Themes are fully customizable by the user.

![monopreview](https://github.com/user-attachments/assets/365babe3-0ffd-4095-a8b8-ff98d0e615a7)

```py
import tkinter as tk

from mono import Terminals, get_available_shells, get_shell_from_name

root = tk.Tk()
root.geometry('800x300')

terminals = Terminals(root)
terminals.add_default_terminal()
terminals.pack(fill='both', expand=True)

# A menu for opening terminals
mbtn = tk.Menubutton(root, text="Open Terminal", relief=tk.RAISED)
menu = tk.Menu(mbtn)
for i in get_available_shells():
    menu.add_command(label=i, command=lambda i=i: terminals.open_shell(get_shell_from_name(i)))

mbtn.config(menu=menu)
mbtn.pack()
root.mainloop()
```

`Terminals` is a container for multiple terminals. It provides a simple interface for managing multiple terminals in a tabbed interface.

All the shells detected for the platform can be accessed with `get_available_shells()`. The `get_shell_from_name()` function returns a shell object from the name of the shell.

### Custom Terminals

Following example demonstrates how to create a NodeJS standalone terminal with mono.
```py
# NOTE: Due to the missing additional ANSI handling, NodeJS shell 
# might not work as expected. The issue is being fixed, see pr #4

import tkinter as tk
from mono import Terminal

class NodeJS(Terminal):
    name = "NodeJS"
    shell = "node"

root = tk.Tk()
terminal = NodeJS(root)
terminal.start_service()
terminal.pack(fill='both', expand=True)

root.mainloop()
```

### Custom Theming

Following example implements a custom light theme for mono terminals

```py
import tkinter as tk
from mono import Terminals, Theme

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


root = tk.Tk()
root.geometry("800x300")

terminals = Terminals(root, theme=Light())
terminals.pack(fill="both", expand=True)

terminals.open_python()             # open a python console
terminals.open_another_terminal()   # open another instance of active

root.mainloop()

```

## Installation
```py
pip install mono-term
```


Further...

- Shells can be run standalone or in a tabbed interface, see [examples/standalone](./examples/standalone.py).
- Custom terminals can be made by subclassing the `Terminal` class, see [examples/customshell](./examples/customshell.py).
- Custom themes can be passed to the `Terminal`, `Terminals` classes, see [examples/customtheme](./examples/customtheme.py).
- High resolution text rendering can be enabled for windows, see [examples/highres](./examples/highres.py).

For more examples, see the [examples](./examples) directory.
