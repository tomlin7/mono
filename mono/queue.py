from __future__ import annotations

import queue
from typing import Any, Callable, List, Optional


class TerminalCommandQueue:
    """Manages command queuing and buffered execution for Mono terminals."""

    def __init__(self, executor: Optional[Callable[[str], None]] = None):
        self.queue: queue.Queue[str] = queue.Queue()
        self.executor = executor
        self.is_ready: bool = True

    def put(self, command: str) -> None:
        """Enqueues a command for execution. Flushes immediately if ready."""
        if not command:
            return
        self.queue.put(command)
        if self.is_ready:
            self.flush()

    def set_ready(self, ready: bool) -> None:
        """Sets the readiness state of the terminal. Flushes pending commands if True."""
        self.is_ready = ready
        if self.is_ready:
            self.flush()

    def flush(self) -> List[str]:
        """Flushes all queued commands and passes them to the executor."""
        executed = []
        while not self.queue.empty():
            cmd = self.queue.get()
            executed.append(cmd)
            if self.executor:
                self.executor(cmd)
        return executed

    def clear(self) -> None:
        """Clears all pending commands in the queue."""
        while not self.queue.empty():
            self.queue.get_nowait()

    @property
    def pending_count(self) -> int:
        """Returns the number of pending commands."""
        return self.queue.qsize()
