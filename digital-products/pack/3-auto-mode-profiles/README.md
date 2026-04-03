# Auto Mode Safety Profiles

## What This Is

Auto Mode lets Claude Code run without asking for confirmation on every action.
That's powerful — and risky if misconfigured.

These four `settings.json` profiles give Claude the right level of autonomy for the right situation.
Drop the file into your project's `.claude/settings.json` before running Auto Mode.

---

## The Four Profiles

### `conservative/` — Exploration & Read-Only
Use when: you want Claude to explore, answer questions, audit code.
Allows: Read, Glob, Grep, WebSearch, WebFetch.
Blocks: all writes, all bash commands.

### `standard/` — Normal Development
Use when: you trust Claude to edit files but not push code.
Allows: Read, Write, Edit, Glob, Grep, safe bash (npm install, pip install, pytest, go test).
Blocks: git push, rm, curl to external URLs, any deploy commands.

### `trusted-dev/` — Full Local Dev
Use when: you're pairing with Claude on a feature and want it to commit.
Allows: everything in standard + git add, git commit, git checkout, npm run build.
Blocks: git push --force, rm -rf, any production deploy commands.

### `ci-scripted/` — Cron / CI Automation
Use when: running Claude headless on a schedule (`--bare --print`).
Allows: full tool access.
Blocks: interactive prompts (Claude must never wait for input in CI).

---

## How to Install

**Option 1: Project-level (recommended)**
```bash
# From your project root
mkdir -p .claude
cp path/to/3-auto-mode-profiles/standard/settings.json .claude/settings.json
```

**Option 2: Global default**
```bash
cp path/to/3-auto-mode-profiles/standard/settings.json ~/.claude/settings.json
```

**Option 3: Per-session override**
```bash
CLAUDE_SETTINGS=path/to/settings.json claude --print "..."
```

---

## Switching Profiles

```bash
# Before an exploration session
cp .claude/profiles/conservative.json .claude/settings.json

# Before a coding session
cp .claude/profiles/standard.json .claude/settings.json

# Before letting Claude commit
cp .claude/profiles/trusted-dev.json .claude/settings.json

# Restore to standard after
cp .claude/profiles/standard.json .claude/settings.json
```

Tip: Add a shell alias: `alias claude-safe='cp ~/.claude/profiles/standard.json .claude/settings.json'`
