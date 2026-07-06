---
name: open-remote-tab
description: Use when the user asks to open a new background session, a new
  remote tab, or a session they can drive from their phone / the Claude mobile
  app. Starts a detached remote-control Claude Code session for the current
  project.
---

# Open a remote-control session

Run `open-remote-tab` via the Bash tool. It starts a new background
remote-control Claude Code session for the current project and prints
`remote session started …`.

- Report that line back to the user verbatim.
- If it errors (e.g. `tmux is required`, launcher not found), surface the error
  verbatim and stop — do not retry blindly.
- Each invocation starts a NEW, independent session, so multiple remote sessions
  can run side by side for the same project.

The new session appears in your claude.ai/code (web) and Claude mobile app
session list. Note: a remote-control session is NOT saved locally — the
conversation lives only on the web.

## Window mode (type locally): `REMOTE_TABS_WINDOW`

On Windows the session runs **with no window** by default (headless ConPTY host).
If the user asks to **open a window**, **type/drive it locally**, or **use
Korean/IME input directly** — e.g. "창 열어서 세션 열어줘", "로컬에서 직접
타이핑하게", "open the session in a window" — start it with the
`REMOTE_TABS_WINDOW` env var set:

```sh
REMOTE_TABS_WINDOW=1 open-remote-tab
```

The bash-tool inline prefix is enough: the var is inherited through the launcher
into the `.ps1`, which opens a console window for the session. That gives
`pty_host` a real console stdin and re-enables its local input forwarding — focus
the window and type directly. Any value other than empty / `0` / `false` / `no` /
`off` (any case) turns it on; the plain `open-remote-tab` keeps the default
no-window mode. (Unix/tmux has no window concept, so the var is ignored there.)
