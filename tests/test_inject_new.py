"""pty_host.inject_new 가 PTY 에 쓰는 바이트 차례 — 표지 `{no-esc}` 줄은 ESC 없이, 표지 없는 줄은 0709911 과 바이트까지 같게.

pywinpty 없이 돈다: `winpty` 를 이름만 가진 가짜 모듈로 바꿔 끼운 뒤 pty_host 를 import 하고,
`time.sleep` 은 기록 목으로(mock.patch.object — 판이 끝나면 되돌린다), proc 은 write 인자를 모으는 가짜다.
"""
import os
import sys
import tempfile
import types
import unittest
from unittest import mock

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "plugins", "remote-tabs", "scripts")

_SAVED = {}
pty_host = None


def setUpModule():
    global pty_host
    for name in ("winpty", "pty_host", "inbox_line"):
        _SAVED[name] = sys.modules.get(name)
    fake = types.ModuleType("winpty")
    fake.Backend = type("Backend", (), {"ConPTY": object()})
    fake.PtyProcess = type("PtyProcess", (), {})
    sys.modules["winpty"] = fake
    sys.modules.pop("pty_host", None)
    sys.modules.pop("inbox_line", None)
    if SCRIPTS not in sys.path:
        sys.path.insert(0, SCRIPTS)
    import pty_host as mod  # noqa: E402
    pty_host = mod


def tearDownModule():
    for name, prev in _SAVED.items():
        if prev is None:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = prev


class FakeProc:
    def __init__(self):
        self.writes = []

    def write(self, data):
        self.writes.append(data)


def run_inject(lines):
    """lines 를 완결된 줄로 담은 inbox · offset 0 으로 inject_new 를 한 번 부른다 → (writes, sleeps, state 파일 글)."""
    with tempfile.TemporaryDirectory() as d:
        inbox = os.path.join(d, "t.inbox")
        state = inbox + ".offset"
        with open(inbox, "w", encoding="utf-8", newline="") as f:
            f.write("".join(line + "\n" for line in lines))
        with open(state, "w", encoding="utf-8") as f:
            f.write("0")
        proc = FakeProc()
        with mock.patch.object(pty_host.time, "sleep") as sl:
            pty_host.inject_new(proc, inbox, state)
            sleeps = [c.args[0] for c in sl.call_args_list]
        with open(state, encoding="utf-8") as f:
            st = f.read()
        return proc.writes, sleeps, st


def cases():
    esc, paste = pty_host.ESC_SETTLE, pty_host.PASTE_SETTLE
    return [
        # (줄, 기대 write 차례, 기대 sleep 차례) — 표지 없는 셋(/wake · !ls · hello)은 0709911 과 바이트까지 같다.
        ("/wake", ["\x1b", "/wake", "\r"], [esc, paste]),
        ("{no-esc}/wake", ["/wake", "\r"], [paste]),
        ("!ls", ["\x1b", "\x1b[200~!ls\x1b[201~", "\r"], [esc, paste]),
        ("{no-esc}!ls", ["\x1b[200~!ls\x1b[201~", "\r"], [paste]),
        ("hello", ["hello", "\r"], [paste]),
    ]


class InjectNew(unittest.TestCase):
    def test_pi1_each_line_write_and_sleep_order(self):
        for line, writes, sleeps in cases():
            with self.subTest(line=line):
                got_w, got_s, st = run_inject([line])
                self.assertEqual(got_w, writes)
                self.assertEqual(got_s, sleeps)
                self.assertEqual(st, "1")

    def test_pi2_five_lines_in_one_inbox(self):
        cs = cases()
        got_w, got_s, st = run_inject([c[0] for c in cs])
        self.assertEqual(got_w, [w for c in cs for w in c[1]])
        self.assertEqual(got_s, [s for c in cs for s in c[2]])
        self.assertEqual(st, "5")


if __name__ == "__main__":
    unittest.main()
