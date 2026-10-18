from mono.queue import TerminalCommandQueue


def test_command_queue_flush_when_ready():
    executed = []
    q = TerminalCommandQueue(lambda cmd: executed.append(cmd))

    q.put("echo 1")
    q.put("echo 2")

    assert executed == ["echo 1", "echo 2"]
    assert q.pending_count == 0


def test_command_queue_buffering_when_not_ready():
    executed = []
    q = TerminalCommandQueue(lambda cmd: executed.append(cmd))

    q.set_ready(False)
    q.put("echo 1")
    q.put("echo 2")

    assert executed == []
    assert q.pending_count == 2

    q.set_ready(True)
    assert executed == ["echo 1", "echo 2"]
    assert q.pending_count == 0


def test_command_queue_clear():
    q = TerminalCommandQueue()
    q.set_ready(False)
    q.put("cmd1")
    q.put("cmd2")
    assert q.pending_count == 2
    q.clear()
    assert q.pending_count == 0
