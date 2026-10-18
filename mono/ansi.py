import re

# Match 2J or 3J (Erase Display) to clear the screen
CSI_CLEAR = re.compile(r"\x1b\[[23]J")

# Match cursor newline / positioning at column 1 (e.g. \x1b[24;1H)
CSI_NEWLINE = re.compile(r"\x1b\[\d+;1H")

# Match Operating System Command sequences:
# ESC ] ... (terminated by BEL (\x07) or ST (\x1b\))
OSC_SEQ = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\|$)")

# Match SGR (Select Graphic Rendition) sequences: e.g. \x1b[31m, \x1b[38;5;196m
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


def xterm_to_hex(n: int) -> str:
    """Converts xterm 256-color index to hexadecimal color string."""
    if n < 0:
        return "#ffffff"
    if n < 16:
        standard = [
            "#000000",
            "#cd3131",
            "#0dbc79",
            "#e5e510",
            "#2472c8",
            "#bc3fbc",
            "#11a8cd",
            "#e5e5e5",
            "#666666",
            "#f14c4c",
            "#23d18b",
            "#f5f543",
            "#3b8eea",
            "#d670d6",
            "#29b8db",
            "#ffffff",
        ]
        return standard[n]
    elif 16 <= n <= 231:
        n -= 16
        b = (n % 6) * 51 if (n % 6) else 0
        g = ((n // 6) % 6) * 51 if ((n // 6) % 6) else 0
        r = (n // 36) * 51 if (n // 36) else 0
        return f"#{r:02x}{g:02x}{b:02x}"
    elif 232 <= n <= 255:
        gray = 8 + (n - 232) * 10
        return f"#{gray:02x}{gray:02x}{gray:02x}"
    return "#ffffff"


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
    """Parses ANSI SGR color (standard, 256-color, 24-bit truecolor) and formatting into styled segments.

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

        params_str = match.group(1)
        if not params_str or params_str == "0":
            current_tags.clear()
        else:
            tokens = [int(p) for p in params_str.split(";") if p.isdigit()]
            idx = 0
            while idx < len(tokens):
                code = tokens[idx]
                if code == 0:
                    current_tags.clear()
                    idx += 1
                elif code == 1:
                    current_tags.add("bold")
                    idx += 1
                elif code == 4:
                    current_tags.add("underline")
                    idx += 1
                # 38;5;n -> 256-color foreground
                elif code == 38 and idx + 2 < len(tokens) and tokens[idx + 1] == 5:
                    color_num = tokens[idx + 2]
                    current_tags = {t for t in current_tags if not t.startswith("fg_")}
                    current_tags.add(f"fg_c{color_num}")
                    idx += 3
                # 38;2;r;g;b -> 24-bit truecolor foreground
                elif code == 38 and idx + 4 < len(tokens) and tokens[idx + 1] == 2:
                    r, g, b = tokens[idx + 2], tokens[idx + 3], tokens[idx + 4]
                    current_tags = {t for t in current_tags if not t.startswith("fg_")}
                    current_tags.add(f"fg_rgb_{r}_{g}_{b}")
                    idx += 5
                # 48;5;n -> 256-color background
                elif code == 48 and idx + 2 < len(tokens) and tokens[idx + 1] == 5:
                    color_num = tokens[idx + 2]
                    current_tags = {t for t in current_tags if not t.startswith("bg_")}
                    current_tags.add(f"bg_c{color_num}")
                    idx += 3
                # 48;2;r;g;b -> 24-bit truecolor background
                elif code == 48 and idx + 4 < len(tokens) and tokens[idx + 1] == 2:
                    r, g, b = tokens[idx + 2], tokens[idx + 3], tokens[idx + 4]
                    current_tags = {t for t in current_tags if not t.startswith("bg_")}
                    current_tags.add(f"bg_rgb_{r}_{g}_{b}")
                    idx += 5
                elif code in FG_COLORS:
                    current_tags = {t for t in current_tags if not t.startswith("fg_")}
                    current_tags.add(f"fg_{FG_COLORS[code]}")
                    idx += 1
                elif code in BG_COLORS:
                    current_tags = {t for t in current_tags if not t.startswith("bg_")}
                    current_tags.add(BG_COLORS[code])
                    idx += 1
                elif code == 39:
                    current_tags = {t for t in current_tags if not t.startswith("fg_")}
                    idx += 1
                elif code == 49:
                    current_tags = {t for t in current_tags if not t.startswith("bg_")}
                    idx += 1
                else:
                    idx += 1

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
