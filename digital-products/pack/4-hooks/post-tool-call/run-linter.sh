#!/usr/bin/env bash
# run-linter.sh — PostToolUse hook
# Runs a fast lint check after Claude edits a source file.
# Prints warnings to Claude's context so it can fix them immediately.
# Only runs on source files (not markdown, json, shell scripts, etc.)
#
# Requires linters to be installed (skips silently if not found):
#   Go:         golangci-lint
#   TypeScript: eslint
#   Python:     ruff check
#   Rust:       cargo clippy (project-level, only if Cargo.toml nearby)
#
# Setup: register in ~/.claude/settings.json under PostToolUse

set -uo pipefail

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

EXT="${FILE_PATH##*.}"
DIR="$(dirname "$FILE_PATH")"
ISSUES=""

case "$EXT" in
    go)
        if command -v golangci-lint &>/dev/null; then
            ISSUES=$(golangci-lint run "$FILE_PATH" 2>&1 | head -20) || true
        fi
        ;;
    ts|tsx)
        if command -v eslint &>/dev/null; then
            ISSUES=$(eslint "$FILE_PATH" --max-warnings 0 2>&1 | head -20) || true
        fi
        ;;
    py)
        if command -v ruff &>/dev/null; then
            ISSUES=$(ruff check "$FILE_PATH" 2>&1 | head -20) || true
        fi
        ;;
    rs)
        # Only run clippy if we're inside a Rust project
        if [ -f "$DIR/Cargo.toml" ] || [ -f "$DIR/../Cargo.toml" ]; then
            if command -v cargo &>/dev/null; then
                ISSUES=$(cargo clippy --quiet 2>&1 | grep -E "^warning|^error" | head -10) || true
            fi
        fi
        ;;
esac

if [ -n "$ISSUES" ]; then
    echo "[linter] Issues found in $FILE_PATH:"
    echo "$ISSUES"
    echo ""
    echo "[linter] Fix these before proceeding."
fi

exit 0
