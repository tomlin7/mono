import pytest
import tkinter as tk

from mono import Terminals

@pytest.fixture
def root():
    root = tk.Tk()
    yield root
    root.destroy()

@pytest.fixture
def terminals(root):
    terminals = Terminals(root)
    terminals.add_default_terminal()
    return terminals

def test_terminals(terminals):
    assert terminals.active_terminals
    assert terminals.active_terminals[0].alive
    assert terminals.active_terminals[0].shell
    assert terminals.active_terminals[0].icon != 'error'
