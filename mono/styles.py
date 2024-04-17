from tkinter import ttk

from mono.theme import Theme


class Styles(ttk.Style):
    """Custom ttk styles for Mono terminal."""
    
    def __init__(self, master, theme: Theme, *args, **kwargs) -> None:
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.theme = master.theme
        
        self.config_scrollbar()

    def config_scrollbar(self) -> None:
        self.element_create("MonoScrollbar.trough", "from", "clam")
        self.element_create("MonoScrollbar.thumb", "from", "clam")

        self.layout("MonoScrollbar", [
            ('MonoScrollbar.trough', {
                'sticky': 'ns',
                'children': [
                    ('MonoScrollbar.thumb', {
                        'unit': '1',
                        'sticky': 'nsew'
                    })
                ]
            })
        ])


        bg, highlight = self.theme.scrollbar
        self.configure("MonoScrollbar", gripcount=0, background=bg, troughcolor=bg, bordercolor=bg, lightcolor=bg, darkcolor=bg, arrowsize=14)
        self.map("MonoScrollbar", background=[('pressed', highlight), ('!disabled', self.theme.border)])
