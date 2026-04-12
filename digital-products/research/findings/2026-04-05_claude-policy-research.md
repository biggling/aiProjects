# Claude Code Policy Research — April 2026
> Researched 2026-04-05 | Source: code.claude.com/docs (official Anthropic docs, post-migration from docs.anthropic.com)

**Important:** As of early 2026, all Claude Code docs moved from `docs.anthropic.com/en/docs/claude-code/*` to `code.claude.com/docs/en/*` (301 redirect). Update any links in the pack.

---

## 1. settings.json — Valid Fields (April 2026)

### Schema

The official JSON schema is at `https://json.schemastore.org/claude-code-settings.json`. Add `"$schema"` to get VS Code/Cursor autocomplete.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json"
}
```

### File Locations (Scope Hierarchy)

| Priority | Scope | File |
|---|---|---|
| 1 (highest) | Managed | `/Library/Application Support/ClaudeCode/managed-settings.json` (macOS) |
| 2 | CLI args | `--permission-mode`, `--allowedTools`, etc. |
| 3 | Local | `.claude/settings.local.json` (gitignored) |
| 4 | Project | `.claude/settings.json` (committed) |
| 5 (lowest) | User | `~/.claude/settings.json` |

Deny at ANY level blocks the tool — no lower scope can override a deny.

### Complete Valid Fields (settings.json)

| Field | Type | Notes |
|---|---|---|
| `agent` | string | Run main thread as a named subagent |
| `allowedHttpHookUrls` | string[] | URL patterns HTTP hooks may target (`*` wildcard) |
| `allowedMcpServers` | object[] | Managed only: MCP allowlist |
| `allowManagedHooksOnly` | bool | Managed only: block user/project hooks |
| `allowManagedMcpServersOnly` | bool | Managed only |
| `allowManagedPermissionRulesOnly` | bool | Managed only: block user/project permission rules |
| `alwaysThinkingEnabled` | bool | Enable extended thinking by default |
| `apiKeyHelper` | string | Shell script path to generate API key |
| `attribution` | object | `{commit: "...", pr: "..."}` — replaces deprecated `includeCoAuthoredBy` |
| `autoMemoryDirectory` | string | Custom path for auto-memory (NOT in project settings.json) |
| `autoMode` | object | `{environment: [...], allow: [...], soft_deny: [...]}` — classifier config |
| `autoUpdatesChannel` | string | `"stable"` or `"latest"` (default) |
| `availableModels` | string[] | Restrict `/model` picker options |
| `awsAuthRefresh` | string | Script to refresh AWS credentials |
| `awsCredentialExport` | string | Script that outputs JSON with AWS creds |
| `blockedMarketplaces` | object[] | Managed only |
| `channelsEnabled` | bool | Managed only |
| `cleanupPeriodDays` | number | Session retention (default 30, min 1) |
| `companyAnnouncements` | string[] | Messages shown at startup |
| `defaultShell` | string | `"bash"` or `"powershell"` |
| `deniedMcpServers` | object[] | Managed only: MCP denylist |
| `disableAllHooks` | bool | Disable all hooks (managed hooks cannot be disabled) |
| `disableAutoMode` | string | `"disable"` to block auto mode |
| `disableDeepLinkRegistration` | string | `"disable"` |
| `disabledMcpjsonServers` | string[] | MCP servers from .mcp.json to reject |
| `disableSkillShellExecution` | bool | Disable inline shell in skills/commands |
| `effortLevel` | string | `"low"`, `"medium"`, `"high"` |
| `enableAllProjectMcpServers` | bool | Auto-approve all project .mcp.json servers |
| `enabledMcpjsonServers` | string[] | MCP servers from .mcp.json to approve |
| `env` | object | Environment variables for every session |
| `fastModePerSessionOptIn` | bool | Require `/fast` each session |
| `feedbackSurveyRate` | number | 0–1, feedback survey probability |
| `fileSuggestion` | object | Custom `@` file autocomplete command |
| `forceLoginMethod` | string | `"claudeai"` or `"console"` |
| `forceLoginOrgUUID` | string or string[] | Lock to org UUID(s) |
| `forceRemoteSettingsRefresh` | bool | Managed only: fail-closed startup (v2.1.92) |
| `hooks` | object | Hook configuration (see Section 2) |
| `httpHookAllowedEnvVars` | string[] | Env vars HTTP hooks may use |
| `includeCoAuthoredBy` | bool | **DEPRECATED** — use `attribution` instead |
| `includeGitInstructions` | bool | Include built-in git instructions (default true) |
| `language` | string | Claude's response language (e.g. `"japanese"`) |
| `model` | string | Override default model |
| `modelOverrides` | object | Map model IDs to provider-specific IDs (e.g. Bedrock ARNs) |
| `otelHeadersHelper` | string | Script for dynamic OpenTelemetry headers |
| `outputStyle` | string | Output style preset |
| `permissions` | object | See permission block below |
| `plansDirectory` | string | Where plan files are stored |
| `pluginTrustMessage` | string | Managed only: appended to plugin trust warning |
| `prefersReducedMotion` | bool | Reduce UI animations |
| `respectGitignore` | bool | `@` picker respects .gitignore (default true) |
| `showClearContextOnPlanAccept` | bool | Show "clear context" on plan accept (default false) |
| `showThinkingSummaries` | bool | Show thinking summaries (default false since v2.1.83) |
| `spinnerTipsEnabled` | bool | Show spinner tips (default true) |
| `spinnerTipsOverride` | object | `{tips: [...], excludeDefault: bool}` |
| `spinnerVerbs` | object | `{mode: "append"|"replace", verbs: [...]}` |
| `statusLine` | object | Custom status line command |
| `strictKnownMarketplaces` | object[] | Managed only: allowed marketplaces |
| `useAutoModeDuringPlan` | bool | Auto mode semantics in plan mode (default true) |
| `voiceEnabled` | bool | Push-to-talk voice dictation |
| `worktree.symlinkDirectories` | string[] | Dirs to symlink in worktrees |
| `worktree.sparsePaths` | string[] | Sparse checkout paths in worktrees |

### Permissions Sub-block

```json
{
  "permissions": {
    "allow": ["Bash(npm run *)", "Read(~/.zshrc)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Bash(curl *)", "Read(./.env)", "Read(./secrets/**)"],
    "additionalDirectories": ["../docs/"],
    "defaultMode": "acceptEdits",
    "disableBypassPermissionsMode": "disable",
    "skipDangerousModePermissionPrompt": true
  }
}
```

`defaultMode` valid values: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`

### Settings ONLY in ~/.claude.json (NOT settings.json)

These will cause schema validation errors if placed in settings.json:
- `autoConnectIde`
- `autoInstallIdeExtension`
- `editorMode`
- `showTurnDuration`
- `terminalProgressBarEnabled`
- `teammateMode`

### Deprecated Fields (remove from pack configs)

| Deprecated | Replacement |
|---|---|
| `includeCoAuthoredBy` | `attribution: {commit: "...", pr: "..."}` |
| `/output-style` command | Use `/config` instead |
| `/tag` command | Removed in v2.1.92 |
| `/vim` command | Toggle via `/config` → Editor mode |
| `TaskOutput` tool | Use `Read` on background task output file |
| `model` param on Agent tool | Use `SendMessage({to: agentId})` |
| `/fork` command | Renamed to `/branch` (`/fork` still works as alias) |
| Windows managed path `C:\ProgramData\ClaudeCode\managed-settings.json` | `C:\Program Files\ClaudeCode\managed-settings.json` |

---

## 2. Hooks API — Current Format (April 2026)

### Hook Handler Types (4 types)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/pre-bash.sh",
            "timeout": 30,
            "async": false,
            "if": "Bash(git *)"
          }
        ]
      }
    ]
  }
}
```

**Type options:**
- `"command"` — shell command, reads JSON from stdin
- `"http"` — POST JSON to URL, read JSON response
- `"prompt"` — single-turn LLM evaluation
- `"agent"` — subagent with tool access

### Common Fields (all types)

```json
{
  "type": "command|http|prompt|agent",
  "if": "Bash(git *)",          // NEW v2.1.83+: filter when hook fires (permission rule syntax)
  "timeout": 600,               // seconds
  "statusMessage": "...",       // custom spinner text
  "once": false                 // Skills only: run once per session
}
```

### stdin JSON Format — What Hooks Receive

All events include:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/dir",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "agent_id": "agent-abc",     // present in subagents (v2.1.69+)
  "agent_type": "Explore"      // present with --agent or in subagents (v2.1.69+)
}
```

Tool events (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest) also include:
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run tests",
    "timeout": 120000,
    "run_in_background": false
  },
  "tool_use_id": "toolu_01ABC..."
}
```

**Reading tool input in a hook script:**
```bash
#!/bin/bash
COMMAND=$(jq -r '.tool_input.command' < /dev/stdin)
```

### Hook Output Format

```json
{
  "continue": true,
  "stopReason": "...",
  "suppressOutput": false,
  "systemMessage": "...",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",    // allow|deny|ask|defer (NEW: "defer" added v2.1.89)
    "permissionDecisionReason": "...",
    "updatedInput": {},               // modify tool parameters
    "additionalContext": "...",
    "updatedMCPToolOutput": {}        // PostToolUse only
  }
}
```

**Exit codes (command hooks):**
- Exit 0: Success. JSON in stdout processed.
- Exit 2: Blocking error. stderr fed back to Claude/user.
- Other: Non-blocking. stderr shown in verbose mode only.

### BREAKING CHANGE: PreToolUse Permission Decision Format

Old format (still works but deprecated):
```json
{"decision": "block"}
{"decision": "approve"}
```

New format (required for new hooks):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask|defer"
  }
}
```

### SECURITY FIX (v2.1.82): Hook allow no longer bypasses deny rules

**Breaking behavior change:** Before v2.1.82, a hook returning `permissionDecision: "allow"` would bypass deny permission rules. As of v2.1.82, hooks returning `"allow"` do NOT bypass `deny` rules — deny rules are still evaluated. This may break hooks that were used to override deny rules.

### New Hook Events (added in 2026)

| Event | Version | Description |
|---|---|---|
| `SessionStart` | early | Session begins/resumes |
| `SessionEnd` | v2.1.79 | Session terminates or `/resume` switches |
| `UserPromptSubmit` | — | User submits prompt |
| `PreToolUse` | — | Before tool execution (can block) |
| `PermissionRequest` | — | Permission dialog appears |
| `PermissionDenied` | v2.1.81 | Auto mode denied tool; return `{retry: true}` |
| `PostToolUse` | — | After successful tool execution |
| `PostToolUseFailure` | — | After tool failure |
| `SubagentStart` | — | Subagent spawned |
| `SubagentStop` | — | Subagent finished |
| `TaskCreated` | v2.1.84 | Task creation initiated |
| `TaskCompleted` | — | Task marked complete |
| `Notification` | — | Notification sent |
| `ConfigChange` | v2.1.49 | Config file changed during session |
| `FileChanged` | v2.1.83 | Watched file changed (async) |
| `CwdChanged` | v2.1.83 | Working directory changed |
| `InstructionsLoaded` | v2.1.76 | CLAUDE.md or rules loaded |
| `PreCompact` | — | Before context compaction |
| `PostCompact` | v2.1.76 | After compaction |
| `WorktreeCreate` | v2.1.69 | Worktree being created |
| `WorktreeRemove` | — | Worktree being removed |
| `Stop` | — | Claude finishes responding (can block) |
| `StopFailure` | v2.1.80 | Turn ends with API error |
| `TeammateIdle` | — | Team teammate about to idle |
| `Elicitation` | v2.1.82 | MCP server requests user input |
| `ElicitationResult` | v2.1.82 | User responds to elicitation |

### Hook Output Size Change (v2.1.90)

Hook output over 50K characters is now saved to disk and referenced by file path + preview instead of being injected directly into context. Scripts producing large output should be aware of this.

### New `defer` Decision (v2.1.89)

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "defer"
  }
}
```
Headless sessions can pause at a tool call and resume with `-p --resume`. Useful for non-interactive approval workflows.

### HTTP Hook Type (new in v2.1.80)

```json
{
  "type": "http",
  "url": "http://localhost:8080/hooks/pre-tool-use",
  "timeout": 30,
  "headers": {"Authorization": "Bearer $MY_TOKEN"},
  "allowedEnvVars": ["MY_TOKEN"]
}
```
Returns 2xx with JSON body to block or deny. Non-2xx is non-blocking error.

### Conditional `if` field (v2.1.83)

```json
{
  "type": "command",
  "command": "script.sh",
  "if": "Bash(git *)"
}
```
Uses permission rule syntax to filter when hook fires. Fixed in v2.1.92 to properly handle compound commands and env-var prefixes.

### Environment Variables Available in Hook Scripts

- `CLAUDE_PROJECT_DIR` — project root
- `CLAUDE_PLUGIN_ROOT` — plugin installation dir
- `CLAUDE_PLUGIN_DATA` — plugin persistent data dir
- `CLAUDE_ENV_FILE` — for SessionStart/CwdChanged/FileChanged env var persistence
- `CLAUDE_CODE_REMOTE` — `"true"` in web environment

### Hook Locations

| Location | Scope |
|---|---|
| `~/.claude/settings.json` | All projects |
| `.claude/settings.json` | Single project (shared) |
| `.claude/settings.local.json` | Single project (personal) |
| Managed settings | Organization-wide |
| Plugin `hooks/hooks.json` | When plugin enabled |
| Skill/Agent frontmatter | While component active |

---

## 3. Permission System — Full Detail

### Rule Evaluation Order

**deny → ask → allow** — first match wins. Deny at managed level cannot be overridden anywhere.

### Rule Syntax

```
Tool                    # match all uses
Tool(*)                 # same as above
Bash(npm run *)         # glob pattern
Bash(git * main)        # wildcards anywhere
Read(./.env)            # specific file
Read(./secrets/**)      # recursive glob
WebFetch(domain:example.com)  # domain match
mcp__puppeteer          # MCP server (all tools)
mcp__puppeteer__puppeteer_navigate  # specific MCP tool
Agent(Explore)          # subagent type
```

### Path Prefixes for Read/Edit Rules

| Prefix | Meaning |
|---|---|
| `//path` | Absolute path from filesystem root |
| `~/path` | From home directory |
| `/path` | Relative to project root |
| `path` or `./path` | Relative to current directory |

**Warning:** `/Users/alice/file` is NOT absolute — it's project-relative. Use `//Users/alice/file` for absolute.

### Permission Modes

| Mode | Description |
|---|---|
| `default` | Prompts on first use of each tool |
| `acceptEdits` | Auto-accepts file edits (not writes to protected dirs) |
| `plan` | Read-only analysis only |
| `auto` | AI classifier approves/blocks (research preview) |
| `dontAsk` | Auto-denies unless pre-approved via /permissions |
| `bypassPermissions` | Skips prompts (except .git, .claude, .vscode, .idea, .husky) |

Protected dirs in bypassPermissions (still prompt): `.git`, `.claude`, `.vscode`, `.idea`, `.husky`
Exempt from bypassPermissions prompts: `.claude/commands`, `.claude/agents`, `.claude/skills`

### Known Bug: deny Rules Non-Functional in Some Versions

GitHub issues (#6699, #27040) report deny rules being ignored in certain versions. Workaround: use a PreToolUse hook to block sensitive operations until the core deny functionality is verified fixed in your version.

### Important Security Warning (v2.1.82)

`Read` and `Edit` deny rules apply to Claude's built-in file tools only — NOT to Bash subprocesses. `Read(./.env)` blocks the Read tool but NOT `cat .env` in Bash. For OS-level enforcement, enable sandboxing.

### Bash Pattern Limitations

Patterns that try to constrain arguments are fragile:
- `Bash(curl http://github.com/ *)` won't match `curl -X GET http://github.com/...`
- Shell variables, redirects, and extra spaces all evade prefix patterns

**Better approach:** deny `Bash(curl *)` + use `WebFetch(domain:github.com)` allow rule.

### New Managed-Only Settings

```json
{
  "allowManagedHooksOnly": true,
  "allowManagedMcpServersOnly": true,
  "allowManagedPermissionRulesOnly": true,
  "disableBypassPermissionsMode": "disable",
  "disableAutoMode": "disable",
  "forceRemoteSettingsRefresh": true
}
```

---

## 4. CLAUDE.md — Official Best Practices (Current)

### File Locations

| Scope | Location |
|---|---|
| Managed/org | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) |
| Project (shared) | `./CLAUDE.md` or `./.claude/CLAUDE.md` |
| User (personal, all projects) | `~/.claude/CLAUDE.md` |
| Local (personal, this project) | `./CLAUDE.local.md` (gitignore this) |

### Key Facts

- CLAUDE.md is loaded as a user message after the system prompt, not as part of the system prompt itself (affects compliance reliability)
- Target under 200 lines per file — beyond 200 lines reduces adherence
- Use `@path/to/file` import syntax to pull in external files (max 5 hops deep)
- HTML block comments `<!-- notes -->` are stripped before injection into Claude context (visible when you Read the file directly) — use for maintainer notes that don't cost tokens
- Auto memory (v2.1.59+): Claude saves learnings automatically to `~/.claude/projects/<project>/memory/MEMORY.md` (first 200 lines/25KB loaded per session)
- `/init` command generates a starter CLAUDE.md; set `CLAUDE_CODE_NEW_INIT=1` for interactive multi-phase flow
- `claudeMdExcludes` setting in settings.json to skip specific CLAUDE.md files by glob

### .claude/rules/ Directory (NEW — important for pack)

Path-scoped rules that only load when Claude works with matching files:

```
.claude/
└── rules/
    ├── testing.md          # always loaded
    └── api-design.md       # path-scoped with frontmatter
```

Path-scoped rule frontmatter:
```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/**/*.{ts,tsx}"
---

# API Rules
- All endpoints must include input validation
```

Rules without `paths` frontmatter load at session start like CLAUDE.md. Rules load in print mode (`-p`) as of v2.1.81.

### AGENTS.md Integration

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. If a repo uses both:
```markdown
<!-- CLAUDE.md -->
@AGENTS.md

## Claude Code Specific
Use plan mode for changes under src/billing/.
```

### Auto Memory

- Enable/disable: `autoMemoryEnabled` in settings or `/memory` command toggle
- Stored at: `~/.claude/projects/<project>/memory/MEMORY.md`
- Shared across worktrees of same repo
- NOT loaded in `--bare` mode (v2.1.69)
- Can set custom path: `autoMemoryDirectory` in user/local settings (NOT project settings.json)

---

## 5. CLI Flags — Current State (April 2026)

### Still Valid Flags

| Flag | Status | Notes |
|---|---|---|
| `--print` / `-p` | Valid | Print mode, exit after response |
| `--dangerously-skip-permissions` | Valid | Equivalent to `--permission-mode bypassPermissions` |
| `--bare` | Valid (added v2.1.81) | Skip hooks, LSP, plugins, MCP, auto-memory, CLAUDE.md for fast scripted calls |
| `--output-format` | Valid | `text`, `json`, `stream-json` |
| `--allowedTools` | Valid | Space-separated permission rules |
| `--disallowedTools` | Valid | Remove tools from model context entirely |
| `--model` | Valid | Model alias or full ID |
| `--resume` / `-r` | Valid | Resume by ID or name |
| `--continue` / `-c` | Valid | Most recent session |

### Important: `--bare` Flag Details

`--bare` skips: hooks, LSP, plugin sync, skills, auto-memory, CLAUDE.md
Requires `ANTHROPIC_API_KEY` env var.
Sets `CLAUDE_CODE_SIMPLE` environment variable.
Use for scripted `-p` calls where you want minimal overhead.

### New Flags in 2026

| Flag | Added | Description |
|---|---|---|
| `--allow-dangerously-skip-permissions` | — | Add bypassPermissions to Shift+Tab cycle without starting in it |
| `--permission-mode` | — | `default|acceptEdits|plan|auto|dontAsk|bypassPermissions` |
| `--enable-auto-mode` | — | Unlock auto mode in Shift+Tab cycle |
| `--worktree` / `-w` | — | Start in isolated git worktree |
| `--tmux` | — | Create tmux session for worktree |
| `--name` / `-n` | v2.1.76 | Set session display name |
| `--remote` | — | Create new web session |
| `--remote-control` / `--rc` | — | Enable Remote Control |
| `--teleport` | — | Resume web session in local terminal |
| `--fork-session` | — | New session ID when resuming |
| `--from-pr` | — | Resume sessions linked to GitHub PR |
| `--init` | — | Run initialization hooks + interactive mode |
| `--init-only` | — | Run initialization hooks then exit |
| `--tools` | — | Restrict which built-in tools Claude can use |
| `--effort` | — | `low|medium|high|max` (Opus 4.6 only) |
| `--agent` | — | Specify agent for current session |
| `--agents` | — | Define subagents dynamically via JSON |
| `--json-schema` | — | Validated JSON output matching schema |
| `--max-budget-usd` | — | Dollar limit for API calls (print mode) |
| `--max-turns` | — | Limit agentic turns (print mode) |
| `--append-system-prompt` | — | Append to default system prompt |
| `--append-system-prompt-file` | — | Append file contents to system prompt |
| `--system-prompt` | — | Replace entire system prompt |
| `--system-prompt-file` | — | Replace system prompt with file |
| `--add-dir` | — | Additional working directories |
| `--setting-sources` | — | `user,project,local` sources to load |
| `--settings` | — | Path to settings file or JSON string |
| `--channels` | — | MCP servers to listen for channel notifications |
| `--chrome` | — | Enable Chrome browser integration |
| `--teammate-mode` | — | `auto|in-process|tmux` |
| `--include-hook-events` | — | Include hook events in stream-json output |
| `--remote-control-session-name-prefix` | v2.1.92 | Prefix for auto-generated RC session names |

---

## 6. New Claude Code Features in 2026 (Pack Should Mention)

### Subagents (previously called "Sub-agents")

Defined in markdown files with YAML frontmatter at `.claude/agents/` (project) or `~/.claude/agents/` (user):

```markdown
---
description: Reviews code quality. Use proactively after code changes.
model: sonnet
tools:
  - Read
  - Grep
  - Glob
  - Bash
permissionMode: acceptEdits
memory: user
---
You are a senior code reviewer. Focus on quality, security, and best practices.
```

Supported frontmatter fields: `description`, `model`, `tools`, `disallowedTools`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, `color`

Built-in subagents: `Explore` (read-only, Haiku model), `Plan` (research), `general-purpose`

`isolation: worktree` — run subagent in isolated git worktree (v2.1.50)
`background: true` — always run as background task (v2.1.49)

### Auto Mode (AI Classifier)

Automatically approves tool calls based on AI safety classification. Requires Sonnet 4.6 or Opus 4.6. Team/Enterprise/API plans.

Configure trusted infrastructure:
```json
{
  "autoMode": {
    "environment": [
      "Source control: github.com/your-org",
      "Trusted domains: *.internal.company.com"
    ]
  }
}
```

CLI: `claude auto-mode defaults`, `claude auto-mode config`, `claude auto-mode critique`

### Worktrees (`--worktree` / `-w`)

```bash
claude -w feature-auth       # creates .claude/worktrees/feature-auth/
claude -w feature-auth --tmux  # with tmux pane
```

Settings:
```json
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"],
    "sparsePaths": ["packages/my-app", "shared/utils"]
  }
}
```

### Agent Teams

Multiple Claude instances working in parallel via `agent teams`. Different from subagents (which are within a single session). Use `--teammate-mode auto|in-process|tmux`.

### Plugins

Package and distribute Claude Code configuration. Install via:
```bash
claude plugin install code-review@claude-plugins-official
```

### MCP (Model Context Protocol)

Now under Linux Foundation Agentic AI Foundation (donated by Anthropic, December 2025). Configure in `.mcp.json` (project) or `~/.claude.json` (user).

### Channels (Research Preview)

MCP servers that push messages into sessions. Configure with `--channels` flag. Requires Claude.ai authentication.

### Remote Control

Control a local Claude Code session from claude.ai or the Claude iOS app:
```bash
claude --remote-control "My Project"
```

### Scheduled Tasks

- Cloud scheduled tasks (run on Anthropic infrastructure): `/schedule` command
- Desktop scheduled tasks (run locally)
- `/loop` repeats a prompt within a session

### Chrome Integration

```bash
claude --chrome  # Enable browser automation and web testing
```

### Skills (Custom Slash Commands)

Defined in `.claude/commands/` (project) or `~/.claude/commands/` (user). Loaded only when invoked. Frontmatter supports: `description`, `allowed-tools`, `disallowed-tools`, `model`, `if`, `once`

---

## 7. AGENTS.md Spec — Linux Foundation Status

**Status as of December 2025:** AGENTS.md donated to the Linux Foundation Agentic AI Foundation (AAIF) by OpenAI. Anthropic's MCP also donated to AAIF.

**Format:** Standard Markdown, no required fields, no YAML frontmatter, no special syntax.

**Claude Code and AGENTS.md:** Claude Code reads `CLAUDE.md`, NOT `AGENTS.md`. If a project has both, create a CLAUDE.md that imports AGENTS.md:
```markdown
@AGENTS.md

## Claude Code Specific Instructions
...
```

**Adoption:** 60,000+ open-source projects as of early 2026. Supported by Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules, VS Code, and others.

**For the pack:** Our `CLAUDE.md` templates are correct. We should note that AGENTS.md is an interoperability format for teams using multiple coding agents. Our product can include a section on creating an AGENTS.md alongside CLAUDE.md for teams using multiple agents.

---

## 8. Breaking Changes Checklist for Pack Configs

Any pack configs, templates, or hook scripts should be audited for:

### settings.json

- [ ] Replace `includeCoAuthoredBy: true/false` with `attribution: {commit: "...", pr: "..."}`
- [ ] Remove `model` parameter from Agent tool calls in any hook scripts
- [ ] Move `autoMemoryDirectory` out of `.claude/settings.json` — NOT valid there
- [ ] Move `autoMode` out of `.claude/settings.json` — NOT read from shared project settings
- [ ] Remove Windows managed settings from `C:\ProgramData\ClaudeCode\` — use `C:\Program Files\ClaudeCode\`
- [ ] `showThinkingSummaries` now defaults to `false` (was `true`) since v2.1.83

### Hooks

- [ ] Update old `{"decision": "block"}` / `{"decision": "approve"}` output format to new `hookSpecificOutput.permissionDecision: "allow"|"deny"|"ask"|"defer"`
- [ ] Do NOT assume hook `"allow"` output overrides deny rules — it doesn't since v2.1.82
- [ ] Handle hook output >50K chars differently — now saved to disk (v2.1.90)
- [ ] Add `agent_id` and `agent_type` fields to any stdin parsers if needed (v2.1.69+)

### Docs URL

- [ ] Update all links from `docs.anthropic.com/en/docs/claude-code/*` to `code.claude.com/docs/en/*`

### Commands

- [ ] `/tag` command removed (v2.1.92)
- [ ] `/vim` command removed — use `/config` to toggle vim mode
- [ ] `/output-style` deprecated — use `/config`
- [ ] `TaskOutput` tool deprecated — use `Read` on the output file path

---

## 9. Reference Hook Script — Current Best Practice

```bash
#!/bin/bash
# PreToolUse hook — blocks dangerous Bash commands
# Location: .claude/hooks/pre-bash.sh

set -euo pipefail

INPUT=$(cat /dev/stdin)
TOOL=$(echo "$INPUT" | jq -r '.tool_name')

if [ "$TOOL" != "Bash" ]; then
  exit 0  # Not a Bash call, allow
fi

COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Block rm -rf
if echo "$COMMAND" | grep -qE '^rm\s+-[rf]'; then
  echo '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Destructive rm -rf blocked by org policy"
    }
  }'
  exit 0
fi

# Block curl/wget to external domains
if echo "$COMMAND" | grep -qE '^\s*(curl|wget)\s'; then
  echo '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Use WebFetch tool instead of curl/wget"
    }
  }'
  exit 0
fi

exit 0  # Allow
```

Hook registration in `.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/pre-bash.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

---

## Sources

- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [Claude Code Hooks](https://code.claude.com/docs/en/hooks)
- [Claude Code Permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Claude Code Memory/CLAUDE.md](https://code.claude.com/docs/en/memory)
- [Claude Code Overview](https://code.claude.com/docs/en/overview)
- [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents)
- [AGENTS.md spec](https://agents.md/)
- [Linux Foundation Agentic AI Foundation announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [GitHub issue: deny permissions not enforced #6699](https://github.com/anthropics/claude-code/issues/6699)
- [GitHub issue: deny permissions ignored #27040](https://github.com/anthropics/claude-code/issues/27040)
- [eesel.ai: Claude Code settings.json guide 2026](https://www.eesel.ai/blog/settings-json-claude-code)
