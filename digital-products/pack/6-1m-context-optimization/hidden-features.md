# Hidden Features Guide

Features that most developers only discover after 6+ months — or after taking Anthropic's paid course.
This guide surfaces them all on day one.

---

## Built-In Slash Commands

Claude Code ships with powerful built-in commands most users never use:

### /compact
**What it does:** Summarizes the entire conversation into a compressed context, then continues.
**When to use:** Every 20-30 turns in a long session. When you notice Claude "forgetting" earlier context.
**Why it matters:** After auto-compaction (which happens silently), Claude loses nuance from early in the session. `/compact` gives you a controlled reset.

```
/compact
/compact focus on the authentication changes we made
```

### /memory
**What it does:** Opens the user-level memory file where Claude stores facts about you.
**When to use:** After setting up Memory OS — verify Claude is loading your project memory correctly.

```
/memory
```

### /review
**What it does:** Built-in code review. Reviews staged changes for issues.
**Note:** The `/review` command in `9-slash-commands/review.md` is more structured — use that instead.

### /init
**What it does:** Generates a CLAUDE.md for your project by reading the codebase.
**Warning:** The auto-generated CLAUDE.md is generic. Use it as a starting point, then replace with the right config from `1-stack-configs/`.

### /cost
**What it does:** Shows token usage and estimated cost for the current session.
**When to use:** Before a long autonomous task, to baseline your token burn rate.

---

## Git Worktrees — Run Claude in Parallel

The most underused feature. Worktrees let you run multiple Claude sessions on the same repo simultaneously — each in an isolated branch.

```bash
# Create a worktree for a feature branch
git worktree add ../my-project-feature feature/auth-refactor

# Open Claude in the worktree
cd ../my-project-feature
claude

# Meanwhile, keep coding in the main directory
cd ../my-project
# Claude in here is on main, Claude in worktree is on feature/auth-refactor
# They don't interfere with each other
```

**Use case:** Run a cron agent in a worktree overnight. It works on a feature branch without touching your working tree. In the morning: `git merge feature/auth-refactor`.

```bash
# In crontab: run agent in an isolated worktree
0 20 * * * cd /workspace && \
  git worktree add /tmp/agent-run-$(date +%Y%m%d) agent/$(date +%Y%m%d) && \
  claude --print "$(cat continue.md)" --cwd /tmp/agent-run-$(date +%Y%m%d)
```

---

## GitHub Integration

Claude Code can read GitHub issues, PRs, and comments directly.

```bash
# Reference an issue in your prompt
claude "Fix the bug described in #142"

# Claude will fetch the issue content and use it as context
# Works with: issues, PRs, commit SHAs, file URLs
```

**Setup:** Run `gh auth login` once. Claude uses your GitHub CLI auth automatically.

**Use case:** Your research agent can open issues automatically:
```bash
claude --print "Read research/findings/latest.md. 
For each opportunity found, create a GitHub issue with the research as context."
```

---

## Checkpoints / Session Snapshots

Claude Code can snapshot the session state so you can resume or branch:

```bash
# Create a checkpoint
/checkpoint save before-refactor

# Restore to a checkpoint
/checkpoint restore before-refactor
```

**Use case:** Before a risky refactor in Auto Mode, save a checkpoint. If it goes wrong, restore rather than git reset.

---

## Running Claude Headless (--print mode)

The foundation of the multi-agent system (folder 5), but useful to know directly:

```bash
# Run a one-shot task, print output, exit
claude --print "What does src/auth/jwt.go do?"

# Use in scripts
RESULT=$(claude --print "List all API endpoints in src/routes/")
echo "$RESULT" >> docs/api-inventory.md

# Pipe context
cat continue.md | claude --print "Based on this context, what's the next task?"

# With --bare (skip hooks, LSP, skill walks — saves ~5k tokens per session)
claude --bare --print "fix the failing test in tests/auth_test.go"
```

---

## MCP Token Management

MCP servers consume 30-40K tokens before your first prompt — most of it unused tool definitions.

```bash
# See how many tokens your current MCP setup burns
claude --print "/cost" --no-mcp

# Compare: same prompt with and without MCP
claude --print "hello" 2>&1 | grep -i token
claude --no-mcp --print "hello" 2>&1 | grep -i token
```

**Fix:** Only load MCP servers you need for the current session. In `.claude/settings.json`:

```json
{
  "mcpServers": {
    "github": { ... },
    "postgres": { ... }
  },
  "disabledMcpServers": ["postgres"]  // disable when not doing DB work
}
```

---

## The `--dangerously-skip-permissions` Flag

Allows Claude to run without any permission prompts — for fully autonomous CI/cron runs.

**ONLY use with the `ci-scripted` Auto Mode profile** from `3-auto-mode-profiles/`. That profile has explicit allow/deny lists that constrain what Claude can actually do. Without it, `--dangerously-skip-permissions` is genuinely dangerous.

```bash
# Safe: ci-scripted profile constrains actions even without prompts
CLAUDE_SETTINGS=/workspace/.claude/ci-scripted.json \
  claude --print --dangerously-skip-permissions "$(cat continue.md)"
```

---

## Token Budget Statusline

See your rate-limit usage in real time in the terminal statusline.
Full setup in `6-1m-context-optimization/token-budget-statusline.md`.

Quick version: set `CLAUDE_CODE_USE_BEDROCK=0` and add `%tokenUsage` to your statusline config (Claude Code v2.1.86+).

---

## Session Context Commands

```bash
/context               # show current token usage and context size
/context files         # list files currently in context
/clear                 # clear context and start fresh (keeps CLAUDE.md loaded)
```

Use `/context` before a big task to know if you have enough runway.
Use `/clear` when you've finished a task and want to start a clean context for the next one.

---

## New in 2026 — Features Most Devs Haven't Found Yet

### Subagents (`.claude/agents/`)
Claude Code can now spawn sub-agents with different personas, tools, and instructions:

```markdown
<!-- .claude/agents/researcher.md -->
---
name: researcher
description: Web research and competitive analysis agent
tools: WebSearch, WebFetch, Read, Write
---

You are a research specialist. Always cite sources.
Summarize findings in findings/YYYY-MM-DD_topic.md.
```

Invoke with: `claude "use the researcher agent to find competitors for our pricing page"`

### Path-Scoped Rules (`.claude/rules/`)
Rules that only load when Claude works on matching files — avoids bloating context:

```
.claude/rules/
  *.test.ts.md      # test-file-specific rules
  migrations/*.md   # migration safety rules
  api/routes/*.md   # API design rules
```

### Auto Mode AI Classifier
Claude Code now has a built-in classifier that automatically decides whether to prompt or proceed. You can steer it:

```json
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "acceptEdits",   // auto-accept edits, prompt for commands
    "autoModeThreshold": "cautious" // "permissive" | "cautious" | "paranoid"
  }
}
```

### Worktree Flag (`--worktree` / `-w`)
Create an isolated worktree session in one command:

```bash
claude -w feature/auth-refactor    # creates worktree + opens Claude on that branch
claude --worktree main             # opens isolated session on main without leaving your branch
```

### Built-in `/schedule`
Schedule a one-shot task to run at a specific time — no cron needed:

```
/schedule "in 30 minutes, run the test suite and report results"
/schedule "at 9am, read continue.md and start the next task"
```

### Remote Control (`--remote-control`)
Control a running Claude Code session from another terminal or script:

```bash
# Terminal 1: running Claude session
claude --remote-control

# Terminal 2: send commands to it
claude remote send "run the tests now"
claude remote send "stop and summarize what you did"
```

### AGENTS.md — Cross-Tool Standard
The Linux Foundation AI & Automation Interoperability Forum (AAIF) now maintains `AGENTS.md` as a cross-tool standard. Claude Code reads `CLAUDE.md` natively; to support Cursor, OpenCode, and Continue from the same file, add to your `CLAUDE.md`:

```markdown
@AGENTS.md
```

This imports your `AGENTS.md` into Claude's context while keeping the canonical source in `AGENTS.md` for other tools. See `7-cross-platform/` for stack-specific templates.
