import pytest
from mono.ansi import clean_ansi, replace_newline, strip_ansi_escape_sequences


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


def test_replace_newline():
    raw = "a\x1b[5;1Hb"
    assert replace_newline(raw) == "a\nb"
