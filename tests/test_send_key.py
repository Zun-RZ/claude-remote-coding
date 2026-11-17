"""send-key 는 줄 머리 `{no-esc}` 를 받지 않는다(bridge-esc-busy 리뷰 F1).

send-key 의 «UI 를 여는 명령» 가드(`/resume` · bare `/model` … → exit 3)는 줄 머리 `/` 만 본다. 1.7.0 브리지는 줄 머리
`{no-esc}` 를 떼고 나머지를 ESC 없이 넣으므로 `send-key '{no-esc}/resume'` 은 가드를 지나 `/resume` 으로 들어간다.
그래서 send-key 는 줄 머리 표지를 거부한다 — 떼고 다시 가드하지 않는다(표지를 해석하는 자리는 inbox_line 하나).

🔴 줄을 sh 의 «명령줄 인자» 로 넘기지 않는다 — Windows 에서 MSYS 런타임이 `{…}` 를 glob 으로 펼쳐 중괄호가 사라진다
(리뷰 §6 1). 실제 경로(Git Bash → send-key)처럼 sh «안» 의 driver 가 send-key 를 부르고, 줄은 환경 변수로 준다.
대조군 ` {no-esc}/x`(앞 공백 — 표지 아님)가 inbox 에 글자 그대로 남는지가 그 전달을 잰다.
🔴 CLAUDE_BRIDGE_INBOX 는 자식 환경에서 임시 파일로 «덮어쓴다» — 브리지 세션 안에서 돌려도 실제 inbox 에 안 쓴다.
"""
import os
import shutil
import subprocess
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEND_KEY = os.path.join(REPO, "plugins", "remote-tabs", "bin", "send-key")
DRIVER = 'exec sh "$SENDKEY_SCRIPT" "$SENDKEY_LINE"\n'


def find_sh():
    """PATH 의 sh(리눅스 · macOS · Git Bash 안). 없으면 git 옆 Git for Windows 의 bin/sh.exe. 둘 다 없으면 None."""
    sh = shutil.which("sh")
    if sh:
        return sh
    git = shutil.which("git")
    if git:
        cand = os.path.join(os.path.dirname(os.path.dirname(git)), "bin", "sh.exe")
        if os.path.isfile(cand):
            return cand
    return None


class SendKeyMarkGuard(unittest.TestCase):
    def setUp(self):
        self.sh = find_sh()
        self.assertIsNotNone(self.sh, "sh 를 못 찾았다(PATH · git 옆 bin/sh.exe) — 이 판은 send-key 를 sh 로 돌린다")
        self.tmp = tempfile.mkdtemp(prefix="sendkey-")
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.inbox = os.path.join(self.tmp, "fake.inbox")
        open(self.inbox, "w").close()
        self.driver = os.path.join(self.tmp, "driver.sh")
        with open(self.driver, "w", newline="\n") as f:
            f.write(DRIVER)

    def send_key(self, line):
        env = dict(os.environ, CLAUDE_BRIDGE_INBOX=self.inbox,
                   SENDKEY_SCRIPT=SEND_KEY.replace("\\", "/"), SENDKEY_LINE=line)
        p = subprocess.run([self.sh, self.driver.replace("\\", "/")], env=env,
                           capture_output=True, text=True, encoding="utf-8")
        with open(self.inbox, encoding="utf-8", newline="") as f:
            return p.returncode, f.read(), p.stderr

    def test_pk1_marked_slash_line_refused(self):
        rc, inbox, err = self.send_key("{no-esc}/resume")
        self.assertEqual((rc, inbox), (3, ""), err)
        self.assertIn("{no-esc}", err)

    def test_pk2_double_mark_refused(self):
        # 브리지는 표지를 «한 번» 뗀다 → 본문 `{no-esc}/x` 는 평문이 된다. 그래도 줄 머리 표지라 거부한다.
        rc, inbox, err = self.send_key("{no-esc}{no-esc}/x")
        self.assertEqual((rc, inbox), (3, ""), err)
        self.assertIn("{no-esc}", err)

    def test_pk3_control_bare_guard_unchanged(self):
        rc, inbox, err = self.send_key("/resume")
        self.assertEqual((rc, inbox), (3, ""), err)
        self.assertIn("'/resume'", err)

    def test_pk4_control_leading_space_is_plain(self):
        # 앞 공백 — 브리지가 표지로 안 본다(평문). 지금처럼 그대로 큐에 간다 · 중괄호가 글자 그대로 남는다.
        rc, inbox, err = self.send_key(" {no-esc}/x")
        self.assertEqual((rc, inbox), (0, " {no-esc}/x\n"), err)


if __name__ == "__main__":
    unittest.main()
