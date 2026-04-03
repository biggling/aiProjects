#!/usr/bin/env bash
# session-start/load-context.sh
# Loads continue.md and latest research findings into Claude's context at turn 0.
# Saves tokens vs. Claude reading them manually — content is already in context.
# Claude Code hook — SessionStart

MAX_CHARS=4000

print_file_capped() {
  local file="$1"
  local label="$2"
  if [ -f "$file" ]; then
    echo ""
    echo "--- $label ---"
    head -c "$MAX_CHARS" "$file"
    local size
    size=$(wc -c < "$file")
    if [ "$size" -gt "$MAX_CHARS" ]; then
      echo ""
      echo "[... truncated at ${MAX_CHARS} chars. Full file at: $file]"
    fi
    echo ""
  fi
}

print_file_capped "continue.md" "continue.md"
print_file_capped "research/findings/latest.md" "research/findings/latest.md"

exit 0
