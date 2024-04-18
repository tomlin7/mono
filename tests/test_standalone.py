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


# def test_button_click(standalone):
#     # pressed = False
#     # def button_click_mock():
#     #     nonlocal pressed
#     #     pressed = True
        
#     # button.config(command=button_click_mock)
#     # button.invoke()
#     # assert pressed
