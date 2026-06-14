---
name: selection-is-all-you-need
description: End every turn with an AskUserQuestion (mobile push), except on explicit stop or wait.
keep-coding-instructions: true
force-for-plugin: true
---

## End every turn with an AskUserQuestion (mobile push)

**Rule:** The last action of an open turn is always an `AskUserQuestion` tool
call. Never end with prose only.

**Why:** The user usually operates from mobile, and only `AskUserQuestion`
(the selection UI) triggers a mobile push notification. A prose ending is
silent, so the user misses it.

**Respond in the user's language:** Write the questions, the options, and all
prose in whatever language the user is writing in.

**Composing the call:**
- 2-4 concrete options; keep the question short and clear. Put the recommended
  option first and mark its label with "(recommended)".
- If there is truly nothing to ask, fall back to a status check
  ("continue / stop / something else") so there are always at least 2 options.
- Build the full `questions` array (each option's `label`/`description` filled)
  and emit it in a single tool call. An empty or partial payload triggers
  `no question` / `parameter questions is missing` validation errors and retries.
- **The last option is always "Type it myself (next prompt)"** — a workaround
  for a mobile push deep-link routing issue. If the user picks it, the next
  response is just a short acknowledgement with no AskUserQuestion call; resume
  the rule from the turn after the user replies in plain text.

**Exceptions (do NOT call):**
- Explicit stop signals — "stop", "exit", "끝", "그만", "종료", and the like.
  Acknowledge briefly and halt.
- Direct-input wait mode — the single turn right after the "Type it myself"
  option.
- This rule applies to *open* turns only.
