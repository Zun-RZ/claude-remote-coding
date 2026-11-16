"""플러그인 판 계약 — 표지 `{no-esc}` 를 아는 첫 판은 1.7.0 이다.

taskforce 는 브리지 프로세스 명령줄의 판 폴더(remote-tabs/<판>/scripts/pty_host.py)가 1.7.0 이상일 때만 표지를 붙인다.
캐시 폴더 이름은 plugin.json 의 version 이다 — 표지를 아는 코드가 그보다 낮은 판으로 나가면 taskforce 가 영영 표지를 안 붙인다.
(inbox_line 을 import 하지 않는다 — 이 판의 red 는 import 오류가 아니라 «값» 으로 보여야 한다.)
"""
import json
import os
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGIN_JSON = os.path.join(REPO, "plugins", "remote-tabs", ".claude-plugin", "plugin.json")


class PluginVersion(unittest.TestCase):
    def test_pc2_plugin_version_knows_mark(self):
        with open(PLUGIN_JSON, encoding="utf-8") as f:
            version = json.load(f)["version"]
        parts = tuple(int(p) for p in version.split("."))
        self.assertEqual(len(parts), 3, version)
        self.assertGreaterEqual(parts, (1, 7, 0), version)


if __name__ == "__main__":
    unittest.main()
