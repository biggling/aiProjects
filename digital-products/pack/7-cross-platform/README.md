# Cross-Platform AGENTS.md

## What This Is

AGENTS.md is the equivalent of CLAUDE.md for OpenCode, Cursor, and other AI coding tools that follow the AGENTS.md spec.

OpenCode has 120,000+ GitHub stars and 5M+ users/month (2026). Many developers use both Claude Code and OpenCode depending on task. These files let you enforce the same conventions across both tools.

---

## CLAUDE.md vs AGENTS.md

| | CLAUDE.md | AGENTS.md |
|---|---|---|
| Tool | Claude Code | OpenCode, Cursor, others |
| Location | Project root | Project root |
| Format | Free-form markdown | Structured markdown with specific headers |
| Auto-loaded | Yes (Claude Code) | Yes (OpenCode) |

AGENTS.md uses the same conventions as the CLAUDE.md files in folder 1, reformatted for the AGENTS.md spec.

---

## AGENTS.md Format

OpenCode reads these specific headers:

```markdown
# Agent Instructions

## allowed_tools
[list of tools the agent can use]

## context_files
[files to load into context at session start]

## conventions
[coding conventions — same as CLAUDE.md content]

## workflow
[how the agent should approach tasks]
```

---

## Installation

Copy the relevant `AGENTS.md` file to your project root:

```bash
# For a Go project
cp 7-cross-platform/go-microservices/AGENTS.md /your/project/AGENTS.md

# For a TypeScript project
cp 7-cross-platform/typescript-node/AGENTS.md /your/project/AGENTS.md
```

If you're using both Claude Code and OpenCode on the same project, have both files:
```
your-project/
├── CLAUDE.md     ← for Claude Code
├── AGENTS.md     ← for OpenCode / Cursor
└── ...
```

---

## Notes

- AGENTS.md content mirrors the CLAUDE.md files in folder 1
- Keep both files in sync when you update conventions
- OpenCode also reads `.cursorrules` — use AGENTS.md as it's the newer standard
