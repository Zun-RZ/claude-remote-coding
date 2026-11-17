"""inbox 줄 표지 판정(inbox_line.plan_injection)과 README 계약.

표지 `{no-esc}` 가 줄 «맨 앞» 에 있으면 pty_host 는 표지를 떼고 `/`·`!` 줄 앞의 ESC 를 생략한다(1.7.0).
표지 없는 줄은 0709911 과 같은 판정이다(바이트 무변 — test_inject_new.py 가 바이트로 잰다).
"""
import os
import re
import sys
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(REPO, "plugins", "remote-tabs", "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)

from inbox_line import NO_ESC_MARK, plan_injection  # noqa: E402


class PlanInjection(unittest.TestCase):
    def test_pb1_unmarked_slash_keeps_esc(self):
        self.assertEqual(plan_injection("/wake"), ("/wake", True))

    def test_pb2_marked_slash_drops_esc(self):
        self.assertEqual(plan_injection("{no-esc}/wake"), ("/wake", False))

    def test_pb3_bang(self):
        self.assertEqual(plan_injection("!ls"), ("!ls", True))
        self.assertEqual(plan_injection("{no-esc}!ls"), ("!ls", False))

    def test_pb4_plain(self):
        self.assertEqual(plan_injection("hello"), ("hello", False))
        self.assertEqual(plan_injection("{no-esc}hello"), ("hello", False))

    def test_pb5_mark_elsewhere_is_text(self):
        self.assertEqual(plan_injection(" {no-esc}/wake"), (" {no-esc}/wake", False))
        self.assertEqual(plan_injection("/wake {no-esc}"), ("/wake {no-esc}", True))

    def test_pb6_empty_and_mark_only(self):
        self.assertEqual(plan_injection(""), ("", False))
        self.assertEqual(plan_injection("{no-esc}"), ("", False))

    def test_pb7_mark_constant_line_is_single_and_readable(self):
        # taskforce 판(TC1)이 이 줄 꼴을 정규식으로 읽어 자기 상수와 맞댄다 — 꼴이 바뀌면 그쪽이 조용히 못 읽는다.
        with open(os.path.join(SCRIPTS, "inbox_line.py"), encoding="utf-8") as f:
            src = f.read()
        found = re.findall(r'(?m)^NO_ESC_MARK\s*=\s*"([^"]*)"\s*$', src)
        self.assertEqual(found, [NO_ESC_MARK])
        self.assertEqual(NO_ESC_MARK, "{no-esc}")


if __name__ == "__main__":
    unittest.main()
