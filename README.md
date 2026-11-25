# herdr-claude-lab

A black-box lab for tools built around a coding agent. A lab agent drives an isolated [Herdr](https://herdr.dev/) session from outside, reads only the screen, and reports each step as "I tried X, expected Y, got Z" with a quote from the screen.

Workspace: Herdr. Harness: Claude Code. Needs `jq`, `python3`, `rsync` and `git`.

```
./lab doctor
./lab test lab-scenarios.md 1
./lab --help
```

- **Isolate:** a second Herdr session with its own socket and config, in a background tab, plus a clean copy of the project's tracked files (no `.git`, secrets, `agents/` or expectations files).
- **Drive:** `./lab hc <herdr command>` reaches only the lab session.
- **Judge:** the lab agent runs in an empty directory with one tool, Bash, limited to `lab hc` commands. The report rejects any quote that the lab never showed.
- **Stop:** `./lab stop` closes only what the lab started and lists anything left behind.

## Limits

- Run it from inside a Herdr pane.
- Claude Code in the lab reuses your login and skips your user settings (hooks, MCP servers). Your global `CLAUDE.md` and skills still load.
- No screenshots: Herdr gives pane text only.
- The lab runs as you on your machine. Use it for tools you are building, not for untrusted code.
- Every check uses model tokens.
