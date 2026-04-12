#!/usr/bin/env bash
# block-test-skip.sh — PreToolUse hook
# Blocks commands that skip or disable tests.
# Claude cannot use --skip-tests, -DskipTests, etc.
# Forces Claude to fix failing tests rather than skip them.
#
# Setup: register in ~/.claude/settings.json under PreToolUse → matcher: "Bash"

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

# Patterns that skip or disable tests
SKIP_PATTERNS=(
    "--skip-tests"
    "-DskipTests"
    "skipTests=true"
    "pytest.*-k.*skip"
    "go test.*-run.*Skip"
    "jest.*--testPathIgnorePatterns"
    "jest.*--passWithNoTests"
    "vitest.*--reporter=none"
)

for PATTERN in "${SKIP_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qiE "$PATTERN"; then
        printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Test-skipping flags are blocked (matched: %s). Fix the failing tests instead of skipping them. If a test is truly not applicable, remove it with a commit explaining why."}}' "$PATTERN"
        exit 0
    fi
done

exit 0
