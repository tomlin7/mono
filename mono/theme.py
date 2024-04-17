class Theme:
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
