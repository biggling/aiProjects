# Social Launch Copy — Claude Code Elite Pack

Launch in this order: Reddit → X/Twitter thread → Product Hunt → HN (Show HN)

---

## 1. Reddit Posts

### r/ClaudeAI — Primary launch post

**Title:**
I spent 40 hours building the right CLAUDE.md setup for 12 stacks — sharing what I learned (and the files)

**Body:**
Been using Claude Code daily for months. Biggest time sink wasn't the coding — it was re-explaining my stack conventions every session.

Go: "return errors, don't panic." TypeScript: "strict mode, no any, ESM only." Python: "SQLAlchemy 2.x — never the old session.query() style." Every. Single. Session.

So I spent a weekend building a proper config system. Here's what I found works:

**What actually changes Claude's behavior:**

The CLAUDE.md file is loaded on every turn. But most examples I found online are generic — they say things like "write clean code." That doesn't change anything.

What works is specificity:

- Bad: "Handle errors properly"
- Good: `Always wrap errors: fmt.Errorf("doing X: %w", err)` — never panic() in service code

- Bad: "Use async properly in FastAPI"
- Good: `Wrap all sync SQLAlchemy calls in asyncio.to_thread() — never call sync DB code from async handlers`

The more specific and stack-specific, the better. Generic instructions get ignored or misapplied.

**The Memory OS pattern:**

Four files in `memory-bank/`:
- `projectBrief.md` — written once: what the project is, the stack, non-negotiables
- `activeContext.md` — what's in progress right now (Claude updates this at session end)
- `progress.md` — done / blocked / next (running changelog)
- `systemPatterns.md` — architecture decisions + gotchas that accumulate over time

CLAUDE.md instruction: "At session start: read ALL files in memory-bank/. At session end: update activeContext.md and progress.md."

With this in place, Claude starts every session with full context. No re-explaining.

**The cron agent pattern:**

```bash
# 8am: research agent
0 8 * * * claude --print "$(cat research/AGENT.md)" > research/findings/$(date +%Y-%m-%d).md

# 8pm: work agent  
0 20 * * * claude --print "$(cat continue.md)" "do the next task"
```

Claude works while you sleep. You check the git log in the morning.

---

Packaged this into a proper product with 12 stack configs (just added Next.js, Rust, Java Spring Boot, React Native, Flutter/Dart) + the memory system + agent scripts. Link in bio if you want it.

Happy to share any specific configs or answer questions about the patterns.

---

### r/ClaudeAI — Softer variant (no product mention)

**Title:**
The CLAUDE.md pattern that actually changed how Claude Code works for me

**Body:**
After months of daily use, the thing that made the biggest difference wasn't prompt engineering — it was adding a `## Common Mistakes Without This Config` section to every CLAUDE.md.

Examples:

**Go:**
```
## Common Mistakes Claude Makes Without This Config
- Writing panic() in service code instead of returning errors
- Using interface{} instead of typed interfaces for repository mocks
- Placing business logic in HTTP handlers instead of the service layer
- Missing context.Context propagation through the call chain
```

**TypeScript:**
```
## Common Mistakes Claude Makes Without This Config
- Using interface everywhere instead of type for object shapes
- Using any instead of unknown + type guards
- Missing import type for type-only imports (causes circular deps in bundlers)
- Using Math.random() for IDs or tokens
```

When you explicitly tell Claude what it tends to get wrong for your specific stack, it stops getting it wrong. The problem wasn't that Claude didn't know the right patterns — it's that without a config, it defaults to the most common patterns it's seen in training data, which may not match your conventions.

Anyone else building out their CLAUDE.md? Curious what patterns people are using.

---

### r/golang

**Title:**
My CLAUDE.md for Go microservices — conventions that actually change Claude's output

**Body:**
Been iterating on this for months. The sections that have the most impact:

```markdown
## Error Handling
- Always wrap errors: fmt.Errorf("doing X: %w", err)
- Never panic() in library or service code — only main() for startup failures
- Use errors.Is() and errors.As() — never string matching

## What NOT to Do
- No init() with side effects
- No global mutable state  
- No interface{} without a clear reason
- No time.Sleep in production — use tickers or context deadlines
- No ignoring errors: _, err := f() must handle err
```

The "What NOT to Do" section is the highest-signal part. Claude already knows the good patterns. It needs the negative constraints to override its defaults.

Full config (with security, observability, graceful shutdown sections) here: [link]

---

### r/rust (if applicable)

**Title:**
Sharing my CLAUDE.md for Rust — stops Claude from using .unwrap() everywhere

**Body:**
The two conventions that change Rust output the most:

```markdown
## Error Handling
- Library code: use thiserror — define typed errors with #[derive(Error, Debug)]
- Application code: use anyhow::Result<T> — context() on every ? call
- Never .unwrap() in application code — only in tests/examples

## Async (Tokio)
- Use tokio::join!() for parallel futures — not sequential .await
- Never std::thread::sleep in async code — use tokio::time::sleep
- Mark async only when doing I/O — pure computation stays sync
```

Without these, Claude defaults to sprinkling .unwrap() everywhere and writing sequential awaits when the operations are independent.

Full Rust config: [link]

---

## 2. Twitter / X Thread

**Tweet 1 (hook):**
Claude Code keeps forgetting your stack conventions.

Every session: "In Go, we return errors, don't panic." "We use SQLAlchemy 2.x sessions." "Don't call get_node() in _process()."

Here's the system I built to fix this permanently 🧵

---

**Tweet 2:**
The root cause: CLAUDE.md is loaded every turn, but generic instructions ("write clean code") don't change Claude's behavior.

What works is specificity + negative constraints.

Bad: "Handle errors properly"
Good: "Always wrap errors: fmt.Errorf("doing X: %w", err) — never panic() in service code"

---

**Tweet 3:**
The highest-signal section isn't the conventions.

It's this:

```
## Common Mistakes Claude Makes Without This Config
- panic() in service code
- business logic in HTTP handlers
- missing context.Context propagation
- hardcoded DB URLs instead of env vars
```

Tell Claude what it gets wrong. It stops getting it wrong.

---

**Tweet 4:**
The Memory OS pattern eliminates context rot:

Four files in memory-bank/:
- projectBrief.md — written once, never changes
- activeContext.md — what's in progress right now
- progress.md — done/blocked/next
- systemPatterns.md — architecture decisions + gotchas

CLAUDE.md: "read ALL files in memory-bank/ at session start"

Claude starts every session with full context. No re-explaining.

---

**Tweet 5:**
The cron agent pattern:

Research at 8am. Work at 8pm. Weekly summary Sunday.

You check the git log in the morning.

[screenshot of git log showing commits made overnight]

---

**Tweet 6:**
I packaged this into a proper system:

- 12 stack configs (Go, TypeScript, Next.js, Rust, Java, Python, Kotlin, React Native, Flutter, Godot 4)
- Memory OS — 4 templates + setup script
- Auto Mode safety profiles — 4 levels
- Hooks — hard blocks, not soft instructions
- Cron-ready agent scripts

Link: [gumroad link]

Free lifetime updates. 30-day refund.

---

**Standalone tweet (no thread):**
The most impactful thing in my CLAUDE.md:

```
## Common Mistakes Claude Makes Without This Config
- panic() in service code instead of returning errors
- business logic in HTTP handlers
- missing context propagation
- hardcoded credentials instead of env vars
```

Tell Claude what it gets wrong. It stops getting it wrong.

(12-stack config pack if you want it: [link])

---

## 3. Product Hunt Listing

**Name:** Claude Code Elite Pack

**Tagline:** Stop explaining your stack to Claude every session

**Description (250 words):**

Claude Code starts every session with zero memory of your project. You spend 15 minutes re-explaining conventions. Claude still gets it wrong.

**The Claude Code Elite Pack fixes this permanently.**

12 battle-tested CLAUDE.md files — one for each stack you actually use. Drop the right one into your project root. From turn 0, Claude knows your error handling patterns, naming conventions, testing structure, and what NOT to do — without any explanation.

**Stacks covered:** Go microservices, TypeScript/Node.js, Next.js App Router, Rust (Axum + SQLx), Java Spring Boot, Python FastAPI + React, Python data pipelines, Kotlin Android (Compose), React Native/Expo, Flutter/Dart, Godot 4, multi-project workspace.

**Also included:**

- **Memory OS** — 4 structured files Claude reads at session start. Full context in 30 seconds. Architecture decisions and gotchas accumulate over time so Claude never repeats mistakes.

- **Auto Mode Safety Profiles** — 4 calibrated settings.json files. Conservative (read-only) to CI (full access). Stop choosing between "too locked down" and "might delete things."

- **Hooks Library** — Hard blocks on rm -rf and force-push. These can't be talked around. Telegram notifications when Claude finishes.

- **Autonomous Agent Runner** — Cron-ready scripts. Research at 8am, work at 8pm. Claude works while you sleep.

- **1M Context Optimization** — Snippets that cut token waste by ~40%. Real-time usage in your statusline.

Built by a senior engineer who uses this daily. Free lifetime updates. 30-day refund.

**Topics:** Developer Tools, Productivity, AI, Developer Experience

---

## 4. Hacker News — Show HN

**Title:**
Show HN: Claude Code Elite Pack – 12 stack-specific CLAUDE.md configs + memory system + agent runner

**Body:**
I've been using Claude Code daily for about six months and the biggest friction point was context loss: every session starts blank and you spend the first 15 minutes re-explaining your stack conventions.

I built a config system to fix this. It's now polished enough to share:

**What's in it:**

1. 12 CLAUDE.md files — one per stack (Go, TypeScript, Next.js, Rust, Java Spring Boot, Python FastAPI, Python data pipeline, Kotlin Android, React Native, Flutter, Godot 4, workspace). Each encodes real production conventions, not generic advice.

2. Memory OS — 4 structured files Claude reads at session start (projectBrief, activeContext, progress, systemPatterns). Full project context in 30 seconds. Gotchas accumulate in systemPatterns.md so Claude never repeats mistakes.

3. Auto Mode safety profiles — 4 calibrated settings.json files for different risk levels. I've seen Claude try rm -rf and force-push in Auto Mode without these.

4. Hooks — Shell scripts that hard-block dangerous commands (rm -rf, force-push). Exit code 1, can't be instructed around.

5. Cron-ready agent scripts — run-research.sh runs at 8am (web research, saves findings). run-agent-continue.sh runs at 8pm (inlines context, does next task). Claude works while you sleep.

6. Context optimization — CLAUDE.md snippets that cut token waste by ~40%, plus real-time token usage in the statusline.

The key insight from six months of iteration: the highest-signal section isn't the positive conventions — it's a "Common Mistakes Without This Config" section that lists exactly what Claude gets wrong for each stack. When you tell it what it tends to do wrong, it stops doing it.

[link]

Happy to answer questions about any of the specific patterns.

---

## 5. Dev.to Article Outline

**Title:** How I stopped Claude Code from forgetting my stack (and automated my side projects)

**Hook:** After 6 months of daily Claude Code use, I solved the two biggest problems: context rot and babysitting every session.

**Structure:**
1. The problem — context rot, specific examples by stack
2. Solution 1: Stack-specific CLAUDE.md (the negative constraints pattern)
3. Solution 2: Memory OS — the 4-file system
4. Solution 3: Auto Mode safety without locking Claude down
5. Solution 4: Cron agent — Claude works while you sleep
6. Results — before/after comparison
7. Where to get it (link)

---

## 6. LinkedIn Post

Had an interesting realization after 6 months of daily Claude Code use:

The most impactful thing in a CLAUDE.md file isn't the positive conventions ("use slog for logging"). It's the negative constraints:

```
## Common Mistakes Claude Makes Without This Config
- panic() in service code instead of returning errors
- Business logic in HTTP handlers instead of the service layer
- Missing context.Context propagation through the call chain
- Using interface{} where typed interfaces are appropriate
```

Claude already knows the right patterns. What it doesn't know is your specific conventions — which patterns to favor and which to avoid. The negative list is what disambiguates.

Packaged this learning (plus Memory OS, Auto Mode profiles, hooks, and a cron agent runner) into a proper system. 12 stacks covered.

Link in comments.

#DevTools #ClaudeCode #AI #DeveloperProductivity #SoftwareEngineering

---

## LAUNCH SEQUENCE

**Day 1 (morning):** Post to r/ClaudeAI — no product mention, just the pattern
**Day 1 (afternoon):** Post X/Twitter thread
**Day 2:** Submit to Product Hunt (Sunday evening for Monday launch)
**Day 3:** Post to stack-specific subreddits (r/golang, r/rust, r/androiddev, r/FlutterDev)
**Day 4:** Show HN
**Day 5:** Dev.to article (links back to everything)
**Week 2:** LinkedIn post targeting senior devs

**Price-raise trigger:** After 10 sales, raise Starter from $19 → $29 and announce it ("raising price in 48h") for urgency.
