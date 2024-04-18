from __future__ import annotations

import re
import typing

if typing.TYPE_CHECKING:
    from .terminal import Terminal

class OutputParser:
    def __init__(self, terminal:Terminal):
        self.terminal = terminal
    
    def parse(self, buf: str):
        display_text = ""
        i = 0
        while i < len(buf):
            match buf[i]:
                case '\x07':
                    # bell
                    ...
                case '\x08':
                    # backspace
                    ...
                case '\x09':
                    # tab
                    ...
                case '\x0a':
                    # newline
                    # self.terminal._newline()
                    ...
                case '\x0d':
                    # carriage return
                    ...
                case '\x1b':
                    # parse escape sequence
                    ...
                case _:
                    display_text += buf[i]
            i += 1
        
        return display_text
