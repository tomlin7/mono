import re

# Match 2J or 3J (Erase Display) to clear the screen
CSI_CLEAR = re.compile(r"\x1b\[[23]J")

# Match cursor newline / positioning at column 1 (e.g. \x1b[24;1H)
CSI_NEWLINE = re.compile(r"\x1b\[\d+;1H")

# Match Operating System Command sequences:
# ESC ] ... (terminated by BEL (\x07) or ST (\x1b\))
OSC_SEQ = re.compile(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\|$)")

# Match general ANSI escape sequences (CSI, control codes, etc.)
ANSI_SEQ = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


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
    text = ANSI_SEQ.sub("", text)

    # Normalize carriage returns and line feeds
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    return should_clear, text


def strip_ansi_escape_sequences(string: str) -> str:
    """Strips all ANSI escape sequences from a string."""
    _, text = clean_ansi(string)
    return text


def replace_newline(string: str) -> str:
    """Replaces newline ANSI sequences with newlines."""
    return CSI_NEWLINE.sub("\n", string)
