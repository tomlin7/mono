import pytest
from mono.ansi import (
    clean_ansi,
    parse_ansi_styled,
    replace_newline,
    strip_ansi_escape_sequences,
    xterm_to_hex,
)


def test_strip_ansi():
    raw = "\x1b[31mRed Text\x1b[0m"
    assert strip_ansi_escape_sequences(raw) == "Red Text"


def test_clean_ansi_clear():
    raw = "\x1b[H\x1b[2J\x1b[3J\x1b[1;1H\r\nPrompt>"
    should_clear, text = clean_ansi(raw)
    assert should_clear is True
    assert "Prompt>" in text


def test_clean_ansi_osc_window_title():
    raw = "\x1b]0;cmd.exe\x1b\\hello world\r\n"
    should_clear, text = clean_ansi(raw)
    assert should_clear is False
    assert text == "hello world\n"


def test_clean_ansi_cursor_col1_to_newline():
    raw = "line1\x1b[2;1Hline2"
    should_clear, text = clean_ansi(raw)
    assert should_clear is False
    assert text == "line1\nline2"


def test_clean_ansi_cursor_col1_with_preceding_newline():
    raw = "line1\r\n\x1b[2;1Hline2"
    should_clear, text = clean_ansi(raw)
    assert should_clear is False
    assert text == "line1\nline2"


def test_replace_newline():
    raw = "a\x1b[5;1Hb"
    assert replace_newline(raw) == "a\nb"


def test_replace_newline_with_preceding_newline():
    raw = "a\r\n\x1b[5;1Hb"
    assert replace_newline(raw) == "a\nb"


def test_parse_ansi_styled_colors():
    raw = "Hello \x1b[31mRed\x1b[0m \x1b[1;32mBold Green\x1b[0m World"
    should_clear, segments = parse_ansi_styled(raw)
    assert should_clear is False

    assert segments == [
        ("Hello ", ()),
        ("Red", ("fg_red",)),
        (" ", ()),
        ("Bold Green", ("bold", "fg_green")),
        (" World", ()),
    ]


def test_parse_ansi_styled_background_and_underline():
    raw = "\x1b[4;44mUnderline BlueBG\x1b[0m"
    should_clear, segments = parse_ansi_styled(raw)
    assert should_clear is False
    assert segments == [("Underline BlueBG", ("bg_blue", "underline"))]


def test_parse_ansi_256_and_truecolor():
    raw = "\x1b[38;5;196mRed256\x1b[0m \x1b[38;2;255;128;0mOrangeRGB\x1b[0m \x1b[48;5;21mBlueBG\x1b[0m"
    should_clear, segments = parse_ansi_styled(raw)
    assert should_clear is False
    assert segments == [
        ("Red256", ("fg_c196",)),
        (" ", ()),
        ("OrangeRGB", ("fg_rgb_255_128_0",)),
        (" ", ()),
        ("BlueBG", ("bg_c21",)),
    ]


def test_xterm_to_hex():
    assert xterm_to_hex(1) == "#cd3131"
    assert xterm_to_hex(196) == "#ff0000"
    assert xterm_to_hex(21) == "#0000ff"
    assert xterm_to_hex(244) == "#808080"
