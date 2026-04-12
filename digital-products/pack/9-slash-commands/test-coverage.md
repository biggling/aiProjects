---
description: Find untested functions in recently changed files and write the missing tests
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# /test-coverage — Find and Write Missing Tests

Find untested functions in recently changed files and write the missing tests.

## Step 1: Find recently changed source files
Run: `git diff --staged --name-only` for staged changes, or `git diff HEAD~1 --name-only` for the last commit.
Filter to source files only (exclude test files, markdown, json, yaml).

## Step 2: For each source file, identify untested functions

Scan the file for exported/public functions and methods. Then check the corresponding test file:
- Go: `*_test.go` in same directory
- TypeScript: `*.test.ts` or `__tests__/*.ts`  
- Python: `test_*.py` or `*_test.py`
- Java: `*Test.java` in `src/test/`
- Kotlin: `*Test.kt` in `src/test/`
- Rust: `#[cfg(test)] mod tests` in same file

List functions that have no test coverage.

## Step 3: Write the missing tests

For each untested function, write a test that covers:
1. The happy path (normal input, expected output)
2. One edge case (empty, nil, zero, max value)
3. One error case (if the function can fail)

Follow the test conventions from CLAUDE.md for this project's stack.

## Step 4: Output a summary

```
## Test Coverage Report

### Files checked
- [file name]: X/Y functions covered

### Tests written
- [function name]: [test file]::[test name]
  [brief description of what's tested]

### Skipped (complex/integration — mark as TODO)
- [function name]: requires external service / DB / filesystem
```

$ARGUMENTS
