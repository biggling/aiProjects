---
description: Propose up to 5 targeted refactors for a file — no behavior changes, ask before applying
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /refactor — Targeted Refactor Proposals

Propose concrete, targeted refactors for the specified file or the most recently edited file.
Do NOT change behavior. Do NOT refactor outside the scope asked.

## Step 1: Identify the target
If $ARGUMENTS is provided, use that file path.
Otherwise use the last file written or edited in this session.

Read the file completely before proposing anything.

## Step 2: Identify refactor opportunities

Look for these specific patterns (rank by impact, propose max 5):

### Extract function
- Function body over 40 lines
- Nested conditionals 3+ levels deep
- Same block of logic copied in 2+ places

### Simplify conditionals
- Nested if/else that can be early-return
- Boolean expressions that can be simplified
- Switch/match that can be a map/dictionary lookup

### Improve naming
- Variables named `data`, `result`, `temp`, `x`, `i` outside of loops
- Functions that do more than their name says
- Booleans not named as questions (`isLoaded` not `loaded`)

### Reduce coupling
- Functions that take 4+ parameters (introduce a struct/object)
- Direct access to another module's internals
- Logic that belongs in a different layer (e.g., DB query in a handler)

### Token/memory efficiency
- Large object loaded when only one field is needed
- Collection built then immediately filtered (combine into one pass)

## Step 3: Output format

For each proposal:

```
### Refactor: [short name]
**File:** path/to/file.go  **Lines:** 42-78
**Problem:** [1 sentence — what's wrong with current code]
**Proposal:** [1 sentence — what to do instead]

Before:
```code
[current code, max 15 lines]
```

After:
```code
[proposed code, max 15 lines]
```
```

Then ask: "Apply all? Apply #1 only? Skip?" before making any changes.

$ARGUMENTS
