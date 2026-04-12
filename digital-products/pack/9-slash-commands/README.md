# Slash Commands Library

Custom `/commands` for Claude Code. Each command is a `.md` file in `.claude/commands/`.
Type `/command-name` in any session to run it.

## What's Included

| Command | File | What it does |
|---|---|---|
| `/review` | `review.md` | Structured diff review before you push — catches bugs, style issues, security problems |
| `/commit` | `commit.md` | Smart conventional commit with auto-generated message from staged changes |
| `/standup` | `standup.md` | Daily standup from git log — what you did, what's next, any blockers |
| `/explain` | `explain.md` | Explains a function/file in plain English with examples |
| `/test-coverage` | `test-coverage.md` | Lists untested functions in changed files and writes missing tests |
| `/security-scan` | `security-scan.md` | Scans changed files for OWASP Top 10 vulnerabilities |
| `/refactor` | `refactor.md` | Proposes targeted refactors for the current file without changing behavior |

---

## Install (2 minutes)

```bash
# Create commands directory in your project
mkdir -p .claude/commands

# Copy all commands
cp 9-slash-commands/*.md .claude/commands/

# Or copy individual commands
cp 9-slash-commands/review.md .claude/commands/
cp 9-slash-commands/commit.md .claude/commands/
```

Alternatively, install globally (works in all projects):
```bash
mkdir -p ~/.claude/commands
cp 9-slash-commands/*.md ~/.claude/commands/
```

---

## Usage

```
/review                    # review all staged changes
/review src/handlers/      # review a specific directory
/commit                    # generate and apply a commit message
/standup                   # what did I do today?
/explain src/auth/jwt.go   # explain a specific file
/test-coverage             # what's not tested?
/security-scan             # any security issues in my changes?
/refactor src/service.ts   # how would you clean this up?
```

---

## Why Slash Commands vs CLAUDE.md Instructions?

CLAUDE.md instructions get **ignored** — it's the #1 filed GitHub issue (4 separate bugs).
Instructions like "always review your code before committing" degrade after 2-5 prompts.

Slash commands are **explicit actions you invoke**. They can't be ignored because you're
explicitly calling them. Use CLAUDE.md for ambient context; use slash commands for
structured workflows you want to run deliberately.
