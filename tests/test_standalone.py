import pytest
import tkinter as tk

from mono import Default

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def default(root):
    return Default(root)

def test_default(default):
    assert default.shell
    assert default.available
    assert default.icon != 'error'
    assert default.alive


def test_terminal_text_clear_input_mark(default):
    default.text.insert("end", "user@host:~$ ")
    default.text.mark_set("input", "insert")
    default.text.insert("end", "ls")
    default.clear()
    assert default.text.index("input") == default.text.index("insert")
    assert default.text.get("1.0", "end-1c") == "user@host:~$ "


def test_enter_command_extraction(default):
    default.text.insert("end", "Prompt> ")
    default.text.mark_set("input", "insert")
    default.text.insert("end", "echo hello")
    default.enter()
    assert default.last_command == "echo hello"


# def test_button_click(standalone):
#     # pressed = False
#     # def button_click_mock():
#     #     nonlocal pressed
#     #     pressed = True
        
#     # button.config(command=button_click_mock)
#     # button.invoke()
#     # assert pressed
