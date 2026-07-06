---
name: send-key
description: DEPRECATED — the Claude mobile app now supports slash commands
  natively, so this keystroke-bridge workaround is retired and no longer
  auto-triggers. The mechanism is preserved (bin/send-key still writes to the
  session inbox) for manual revival; do not invoke this skill automatically.
---

# Fire a TUI command via the keystroke bridge

> **DEPRECATED (v1.6.0).** The Claude mobile app now supports slash commands
> natively, so you no longer need this bridge to fire `/clear`, `/compact`, etc.
> from your phone — type them directly into the mobile composer. This skill no
> longer auto-triggers; the mechanism below is preserved only for manual revival.

The user wants a terminal/TUI command run in **this** session — most importantly a
built-in like `/clear`, `/compact`, `/model`, `/config`. You **cannot** run those
yourself and hooks can't either; the only way is to type them into the real TUI.
This session was started with a keystroke bridge that watches an inbox file and
types each appended line into the TUI, so you trigger the command by writing to it.

## Steps

1. The message starts with the prefix; the command is the rest:
   - `s.k X` or `send-key X` → the command is `X` (e.g. `/clear`, `!git status`)
2. Run it via the Bash tool:
   ```
   send-key <command>
   ```
   `send-key` appends the line to `$CLAUDE_BRIDGE_INBOX`; the bridge then types
   it into the TUI (slash/`!` lines get an ESC first to clear any open modal).
   Report the `queued: …` line back.
3. If `send-key` prints `not in a keystroke-bridge session`, this session wasn't
   started with the bridge — tell the user to open it with `open-remote-tab` and stop.
4. If `send-key` exits with an error that the command "opens an interactive UI" or
   is a "bare picker", that built-in needs more input than one line — relay the
   message, and for a bare picker suggest the one-line form (e.g. `/model haiku`).

Do **not** try to emulate `/clear` (or any built-in) yourself — only the injected
keystroke fires it. Just queue the line and let the bridge do the typing.
