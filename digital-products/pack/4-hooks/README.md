# Hooks Library

## What Are Hooks?

Claude Code hooks are shell scripts that run automatically at key moments in Claude's lifecycle.
They run on YOUR machine, not inside Claude — giving you hard enforcement that CLAUDE.md instructions alone can't provide.

## Hook Events

| Event | When it fires | Use for |
|---|---|---|
| `PreToolCall` | Before Claude executes any tool | Block dangerous commands, log actions |
| `PostToolCall` | After Claude executes a tool | Notifications, audit trail |
| `SessionStart` | When a Claude Code session opens | Load context, print status |
| `SessionStop` | When a session closes | Summarize, cleanup |

## Hooks Included

### Pre-Tool-Call (Safety)
- `block-rm-rf.sh` — exits 1 if command contains `rm -rf` outside `/tmp`
- `block-force-push.sh` — exits 1 if command is `git push --force` or `git push -f`
- `log-tool-calls.sh` — appends every tool call to `~/.claude/tool-calls.log`

### Post-Tool-Call (Notifications)
- `notify-telegram.sh` — sends Telegram message when a tool completes (optional)

### Session-Start (Context Loading)
- `print-status.sh` — prints git branch, status, and last 3 commits when session opens
- `load-context.sh` — cats `continue.md` + `research/findings/latest.md` to stdout

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

### Step 2: Register hooks in settings.json

Add to your `.claude/settings.json` (or `~/.claude/settings.json` for global):

```json
{
  "hooks": {
    "PreToolCall": [
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
    "PostToolCall": [
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

- **Exit code 0**: hook passed, Claude continues
- **Exit code 1**: hook blocked the action, Claude stops and reports the block
- **Stdout**: shown to Claude as context
- **Stderr**: shown to the user as an error message

Use exit code 1 to hard-block dangerous actions. Use stdout to pass context to Claude.

---

## Minimal Install (just safety hooks)

If you only want the safety guards and nothing else:

```json
{
  "hooks": {
    "PreToolCall": [
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
