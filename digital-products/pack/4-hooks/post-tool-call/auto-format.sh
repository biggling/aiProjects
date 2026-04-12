#!/usr/bin/env bash
# auto-format.sh — PostToolUse hook
# Automatically formats files after Claude writes or edits them.
# Detects the file type and runs the appropriate formatter.
# Claude cannot forget to format — it happens automatically.
#
# Requires formatters to be installed (skips silently if not found):
#   Go:         gofmt (built-in)
#   TypeScript: prettier
#   Python:     ruff or black
#   Rust:       rustfmt
#   Kotlin:     ktlint
#   Dart:       dart format
#   Java:       google-java-format (optional)
#
# Setup: register in ~/.claude/settings.json under PostToolUse

set -uo pipefail

INPUT=$(cat)

# tool_input contains the parameters passed to Write/Edit tools
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null)

# No file path = not a file write operation
if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

EXT="${FILE_PATH##*.}"

case "$EXT" in
    go)
        if command -v gofmt &>/dev/null; then
            gofmt -w "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] gofmt applied to $FILE_PATH" || true
        fi
        ;;
    ts|tsx|js|jsx|json)
        if command -v prettier &>/dev/null; then
            prettier --write "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] prettier applied to $FILE_PATH" || true
        fi
        ;;
    py)
        if command -v ruff &>/dev/null; then
            ruff format "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] ruff applied to $FILE_PATH" || true
        elif command -v black &>/dev/null; then
            black "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] black applied to $FILE_PATH" || true
        fi
        ;;
    rs)
        if command -v rustfmt &>/dev/null; then
            rustfmt "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] rustfmt applied to $FILE_PATH" || true
        fi
        ;;
    kt|kts)
        if command -v ktlint &>/dev/null; then
            ktlint --format "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] ktlint applied to $FILE_PATH" || true
        fi
        ;;
    dart)
        if command -v dart &>/dev/null; then
            dart format "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] dart format applied to $FILE_PATH" || true
        fi
        ;;
    java)
        if command -v google-java-format &>/dev/null; then
            google-java-format --replace "$FILE_PATH" 2>/dev/null && \
                echo "[auto-format] google-java-format applied to $FILE_PATH" || true
        fi
        ;;
esac

exit 0
