# Hooks Library

## What Are Hooks?

Claude Code hooks are shell scripts that run automatically at key moments in Claude's lifecycle.
They run on YOUR machine, not inside Claude — giving you hard enforcement that CLAUDE.md instructions alone can't provide.

## Hook Events

| Event | When it fires | Use for |
|---|---|---|
| `PreToolUse` | Before Claude executes any tool | Block dangerous commands, log actions |
| `PostToolUse` | After Claude executes a tool | Notifications, audit trail |
| `SessionStart` | When a Claude Code session opens | Load context, print status |
| `SessionStop` | When a session closes | Summarize, cleanup |

## Hooks Included

### Pre-Tool-Use (Safety — deterministic enforcement)
- `block-rm-rf.sh` — denies `rm -rf` outside `/tmp` via JSON deny output
- `block-force-push.sh` — denies `git push --force` and `git push -f`
- `block-test-skip.sh` — denies `--skip-tests`, `-DskipTests`, pytest skip flags
- `enforce-commit-format.sh` — denies commits not following Conventional Commits
- `log-tool-calls.sh` — appends every tool call to `~/.claude/tool-calls.log`

### Post-Tool-Use (Quality enforcement)
- `auto-format.sh` — auto-runs the right formatter after every file write (gofmt, prettier, black/ruff, rustfmt, ktlint, dart format)
- `run-linter.sh` — runs golangci-lint / eslint / ruff / clippy after file edits, feeds output back to Claude
- `notify-telegram.sh` — sends Telegram message when a tool completes (optional)

### Session-Start (Context Loading)
- `print-status.sh` — prints git branch, status, and last 3 commits when session opens
- `load-context.sh` — cats `continue.md` + `research/findings/latest.md` to stdout

---

## Why Hooks Beat CLAUDE.md Instructions

CLAUDE.md instructions are **suggestions** — Claude ignores them after 2-5 prompts (GitHub issues #668, #7777, #19635, #23032 — 14+ violations in a single session reported by users).

Hooks are **deterministic**. They execute outside Claude's control. Exit code 1 blocks the action. Claude cannot be "told" to bypass them.

**Rule of thumb:**
- Critical constraint (don't force-push, don't skip tests) → Hook
- Style preference (prefer X over Y) → CLAUDE.md
- Workflow preference (check tests before committing) → Slash command

---

## Installation

### Step 1: Copy hooks to your Claude config directory

```bash
mkdir -p ~/.claude/hooks/pre-tool-call
mkdir -p ~/.claude/hooks/post-tool-call
mkdir -p ~/.claude/hooks/session-start

cp pre-tool-call/*.sh ~/.claude/hooks/pre-tool-call/
cp post-tool-call/*.sh ~/.claude/hooks/post-tool-call/
cp session-start/*.sh ~/.claude/hooks/session-start/

chmod +x ~/.claude/hooks/**/*.sh
```

**Which hooks to enable first:**
1. `block-rm-rf.sh` + `block-force-push.sh` — always, no downsides
2. `enforce-commit-format.sh` — if you want consistent commit history
3. `auto-format.sh` — if your formatters are installed (check with `which gofmt prettier black rustfmt`)
4. `run-linter.sh` — optional; adds latency but catches issues immediately
5. `block-test-skip.sh` — if you want to prevent Claude from skipping tests

### Step 2: Register hooks in settings.json

Add to your `.claude/settings.json` (or `~/.claude/settings.json` for global):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/pre-tool-call/block-rm-rf.sh"
          },
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/pre-tool-call/block-force-push.sh"
          },
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/pre-tool-call/log-tool-calls.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/post-tool-call/notify-telegram.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/session-start/print-status.sh"
          },
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/session-start/load-context.sh"
          }
        ]
      }
    ]
  }
}
```

### Step 3: Configure optional hooks

For `notify-telegram.sh`, set these env vars (in `~/.bashrc` or `~/.zshrc`):
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

---

## Hook Behavior

- **Exit code 0 + no JSON output**: hook passed, Claude continues
- **Exit code 0 + JSON `permissionDecision: "deny"`**: action is blocked (correct block method)
- **Stdout**: shown to Claude as context
- **Stderr**: shown to the user as an error message

**Important:** In the current Claude Code API, exit code 1 is **non-blocking** (only shown in verbose mode). To block an action, output the deny JSON and exit 0:

```bash
printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"reason here"}}'
exit 0
```

---

## Minimal Install (just safety hooks)

If you only want the safety guards and nothing else:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/block-rm-rf.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/block-force-push.sh"}
        ]
      }
    ]
  }
}
```
