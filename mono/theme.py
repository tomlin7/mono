class Theme:
    """Color theme for the terminal.

    Attributes:
        bg (str): Background color.
        fg (str): Foreground color.
        abg (str): Active background color.
        afg (str): Active foreground color.
        border (str): Border color.
        tabbar (str): Tab bar background color. This can be modified only after initialization.
        tab (tuple): Tab color scheme. This can be modified only after initialization.
        tabs (tuple): Tabs color scheme. This can be modified only after initialization.
        tab_active (tuple): Active tab color scheme. This can be modified only after initialization.
        terminal (tuple): Terminal color scheme. This can be modified only after initialization.
        scrollbar (tuple): Scrollbar color scheme. This can be modified only after initialization.
    """

    bg = "#181818"
    fg = "#8B949E"
    abg = "#2C2D2D"
    afg = "#CCCCCC"
    border = "#2A2A2A"

    def __init__(self) -> None:
        self.tabbar = self.bg
        self.tab = (self.bg, self.fg, self.abg, self.afg)
        self.tabs = (self.bg, self.fg)
        self.tab_active = (self.abg, self.afg)
        self.terminal = (self.bg, self.fg)
        self.scrollbar = (self.bg, self.abg)
