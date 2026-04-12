# CLAUDE.md Effectiveness Test

**The problem:** CLAUDE.md instructions get ignored after 2-5 prompts (GitHub issue #668, #7777, #19635, #23032). Most developers have no way to know which rules Claude follows vs silently ignores.

This file gives you a systematic way to test your CLAUDE.md before relying on it in production.

---

## How to Run the Test

Start a **fresh Claude Code session** (not mid-conversation — context affects compliance).
Run each prompt below. Score Claude's response: ✅ followed / ❌ ignored / ⚠️ partial.

Then: move any rule Claude ignores into a **hook** instead. Hooks are deterministic — they cannot be ignored.

---

## Universal Tests (run for every stack)

### T1 — Error handling style
**Prompt:** `Write a function that reads a file and returns its contents as a string`

**What to check:**
- Go: Does it use `fmt.Errorf("reading file: %w", err)` or `return nil, err` bare?
- TypeScript: Does it use your preferred error pattern (Result type, throw, etc.)?
- Python: Does it use `logger.exception()` or bare `except:`?
- Java: Does it throw a domain-specific exception or generic `RuntimeException`?

Score: ✅ if follows your CLAUDE.md error convention exactly / ❌ if uses generic pattern

---

### T2 — Naming conventions
**Prompt:** `Add a boolean field to track whether a user has verified their email`

**What to check:** Does the variable name follow your convention?
- Go: `emailVerified` (not `email_verified` or `isEmailVerified`)
- TypeScript: `isEmailVerified` (not `emailVerified` or `email_verified`)
- Java: `emailVerified` in entity, `isEmailVerified()` as getter

Score: ✅ correct naming / ❌ wrong style

---

### T3 — Prohibited patterns
**Prompt:** `Write a function that gets a user from the database by ID`

**What to check:**
- Go: Does it avoid `panic()`? Does it use parameterized queries?
- TypeScript: Does it avoid `any`? Does it use Zod for input validation?
- Python: Does it avoid `session.query()` legacy style if you specified SQLAlchemy 2.x?
- Java: Does it go through the Repository layer (not direct EntityManager)?

Score: ✅ avoided all prohibited patterns / ❌ used a pattern you banned

---

### T4 — Project structure
**Prompt:** `Where should I put the logic for calculating a user's subscription price?`

**What to check:** Does Claude point to the correct layer?
- Go: `internal/service/` (not `internal/handler/`)
- TypeScript: `services/` (not `routes/`)
- Java: `service/` layer (not `controller/`)
- FastAPI: Service function (not route handler)

Score: ✅ correct layer / ❌ wrong layer

---

### T5 — Logging style
**Prompt:** `Add a log line when a payment fails`

**What to check:**
- Go: Uses `slog.Error("payment failed", "error", err, "user_id", id)` not `fmt.Printf`
- TypeScript: Uses `logger.error()` not `console.log()`
- Python: Uses `logger.exception()` not `print()`
- Java: Uses `log.error("payment failed: {}", err.getMessage())` not System.out

Score: ✅ uses your logging convention / ❌ uses wrong method

---

### T6 — Testing conventions
**Prompt:** `Write a test for the function you just wrote`

**What to check:**
- Go: Uses `testify/require` and `testify/assert`, table-driven?
- TypeScript: Uses `describe/it` with Vitest? No `var`?
- Python: Uses `pytest.fixture`? Mocks at HTTP client level?
- Java: `@WebMvcTest` or `@DataJpaTest` depending on layer?

Score: ✅ follows test conventions / ❌ generic test structure

---

## Long-Session Degradation Test

Instructions get ignored more as a session grows. Test this:

1. Run T1–T6 above at the START of a fresh session → record scores
2. Do 10 unrelated prompts (write 3 functions, fix 2 bugs, answer 2 questions)
3. Run T1, T3, T5 again → compare scores

**Expected finding:** T1 and T3 (error handling, prohibited patterns) degrade fastest.
**Fix:** Move the most critical rules to hooks. Keep CLAUDE.md under 60 lines.

---

## Scoring

| Score | What it means | Action |
|---|---|---|
| 5-6 ✅ | Config is working | Monitor during long sessions |
| 3-4 ✅ | Partial compliance | Move failing rules to hooks |
| 1-2 ✅ | Config mostly ignored | Major rewrite needed — see below |
| 0 ✅ | Config not loaded | Check CLAUDE.md is in project root |

---

## When Tests Fail: Fix Strategy

### Option 1: Move the rule to a hook (best for critical rules)
Rules that Claude ignores can be enforced deterministically via hooks.

```bash
# Example: ensure formatters run even if Claude skips them
# 4-hooks/post-tool-call/auto-format.sh handles this already
```

### Option 2: Be more specific in CLAUDE.md
Vague rules get ignored. Specific rules with examples are followed.

```markdown
# Bad — too vague (gets ignored)
Handle errors properly.

# Good — specific with example (gets followed)
Always wrap errors: fmt.Errorf("doing X: %w", err)
Never: return err  (unwrapped)
Never: panic()     (in service code)
```

### Option 3: Progressive disclosure (for long sessions)
Put the most critical rules at the TOP of CLAUDE.md — Claude reads top-down.
Move examples and rationale to a separate `docs/CONVENTIONS.md` file, and reference it:

```markdown
## Conventions
See docs/CONVENTIONS.md for full examples. Summary:
- Error wrapping: fmt.Errorf("context: %w", err)
- No panic() in service code
- All DB via Repository layer only
```

### Option 4: Use /compact regularly
Run `/compact` every 20-30 turns in long sessions. This compresses context and reloads
CLAUDE.md from scratch — compliance resets to session-start levels.

---

## What Good Looks Like

A well-configured CLAUDE.md achieves:
- **T1–T6: 5-6/6 ✅** at session start
- **T1, T3, T5: 3/3 ✅** after 10 turns
- **Prohibited patterns:** 0 violations in a 60-minute session
- **Time to correct Claude:** < 1 per session (vs 14+ corrections without this config)

---

## Re-Test Schedule

Run this test:
- After first setting up CLAUDE.md (baseline)
- After any major change to CLAUDE.md
- When you notice Claude making the same mistake twice in a session
- Monthly, to catch Claude model update drift
