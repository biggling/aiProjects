---
description: Generate and apply a Conventional Commit message for staged changes
allowed-tools: Bash, Read
---

# /commit — Smart Conventional Commit

Generate a conventional commit message for staged changes and apply it.

## Step 1: Inspect staged changes
Run `git diff --staged --stat` to see which files changed.
Run `git diff --staged` to read the actual changes.

## Step 2: Determine the commit type

| Type | When to use |
|---|---|
| `feat` | New feature or behavior added |
| `fix` | Bug fixed |
| `refactor` | Code restructured — no behavior change |
| `test` | Tests added or updated |
| `docs` | Documentation only |
| `chore` | Dependency updates, build changes, config |
| `perf` | Performance improvement |
| `style` | Formatting, whitespace — no logic change |
| `ci` | CI/CD pipeline changes |

Use `!` suffix for breaking changes: `feat!: remove deprecated API`

## Step 3: Determine the scope (optional)

The scope is the area of the codebase changed. Examples: `auth`, `api`, `db`, `ui`, `payments`.
Omit if the change spans too many areas.

## Step 4: Write the description

- Present tense, imperative mood: "add" not "added" or "adds"
- No capital letter at start
- No period at end
- Under 72 characters total (including type and scope)
- Describes WHAT changed and WHY, not HOW

## Step 5: Write the body (optional, for complex changes)

Add a blank line after the subject, then explain:
- What was the problem?
- Why this approach?
- Any side effects or caveats?

## Step 6: Apply the commit

Run `git commit -m "$(cat <<'EOF'
[your generated message here]
EOF
)"` 

Show me the message before committing and ask for confirmation if the change is large (>5 files or >100 lines).

$ARGUMENTS
