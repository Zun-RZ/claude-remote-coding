---
name: selection-is-all-you-need
description: End every turn with an AskUserQuestion (mobile push), except on explicit stop, wait, or when no human is watching.
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
- Explicit stop signals — "stop", "exit", "끝", "그만", "종료", the fast-close
  keyword `#@stop#@`, and the like. This holds even when the signal arrives as
  an answer to a previous `AskUserQuestion` (a selected option's notes or the
  "Other" free-text input), not only as a plain message. Acknowledge briefly and
  halt — do not loop another question. (If the `remote-tabs` plugin is installed,
  `#@stop#@` is its fast-close keyword and its close-remote-tab skill will
  terminate the session; without it, just treat `#@stop#@` as a plain stop.)
- Direct-input wait mode — the single turn right after the "Type it myself"
  option.
- **Agent-driven sessions — no human is watching.** If another agent started this
  session and drives it (e.g. a worker session a lead agent spawned and instructs
  over a message bus), the push has no recipient: it fires on the human's phone
  for a turn they did not ask for and cannot act on. End those turns with prose
  and report back through whatever channel the driving agent reads. Two notes:
  - Judge by *who drives this session*, not by what the task is. A human working
    from their phone through a driving agent is still a human — if your output
    goes to a person, the rule applies.
  - This does not silence you. It moves the report to the channel the driver
    actually reads. Reserve `AskUserQuestion` for decisions that are genuinely a
    human's to make; route everything else through your driver.
- This rule applies to *open* turns only.
