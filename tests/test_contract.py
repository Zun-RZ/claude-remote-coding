"""플러그인 판 · README 계약 — 표지 `{no-esc}` 를 아는 첫 판은 1.7.0 이고, 그 표지는 Windows ConPTY 호스트(pty_host.py)만 안다.

taskforce 는 브리지 프로세스 명령줄의 판 폴더(remote-tabs/<판>/scripts/pty_host.py)가 1.7.0 이상일 때만 표지를 붙인다.
캐시 폴더 이름은 plugin.json 의 version 이다 — 표지를 아는 코드가 그보다 낮은 판으로 나가면 taskforce 가 영영 표지를 안 붙인다.
같은 1.7.0 의 tmux 브리지(bridge.sh)는 표지를 모른다 — README 가 그 범위를 말하지 않으면 «판만 보고» 쓰는 쪽이 리눅스 · macOS 에서
표지를 글자 그대로 제출한다.
(inbox_line 을 import 하지 않는다 — 이 판들의 red 는 import 오류가 아니라 «값» 으로 보여야 한다. 표지 글자는 test_inbox_line PB7 이
inbox_line.NO_ESC_MARK 와 맞댄다.)
"""
import json
import os
import re
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_JSON = os.path.join(REPO, "plugins", "remote-tabs", ".claude-plugin", "plugin.json")
README = os.path.join(REPO, "README.md")
MARK = "{no-esc}"


def inbox_lines_section():
    """README 의 «## Inbox lines …» 절 본문(다음 «## » 머리 앞까지). 없으면 None."""
    with open(README, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"(?ms)^## Inbox lines\b.*?(?=^## |\Z)", text)
    return m.group(0) if m else None


class PluginVersion(unittest.TestCase):
    def test_pc2_plugin_version_knows_mark(self):
        with open(PLUGIN_JSON, encoding="utf-8") as f:
            version = json.load(f)["version"]
        parts = tuple(int(p) for p in version.split("."))
        self.assertEqual(len(parts), 3, version)
        self.assertGreaterEqual(parts, (1, 7, 0), version)


class ReadmeContract(unittest.TestCase):
    def test_pc1_readme_inbox_section_names_mark_version_and_scope(self):
        sec = inbox_lines_section()
        self.assertIsNotNone(sec, "README 에 «## Inbox lines» 절이 없다")
        self.assertIn("`" + MARK + "`", sec)
        self.assertIn("1.7.0", sec)
        # 관문 B 1/3: 범위 — tmux 브리지(bridge.sh)는 표지를 모른다는 것을 같은 절이 말한다.
        self.assertIn("bridge.sh", sec)


if __name__ == "__main__":
    unittest.main()
