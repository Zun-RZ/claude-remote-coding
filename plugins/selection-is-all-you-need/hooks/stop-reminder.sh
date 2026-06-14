#!/usr/bin/env bash
# Stop hook: 종료 신호가 아니면 AskUserQuestion으로 턴을 끝내라고 다음 턴에 상기.
# additionalContext 는 강제가 아니라 보강 — 최종 판단은 모델이 한다.
cat <<'JSON'
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Reminder: unless the user gave an explicit stop signal (그만/끝/stop/exit) or you are in direct-input wait mode, end this turn with a single AskUserQuestion call (2-4 options, last = 직접 입력) so it pushes to mobile."
  }
}
JSON
