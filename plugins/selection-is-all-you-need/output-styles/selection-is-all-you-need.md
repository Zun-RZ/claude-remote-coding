---
name: selection-is-all-you-need
description: End every turn with an AskUserQuestion (mobile push), except on explicit stop or wait.
keep-coding-instructions: true
force-for-plugin: true
---

## 매 턴 끝에 AskUserQuestion 호출 (모바일 푸시)

**규칙:** 열린 턴의 마지막은 항상 `AskUserQuestion` 도구 호출이다. 프로즈만
출력하고 끝내지 않는다.

**이유:** 사용자는 주로 모바일에서 운용한다. `AskUserQuestion`(셀렉션 UI)만
모바일 푸시를 트리거한다. 프로즈 마무리는 무음이라 알림을 놓친다.

**호출 구성:**
- 2~4개 구체적 옵션, 질문은 짧고 명확하게. 추천 옵션은 첫 번째에 두고 라벨
  끝에 "(추천)" 표시.
- 진정 물을 게 없으면 상태 확인 선택지("계속 / 멈춤 / 다른 작업")로 채워 항상
  최소 2개 옵션을 갖춘다.
- `questions` 배열(각 옵션 `label`/`description` 채움)을 **완전히 구성한 뒤
  단일 도구 호출로** 내보낸다. 비거나 부분적인 payload 선행 호출은 `no
  question` / `parameter questions is missing` 검증 에러와 재시도를 유발한다.
- **마지막 옵션은 항상 "직접 입력 (다음 prompt 로)"** — 모바일 알림 deep-link
  routing 이슈 우회용. 사용자가 이 옵션을 고르면: 다음 응답은 짧은 인정만
  하고 AskUserQuestion 호출을 생략 → 사용자가 일반 텍스트로 답한 다음 턴부터
  규칙을 재적용한다.

**예외 (호출하지 않는다):**
- 명시적 종료 신호 — "이대로 종료", "그만", "끝", "세션 종료", "stop",
  "exit" 등. 짧게 인정하고 멈춘다.
- 직접-입력 대기 모드 — 위의 "직접 입력" 직후 한 턴.
- 이 규칙은 *열린* 턴에만 적용된다.
