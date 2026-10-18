import re

# Match 2J or 3J (Erase Display) to clear the screen
CSI_CLEAR = re.compile(r"\x1b\[[23]J")

# Match cursor newline / positioning at column 1 (e.g. \x1b[24;1H)
CSI_NEWLINE = re.compile(r"\x1b\[\d+;1H")

# Match Operating System Command sequences:
# ESC ] ... (terminated by BEL (\x07) or ST (\x1b\))
OSC_SEQ = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\|$)")

# Match SGR (Select Graphic Rendition) sequences: e.g. \x1b[31m, \x1b[1;32m
ANSI_SGR = re.compile(r"\x1b\[([0-9;]*)m")

# Match general ANSI escape sequences (CSI, control codes, cursor movements, etc.)
# Excludes 'm' (SGR) so colors can be parsed separately
ANSI_OTHER = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-ln-~])")

# 16-color ANSI mapping
FG_COLORS = {
    30: "black",
    31: "red",
    32: "green",
    33: "yellow",
    34: "blue",
    35: "magenta",
    36: "cyan",
    37: "white",
    90: "bright_black",
    91: "bright_red",
    92: "bright_green",
    93: "bright_yellow",
    94: "bright_blue",
    95: "bright_magenta",
    96: "bright_cyan",
    97: "bright_white",
}

BG_COLORS = {
    40: "bg_black",
    41: "bg_red",
    42: "bg_green",
    43: "bg_yellow",
    44: "bg_blue",
    45: "bg_magenta",
    46: "bg_cyan",
    47: "bg_white",
    100: "bg_bright_black",
    101: "bg_bright_red",
    102: "bg_bright_green",
    103: "bg_bright_yellow",
    104: "bg_bright_blue",
    105: "bg_bright_magenta",
    106: "bg_bright_cyan",
    107: "bg_bright_white",
}


def clean_ansi(text: str) -> tuple[bool, str]:
    """Cleans terminal escape sequences from PTY output chunk.

    Returns:
        tuple[bool, str]: (should_clear, cleaned_text)
    """
    should_clear = bool(CSI_CLEAR.search(text))

    # Strip OSC sequences (e.g. window title setting)
    text = OSC_SEQ.sub("", text)

    # Convert cursor home/newline to standard newline
    text = CSI_NEWLINE.sub("\n", text)

    # Strip remaining ANSI escape sequences
    text = ANSI_OTHER.sub("", text)
    text = ANSI_SGR.sub("", text)

    # Normalize carriage returns and line feeds
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    return should_clear, text


def parse_ansi_styled(text: str) -> tuple[bool, list[tuple[str, tuple[str, ...]]]]:
    """Parses ANSI SGR color and formatting sequences into styled segments.

    Returns:
        tuple[bool, list[tuple[str, tuple[str, ...]]]]: (should_clear, [(segment, tags), ...])
    """
    should_clear = bool(CSI_CLEAR.search(text))

    # Strip OSC sequences
    text = OSC_SEQ.sub("", text)

    # Convert cursor positioning at column 1 to newline
    text = CSI_NEWLINE.sub("\n", text)

    # Strip non-SGR ANSI sequences
    text = ANSI_OTHER.sub("", text)

    # Normalize carriage returns
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    segments: list[tuple[str, tuple[str, ...]]] = []
    current_tags: set[str] = set()
    last_end = 0

    for match in ANSI_SGR.finditer(text):
        start, end = match.span()
        if start > last_end:
            content = text[last_end:start]
            if content:
                segments.append((content, tuple(sorted(current_tags))))

        params = match.group(1)
        if not params or params == "0":
            current_tags.clear()
        else:
            for p in params.split(";"):
                if not p:
                    continue
                try:
                    code = int(p)
                except ValueError:
                    continue

                if code == 0:
                    current_tags.clear()
                elif code == 1:
                    current_tags.add("bold")
                elif code == 4:
                    current_tags.add("underline")
                elif code in FG_COLORS:
                    current_tags = {t for t in current_tags if not t.startswith("fg_")}
                    current_tags.add(f"fg_{FG_COLORS[code]}")
                elif code in BG_COLORS:
                    current_tags = {t for t in current_tags if not t.startswith("bg_")}
                    current_tags.add(BG_COLORS[code])
                elif code == 39:
                    current_tags = {t for t in current_tags if not t.startswith("fg_")}
                elif code == 49:
                    current_tags = {t for t in current_tags if not t.startswith("bg_")}

        last_end = end

    if last_end < len(text):
        content = text[last_end:]
        if content:
            segments.append((content, tuple(sorted(current_tags))))

    return should_clear, segments


def strip_ansi_escape_sequences(string: str) -> str:
    """Strips all ANSI escape sequences from a string."""
    _, text = clean_ansi(string)
    return text


def replace_newline(string: str) -> str:
    """Replaces newline ANSI sequences with newlines."""
    return CSI_NEWLINE.sub("\n", string)
