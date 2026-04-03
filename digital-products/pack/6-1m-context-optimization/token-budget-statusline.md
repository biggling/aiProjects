# Token Budget Statusline

## What This Is

Claude Code v2.1.86+ exposes your rate-limit token usage as a statusline field.
Displaying it in your terminal gives you a real-time feedback loop — you can see when a session is burning context unusually fast and course-correct.

---

## Setup

### Step 1: Add to your Claude Code statusline config

In `~/.claude/settings.json`, add a statusline configuration:

```json
{
  "statusline": {
    "fields": ["model", "token_usage", "cost"]
  }
}
```

The `token_usage` field shows your current session's token consumption against the rate limit.

### Step 2: Or use the API header (for monitoring scripts)

Claude Code v2.1.86+ adds `X-Claude-Code-Session-Id` to all API requests.
You can aggregate token usage per session by filtering on this header in a proxy.

---

## Reading the Statusline

| Display | Meaning |
|---|---|
| `tokens: 12k / 200k` | 12,000 tokens used of 200k session budget |
| `tokens: 180k / 200k` | Context nearly full — start a new session or summarize |
| `rate: 85%` | 85% of your rate limit used this hour |

---

## Warning Thresholds

Add this to your session-start hook to warn when context is high:

```bash
# In session-start/print-status.sh
# (Add after git status block)

# Warn if previous session log shows high token usage
LAST_LOG=$(ls ~/.claude/logs/*.log 2>/dev/null | sort | tail -1)
if [ -f "$LAST_LOG" ]; then
  TOKENS=$(grep -o 'tokens_used=[0-9]*' "$LAST_LOG" | tail -1 | cut -d= -f2)
  if [ -n "$TOKENS" ] && [ "$TOKENS" -gt 150000 ]; then
    echo "⚠️  Last session used ${TOKENS} tokens — consider starting fresh context"
  fi
fi
```

---

## Token Budget Mental Model

| Token range | What to do |
|---|---|
| 0–50k | Normal session, no concerns |
| 50k–150k | Normal for complex feature work |
| 150k–800k | High — check if Claude is re-reading files |
| 800k+ | Context bloat — start new session, use Memory OS |

The most common cause of high token usage: Claude reading the same large file multiple times in one session. The `context-trim.md` instructions prevent this.

---

## Quick Debug: What's Eating Your Tokens?

Ask Claude mid-session:
> "How many times have you read each file this session? List any file read more than once."

If Claude has read a file 3–4 times, add it to Memory OS so it's loaded once at session start and never re-read.
