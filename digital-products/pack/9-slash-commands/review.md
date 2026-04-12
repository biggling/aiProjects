---
description: Structured pre-push code review covering correctness, security, performance, style, and tests
allowed-tools: Bash, Read, Glob, Grep
---

# /review — Pre-Push Code Review

You are doing a structured code review of my staged changes before I push.

## Step 1: Get the diff
Run `git diff --staged` to see all staged changes. If nothing is staged, run `git diff HEAD~1` to review the last commit.

## Step 2: Review each changed file against these criteria

### Correctness
- Logic errors, off-by-one errors, null/nil dereferences
- Race conditions or concurrency issues
- Missing error handling — errors silently swallowed
- Edge cases not handled (empty input, nil, zero, max values)

### Security (OWASP Top 10)
- SQL injection: string-formatted queries instead of parameterized
- Injection in shell commands: user input in Bash/exec calls
- Hardcoded secrets, tokens, or credentials
- Missing authentication or authorization checks
- Unsafe deserialization or file operations

### Performance
- N+1 query patterns in database calls
- Synchronous I/O blocking an async thread or event loop
- Unnecessary allocations in hot paths
- Missing indexes implied by the query patterns

### Style & Conventions
- Does the code follow the conventions in CLAUDE.md?
- Naming inconsistencies
- Functions that are too long (>50 lines) or doing too much
- Missing or wrong return types / type annotations

### Tests
- Are tests included for new behavior?
- Do existing tests still cover the changed code?
- Any test that was silently removed or skipped?

## Step 3: Output format

Use this exact structure:

```
## Code Review

### Summary
[1-2 sentences on what the change does]

### 🔴 Must Fix (blocks push)
- file.go:42 — [description of critical issue]

### 🟡 Should Fix (fix before merge)
- file.go:15 — [description of issue]

### 🟢 Suggestions (optional improvements)
- [suggestion]

### ✅ Looks Good
- [things done well]

### Verdict
APPROVED / NEEDS CHANGES
```

If there are no issues in a category, omit that section. Be specific — cite file name and line number for every issue.

$ARGUMENTS
