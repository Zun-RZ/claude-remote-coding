# remote-tabs — inbox 한 줄을 어떻게 주입할지 정한다(순수 · 표준 라이브러리만).
# pty_host.inject_new 가 줄마다 부른다. 판: 저장소 뿌리 tests/test_inbox_line.py · tests/test_inject_new.py.
#
# 표지 `{no-esc}`(1.7.0): 줄 «맨 앞» 에 있으면 표지를 떼고 `/`·`!` 줄 앞의 ESC 를 생략한다.
#   그 ESC 는 열린 모달을 닫으려고 넣는 것이지만 «도는 턴» 도 끊는다 — 부르는 쪽(예: taskforce)이 턴이 끝났다고
#   확실하지 않을 때 이 표지를 붙여 끊지 않고 넣는다(Claude Code 는 도는 턴 동안 들어온 `/` 줄을 대기열에 두었다가
#   턴 뒤에 전개한다). 줄 중간 · 뒤의 표지는 뜻이 없다(그냥 글자다).
#   표지 없는 줄의 판정은 1.6.2 와 같다 — 주입 바이트도 같다.
# ⚠️ Windows ConPTY 호스트(pty_host.py)만 이 표지를 안다. tmux 브리지(bridge.sh)는 모른다 — 거기서는 글자 그대로 제출된다.

# 🔑 taskforce 판이 이 줄을 정규식 `^NO_ESC_MARK\s*=\s*"([^"]*)"\s*$` 로 읽어 자기 상수와 맞댄다 — 꼴을 바꾸지 않는다.
NO_ESC_MARK = "{no-esc}"


def plan_injection(line):
    """inbox 한 줄 → (주입할 본문, 그 앞에 ESC 를 보낼지)."""
    if line.startswith(NO_ESC_MARK):
        return line[len(NO_ESC_MARK):], False
    return line, line.startswith(("/", "!"))
