# CLAUDE.md Token Efficiency — Concept & Examples
> 2026-04-05 | How to write CLAUDE.md for specific tasks without burning tokens

---

## Why It Costs Tokens

Every line of CLAUDE.md is injected into context **on every single request** in a session. If your CLAUDE.md is 500 lines (~5,000 tokens) and you make 40 tool calls in a session, that's **200,000 tokens** just from the config file — before any code is read.

The goal: maximum signal, minimum tokens.

---

## Core Principles

### 1. Goal + Constraint — not Step-by-Step

Claude already knows how to code. Don't describe the procedure. Describe the outcome and the guardrail.

**WASTEFUL (37 tokens):**
```markdown
When writing error handling, please make sure you always wrap errors
with context so that stack traces are meaningful and debugging is easier.
```

**LEAN (11 tokens):**
```markdown
Errors: wrap with context. `fmt.Errorf("parseUser: %w", err)`
```

---

### 2. Specifics Beat Adjectives

"Write clean code" = 0 information. Claude already tries to do that.
"No naked returns in functions >3 lines" = actionable constraint Claude can actually follow.

**WASTEFUL:**
```markdown
Always write high quality, clean, maintainable, well-structured code
following industry best practices and proper design patterns.
```

**LEAN:**
```markdown
No naked returns. No init(). No global state. Errors named: parseErr, dbErr (not reusing `err`).
```

---

### 3. One Line Per Rule — Lists, Not Prose

Prose forces Claude to parse sentences. Lists are parsed in one pass.

**WASTEFUL:**
```markdown
When working with the database, you should always use the repository
pattern and never call the database directly from handlers. Make sure
to use transactions when doing multiple writes.
```

**LEAN:**
```markdown
DB rules:
- Repo pattern only — no direct DB calls from handlers
- Multi-write = transaction required
```

---

### 4. Gotchas Section — Highest ROI Per Token

A "Gotcha" is a project-specific fact Claude cannot infer from the code alone.
These are worth 10x their token cost because they prevent 30-minute debugging spirals.

```markdown
## Gotchas
- `UserID` is a string (UUID), not int — never cast to int
- `config.Load()` panics if called before `os.Setenv("ENV", ...)` in tests
- The `/health` route must NOT require auth — load balancer calls it unauthenticated
- `ctx.Done()` is nil in background jobs — always set a timeout explicitly
```

---

### 5. Modular Loading — Keep Base CLAUDE.md Tiny

The base CLAUDE.md should be <100 lines. Put deep docs in skill files loaded on-demand.

```
project/
├── CLAUDE.md           ← Always loaded (~80 lines max)
└── .claude/
    └── commands/
        ├── deploy.md   ← Only loaded when you run /deploy
        ├── migrate.md  ← Only loaded when you run /migrate
        └── review.md   ← Only loaded when you run /review
```

**The base CLAUDE.md just points to commands:**
```markdown
## Commands
- `/deploy` — see .claude/commands/deploy.md
- `/migrate` — see .claude/commands/migrate.md
```

Those files never load unless called. You get full detail at zero base cost.

---

### 6. Skip What Claude Can Already See

Don't put things in CLAUDE.md that Claude can discover by reading your code.

**Wastes tokens:**
```markdown
This is a Go project using the Gin framework with PostgreSQL.
The main entry point is cmd/server/main.go. We use GORM for ORM.
The project structure follows hexagonal architecture with domain,
repository, and handler layers.
```

Claude sees `go.mod`, `import "github.com/gin-gonic/gin"`, `import "gorm.io/gorm"` in 2 seconds.
**Only write what Claude CANNOT discover from reading files.**

---

## Full Example — Go Microservice CLAUDE.md (73 lines, ~650 tokens)

```markdown
# Project: payments-service

## Stack
Go 1.23 · Gin · GORM · PostgreSQL · Redis · deployed on K8s

## Code Rules
- Errors: `fmt.Errorf("funcName: %w", err)` — always wrap with caller context
- No naked returns in funcs >3 lines
- No `init()` — use constructor functions
- No global mutable state
- Context: always first param, named `ctx`, never `context.Background()` in handlers

## Structure
cmd/server/       ← entry point only, no logic
internal/
  domain/         ← structs, interfaces (no imports from infra)
  repository/     ← DB only, returns domain types
  service/        ← business logic, calls repository
  handler/        ← HTTP only, calls service, no DB

Handler → Service → Repository. Never skip layers.

## Testing
- Unit tests: mock at repository interface, never mock DB driver
- Integration tests in `_test/integration/`, require `TEST_DB_URL` env
- Table-driven tests only for input/output variations
- No `t.Skip()` without a linked GitHub issue comment

## API Conventions
- Route format: `/v1/{resource}/{id}` (plural noun, no verbs)
- All responses: `{"data": ..., "error": null}` or `{"data": null, "error": "..."}`
- 422 for validation errors, 500 only for unexpected failures
- Never expose internal error messages to API responses

## Git
- Branch: `feat/`, `fix/`, `chore/` prefixes
- Commits: imperative mood, max 72 chars, no period
- Never commit directly to main

## Gotchas
- `PaymentID` is UUID string — never int
- Redis client is NOT thread-safe — use pool, never share single client
- `ProcessPayment()` is idempotent by `idempotency_key` — do NOT add retry logic at the call site
- DB migrations run automatically on startup — do NOT run manually in dev
- The `amount` field is in satang (×100) — never treat as baht directly

## Do NOT
- No `fmt.Println` — use `slog.Info/Error` with structured fields
- No hardcoded config values — all from `os.Getenv`
- No `SELECT *` — always explicit columns
- No direct `panic()` — return errors up the stack

## On Ambiguity
Ask ONE clarifying question before writing code. Do not assume business logic.
```

---

## Comparison — Before vs After

| | Before (bloated) | After (lean) |
|---|---|---|
| Line count | 280 lines | 73 lines |
| Estimated tokens | ~3,200 | ~650 |
| Token cost per session (40 turns) | ~128,000 | ~26,000 |
| Monthly cost saved (heavy user) | — | ~$40–$80/month |
| Claude compliance | Low (too much to follow) | High (dense, scannable) |

---

## The Mental Model

Think of CLAUDE.md like a **compiler flag file**, not a tutorial.

A compiler flag doesn't explain why flags exist — it just enforces them.
Your CLAUDE.md should do the same: state the constraint, not the reasoning (except in Gotchas, where the "why" prevents confusion).

```
# Bad: tutorial mode
When handling database errors, it's important to always wrap them because
this makes debugging easier and helps with distributed tracing...

# Good: compiler flag mode
DB errors: always wrap. `fmt.Errorf("repo.GetUser: %w", err)`
```

**The rule of thumb:** if a senior dev on your team would already know it, skip it.
Only write what a smart person would get wrong about your specific project.

---

## Quick Reference Checklist

Before adding any line to CLAUDE.md, ask:

- [ ] Is this something Claude could discover by reading my code? → **Skip it**
- [ ] Is this a general best practice? → **Skip it** (Claude already knows)
- [ ] Is this a project-specific constraint a smart dev could get wrong? → **Keep it**
- [ ] Is this a "Gotcha" that caused a real bug? → **Keep it, add why**
- [ ] Is this a deep procedure (>5 steps)? → **Move to a /command file**
- [ ] Can I say this in one line instead of three? → **Compress it**

---

## Token Budget by Section Type

| Section | Max Lines | Notes |
|---|---|---|
| Stack / Tech | 2–3 lines | Only unusual choices; skip obvious stuff |
| Code Rules | 8–12 lines | One rule per line, no explanation |
| Structure | 5–8 lines | Only if non-standard layout |
| Testing | 4–6 lines | Project-specific constraints only |
| API Conventions | 4–6 lines | Response format, error codes |
| Gotchas | 4–8 lines | Gold — spend tokens here |
| Do NOT list | 4–6 lines | Hard prohibitions only |
| On Ambiguity | 1–2 lines | How Claude should handle unclear tasks |
| **Total** | **~50–80 lines** | **Target: under 100 lines always** |
