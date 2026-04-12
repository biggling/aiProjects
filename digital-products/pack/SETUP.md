# Setup Guide — Claude Code Elite Pack

Complete installation in 10 minutes for Starter/Pro, 20 minutes for Elite.

---

## Step 1: Pick Your Stack Config (2 min)

Copy the CLAUDE.md that matches your project's primary stack to your project root:

```bash
# Go microservices (REST/gRPC, pgx, chi, slog)
cp 1-stack-configs/go-microservices/CLAUDE.md /your/project/CLAUDE.md

# TypeScript / Node.js (Hono, Zod, Vitest, ESM)
cp 1-stack-configs/typescript-node/CLAUDE.md /your/project/CLAUDE.md

# Python data pipeline (Celery, SQLAlchemy 2.x, Alembic, loguru)
cp 1-stack-configs/python-data-pipeline/CLAUDE.md /your/project/CLAUDE.md

# Python FastAPI + React (async, React Query, WebSocket)
cp 1-stack-configs/python-fastapi-react/CLAUDE.md /your/project/CLAUDE.md

# Kotlin / Android (Jetpack Compose, MVVM, Hilt, Room)
cp 1-stack-configs/kotlin-android/CLAUDE.md /your/project/CLAUDE.md

# GDScript / Godot 4 (2D/3D game, signals, autoloads)
cp 1-stack-configs/gdscript-godot4/CLAUDE.md /your/project/CLAUDE.md

# Next.js / React (App Router, Server Components, Prisma, NextAuth)
cp 1-stack-configs/nextjs-react/CLAUDE.md /your/project/CLAUDE.md

# Rust (Tokio, Axum, SQLx, Anyhow, Clippy)
cp 1-stack-configs/rust/CLAUDE.md /your/project/CLAUDE.md

# Java / Spring Boot (Spring Data JPA, Spring Security, MapStruct, JUnit 5)
cp 1-stack-configs/java-spring-boot/CLAUDE.md /your/project/CLAUDE.md

# React Native / Expo (Expo Router, Riverpod, React Query, NativeWind)
cp 1-stack-configs/react-native/CLAUDE.md /your/project/CLAUDE.md

# Flutter / Dart (Riverpod 2, GoRouter, Freezed, Dio)
cp 1-stack-configs/flutter-dart/CLAUDE.md /your/project/CLAUDE.md

# Multi-project workspace (side projects, autonomous agents, cron)
cp 1-stack-configs/side-project-workspace/CLAUDE.md /your/workspace/CLAUDE.md
```

**Then customize it:** Add your project-specific conventions at the bottom.
Remove any sections that don't apply to your stack.

---

## Step 2: Set Up Multi-Agent Scripts (3 min)

```bash
# Copy scripts to your workspace
mkdir -p /your/workspace/scripts
cp 5-multi-agent-system/*.sh /your/workspace/scripts/
cp 5-multi-agent-system/crontab.conf /your/workspace/scripts/
chmod +x /your/workspace/scripts/*.sh

# Test it works
cd /your/workspace
./scripts/run-agent.sh your-project "read continue.md and list the next 3 tasks"
```

**Install the cron schedule:**
```bash
# Edit crontab.conf first — set WORKSPACE_ROOT to your actual path
nano /your/workspace/scripts/crontab.conf

# Install
crontab /your/workspace/scripts/crontab.conf

# Verify
crontab -l
```

**Create a continue.md** in each project (copy the template):
```bash
cp 5-multi-agent-system/continue.md.template /your/project/continue.md
# Edit it with your project's current state and next tasks
```

---

## Step 3: Set Up Memory OS (3 min) — Pro/Elite

```bash
# Run from your project root
cd /your/project
bash /path/to/pack/2-memory-os/setup-memory-os.sh
```

This creates `memory-bank/` with 4 files. Fill in `memory-bank/projectBrief.md` with:
- What the project does
- Your tech stack
- Non-negotiable rules

The other 3 files can start empty — Claude will populate them.

**Add to your CLAUDE.md:**
```markdown
## Memory OS
At session start: read ALL files in memory-bank/ before doing anything else.
At session end: update memory-bank/activeContext.md and memory-bank/progress.md.
Never truncate existing content — append only. Keep each file under 200 lines.
```

---

## Step 4: Install Auto Mode Profile (2 min) — Pro/Elite

```bash
# Standard profile (recommended for daily use)
mkdir -p /your/project/.claude
cp 3-auto-mode-profiles/standard/settings.json /your/project/.claude/settings.json
```

Or install globally (applies to all projects):
```bash
cp 3-auto-mode-profiles/standard/settings.json ~/.claude/settings.json
```

**Profile options:**
- `conservative/` — read-only, for exploration
- `standard/` — edits allowed, no git push (recommended)
- `trusted-dev/` — commits allowed, no force-push
- `ci-scripted/` — full access, for cron runs

---

## Step 5: Install Hooks (3 min) — Pro/Elite

```bash
# Create hook directories
mkdir -p ~/.claude/hooks/pre-tool-call
mkdir -p ~/.claude/hooks/post-tool-call
mkdir -p ~/.claude/hooks/session-start

# Copy hooks
cp 4-hooks/pre-tool-call/*.sh ~/.claude/hooks/pre-tool-call/
cp 4-hooks/post-tool-call/*.sh ~/.claude/hooks/post-tool-call/
cp 4-hooks/session-start/*.sh ~/.claude/hooks/session-start/
chmod +x ~/.claude/hooks/**/*.sh
```

**Register hooks in `~/.claude/settings.json`:**

If you already have a settings.json, merge the `hooks` block. If not, create it:

> **Minimum recommended (safety only):** `block-rm-rf`, `block-force-push`
> **Full enforcement:** add `enforce-commit-format`, `block-test-skip`, `auto-format`, `run-linter`

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/block-rm-rf.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/block-force-push.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/enforce-commit-format.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/block-test-skip.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/pre-tool-call/log-tool-calls.sh"}
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {"type": "command", "command": "bash ~/.claude/hooks/post-tool-call/auto-format.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/post-tool-call/run-linter.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/post-tool-call/notify-telegram.sh"}
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {"type": "command", "command": "bash ~/.claude/hooks/session-start/print-status.sh"},
          {"type": "command", "command": "bash ~/.claude/hooks/session-start/load-context.sh"}
        ]
      }
    ]
  }
}
```

**Optional — Telegram notifications:**
```bash
# Add to ~/.bashrc or ~/.zshrc
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

---

## Step 6: Install Slash Commands (2 min) — Elite

```bash
# Install globally (works in all projects)
mkdir -p ~/.claude/commands
cp 9-slash-commands/*.md ~/.claude/commands/

# Or per-project only
mkdir -p /your/project/.claude/commands
cp 9-slash-commands/*.md /your/project/.claude/commands/
```

Then in any Claude Code session:
```
/review              # structured pre-push code review
/commit              # generate conventional commit message
/security-scan       # OWASP scan on staged changes
/test-coverage       # find and write missing tests
/standup             # daily standup from git log
/refactor            # targeted refactor proposals
```

---

## Step 7: Context Optimization (5 min) — Elite

Copy relevant snippets from `6-1m-context-optimization/context-trim.md` to your CLAUDE.md.
Start with sections 1 (Response Conciseness) and 6 (Decision Autonomy) — biggest impact.

Read `6-1m-context-optimization/hidden-features.md` — surface features most devs discover after 6+ months:
`/compact`, `/memory`, git worktrees, headless mode, MCP token management.

---

## Step 8: Cross-Platform AGENTS.md — Elite

```bash
# Copy the AGENTS.md for your stack
cp 7-cross-platform/go-microservices/AGENTS.md /your/project/AGENTS.md
# Customize as needed — works with Cursor, OpenCode, Continue
```

---

## Step 9: Notion Dashboard — Elite

1. Open the link in `8-notion-dashboard/template-link.txt`
2. Click "Duplicate" (top-right)
3. Add your projects (see `8-notion-dashboard/README.md` for properties)

---

## Step 10: Test Your Config (5 min) — All tiers

This is the step most people skip — and then wonder why Claude still gets things wrong.

```bash
# Start a fresh Claude Code session in your project
cd /your/project
claude
```

Then run the 6 test prompts from `EFFECTIVENESS-TEST.md`. Score Claude's responses.
If tests fail → move those rules to hooks (or use the slash commands as explicit enforcement).

Target: 5/6 tests passing at session start.

---

## Verify Everything Works

```bash
# Hooks fire on session open (should print git status)
cd /your/project && claude

# Safety hook blocks rm -rf (should exit with BLOCKED message)
claude --print "run: rm -rf /tmp/test-dir"

# Commit format hook blocks bad messages
claude --print "run: git commit -m 'updated stuff'"

# Work agent (picks up from continue.md)
./scripts/run-agent-continue.sh your-project

# Research agent (reads research/AGENT.md)
./scripts/run-research.sh your-project
```

---

## Troubleshooting

**Hooks not firing?**
- Check `~/.claude/settings.json` is valid JSON: `python3 -m json.tool ~/.claude/settings.json`
- Check hook scripts are executable: `ls -la ~/.claude/hooks/**/*.sh`

**run-agent-continue.sh fails?**
- Check `claude` is in PATH: `which claude`
- Check Claude Code is installed: `claude --version`

**Memory OS not loading?**
- Confirm `memory-bank/` is in the project root (same dir as CLAUDE.md)
- Confirm the Memory OS block is in your CLAUDE.md

**Questions?** Reply to your purchase receipt — I respond within 24 hours.
