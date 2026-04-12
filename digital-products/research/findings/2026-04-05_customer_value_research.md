# Digital Products — Customer Value Research
> 2026-04-05 | What customers need, what they'll pay for, and how to add more value

---

## TL;DR

Customers don't buy CLAUDE.md templates. They buy **saved money**, **saved time**, and **AI that actually listens**.  
The measurable ROI already exists — our job is to make it visible in the product and listing copy.

---

## 1. The Real Jobs-to-be-Done

A "job-to-be-done" is the real reason someone buys. Not "I need a template" — that's the surface. The jobs below are what customers are actually hiring our product to do.

| # | Job Statement | Trigger | Willingness to Pay |
|---|---|---|---|
| J1 | "When I start a new project, I want AI to know my conventions without me re-explaining" | Starting project #3 that week | HIGH — saves 1–2 hrs/project |
| J2 | "When Claude is burning my rate limit in 90 minutes, I want to fix it immediately" | Hitting 5hr session limit at noon | VERY HIGH — they're losing paid time |
| J3 | "When I'm reviewing Claude's suggestions, I want to accept more and reject less" | Manually fixing the same mistake for the 5th time | HIGH — directly linked to productivity |
| J4 | "When my team uses AI, I want everyone getting the same output, not random results" | Team lead whose junior and senior devs get different Claude quality | VERY HIGH — team license territory |
| J5 | "When I work on a new AI tool (Cursor, OpenCode), I want to carry my standards over" | Just installed Cursor or switched from VS Code | MEDIUM-HIGH — cross-tool bundle |
| J6 | "When I have 12 side projects, I want AI to context-switch instantly between them" | BiG himself — also 63% non-developer Claude users | HIGH — Memory OS product |
| J7 | "When I give Claude an agentic task, I want it to not delete my database" | First time using Auto Mode | VERY HIGH — safety is priceless |

---

## 2. Documented Pain Points (Evidence-Based)

### Pain Point #1: Token Waste — the #1 frustration
**Evidence:**
- "Claude Code is silently burning 10-20x your token budget" — DEV Community viral article (Mar 2026)
- 40–60% of read tokens go to **redundant file reads** (reads same file, edits it, reads again to verify)
- Max plan users ($100–200/mo) burning 5-hour session limits in **90 minutes** on identical workloads
- 1,279 sessions had 50+ consecutive failures burning ~250,000 API calls/day in one incident

**What this means for our product:**
- A CLAUDE.md that instructs Claude to avoid redundant reads = immediate measurable savings
- The ROI is concrete: $70–$190/month → $25–$80/month = **$45–$110/month saved**
- This is a **10–55x return** on a $37 product purchase in month 1 alone

### Pain Point #2: CLAUDE.md Ignored — high frustration
**Evidence:**
- Most common complaint on r/ClaudeCode: "Why does Claude ignore CLAUDE.md even with MUST in all caps?"
- CLAUDE.md can get very long and Claude stops following many directions
- Common error: "CLAUDE.md not found" when not in project root

**What causes it:**
- Instructions are too prescriptive (step-by-step), not goal+constraint style
- CLAUDE.md over 300 lines — token budget consumed but low attention
- Missing "Gotchas" section — highest-signal content that actually sticks

**What our product solves:**
- Under-200-line templates (lean, high-signal)
- Goal + constraints format (not railroad instructions)
- "Gotchas" section included in every stack variant
- Setup guide: where to place the file, how to verify it's loading

### Pain Point #3: Starting From Scratch Every Project
**Evidence:**
- "Every new project requires rebuilding the same folder structures, configs, and boilerplate from scratch"
- `/init` generates a starter CLAUDE.md — but it's generic, not stack-specific
- Developers want clarity on "when to use command vs agent vs skill"

**What our product solves:**
- 5 pre-built stack variants (Go, TS, Python, K8s, Side Project)
- Drop-in: copy to project root, done
- Immediate: no setup time, no decisions to make

### Pain Point #4: Context Rot — sessions degrade over time
**Evidence:**
- "Things near the middle of a huge context get underweighted" — technical behavior of attention
- 58% cost reduction with automated context extraction (measurable)
- 82% token recovery per session via progressive disclosure (ClaudeFast study)
- 22% faster task completion with precision context

**What our product solves:**
- Memory OS (Memory Bank pattern): structured context that survives session resets
- `activeContext.md`, `projectBrief.md`, `progress.md` = context that reloads cleanly

### Pain Point #5: AI Suggestion Rejection Rate
**Evidence (Cursor-specific but same mental model):**
- Developers going from **30% acceptance → 80%+ acceptance** just by adding .cursorrules
- Code review comments like "we don't use default exports here" disappear when AI knows conventions
- AI becomes "context-aware coding partner" instead of generic tool

**What our product solves:**
- Stack-specific rules that encode actual coding conventions (BiG's real-world patterns)
- Both .cursorrules and CLAUDE.md variants cover same stacks
- Reduces back-and-forth = faster delivery

### Pain Point #6: Team Inconsistency
**Evidence:**
- "When .cursorrules/CLAUDE.md are checked into version control, every developer gets same AI behavior"
- Cursor Business ($40/seat) offers shared team rules as a paid feature
- Team leads set up AI configs for 2–20 person teams → this is the $97–$197 team license

**What our product solves:**
- Ready-to-commit configs designed for version control
- Team license tier = one purchase, entire team onboarded
- Governance profiles in Auto Mode pack = safe for teams

---

## 3. Measurable Outcomes (The ROI to Sell)

These are specific numbers we can use in listing copy and launch posts:

| Outcome | Metric | Source |
|---|---|---|
| Token cost reduction | 50–70% with well-crafted CLAUDE.md | richardporter.dev, DEV Community |
| Input token drop with precision context | 65–70% | vexp.dev |
| Monthly cost savings (heavy user) | $45–$110/month | Calculated from $70–190 → $25–80 range |
| Task completion speed | 22% faster | ClaudeFast study |
| Token recovery per session (Memory Bank) | 82% improvement via progressive disclosure | ClaudeFast Code Kit data |
| Cursor suggestion acceptance rate | 30% → 80%+ | Multiple Cursor dev blog posts |
| Cost reduction with automation | ~58% | benchmarked tests |

**Headline copy that sells:**
- "Stop burning $100+/month on wasted Claude tokens"
- "Get Claude to actually follow your coding standards"
- "Drop in one file. Get consistent AI output across your entire team."
- "Set up once, carry your standards across Claude Code, Cursor, and OpenCode"

---

## 4. Value Gap Map — What Exists vs What We Offer

| Customer Need | Free Solutions | Our Gap to Fill |
|---|---|---|
| Basic CLAUDE.md template | `/init` command, GitHub repos | Stack-specific, battle-tested, under 200 lines, with rationale |
| Token reduction | Generic blog posts | Actionable configs with specific token-saving directives built-in |
| Memory Bank setup | Cline Memory Bank repo (complex) | Drop-in Memory OS: pre-wired files + setup script + guide |
| Cross-tool configs | awesome-cursorrules (raw list) | Curated + stack-matched CLAUDE.md + .cursorrules + AGENTS.md bundle |
| Auto Mode safety | Anthropic docs (vague) | Opinionated safety profiles: hard-lock constraints, trust levels, diff-review hooks |
| Team consistency | DIY in version control | Packaged team config with governance guide |
| Context rot fix | Blog posts | Working Memory OS files + hooks to reload context |

---

## 5. Value Ladder Design (Revised)

The value ladder maps to progressively higher-value jobs:

```
FREE (lead magnet)
└── Single CLAUDE.md example on GitHub / Reddit post
    └── Drives traffic to Gumroad

$19 — STARTER (J1, J3)
└── 3 CLAUDE.md stacks (Go, TypeScript, Side Project)
    3 .cursorrules variants (same stacks)
    "Why this works" README
    Token-saving directives built in
    → Solves: "Set up AI context for my stack in 5 minutes"

$37 — PRO (J1, J2, J3, J6)
└── Everything in Starter +
    5 stacks (adds Python ML, K8s/microservices)
    Memory OS (activeContext + projectBrief + progress + hooks)
    Auto Mode safety profiles (trusted commands, hard locks)
    AGENTS.md for OpenCode
    Setup script (bash, auto-installs all files)
    → Solves: "Fix my token burn + stop context rot + carry this to OpenCode"

$97 — ELITE (all 7 jobs)
└── Everything in Pro +
    Indie Hacker OS (Notion template — multi-project tracker)
    Multi-Platform Revenue Tracker (Google Sheets)
    1M context optimization variant
    Team onboarding guide (for 2–10 devs)
    Quarterly update promise
    → Solves: "Make my entire AI-coding setup production-grade, once"

$197 — TEAM LICENSE (J4, J7)
└── Elite pack for up to 10 devs
    Team governance CLAUDE.md (code review hooks, consistency rules)
    Auto Mode safe-for-teams profiles
    Slack/Notion onboarding doc template
    → Solves: "Roll this out to my whole team"
```

---

## 6. How to Add More Value — Specific Tactics

### Tactic 1: Document the WHY (highest-leverage, zero extra work)
Every template rule should have a 1-line comment explaining why it's there.  
Example:
```
# NEVER use fmt.Println in production code — use slog with structured fields
# WHY: fmt.Println breaks log aggregation in K8s; slog gives free JSON formatting
```
This turns a generic config file into an opinionated engineering document.  
**Perceived value increase: HIGH. Build cost: near-zero.**

### Tactic 2: Include a "Gotchas" Section in Each Template
The #1 high-signal content that actually gets followed.  
Example gotchas for Go template:
```
## Gotchas (read these or waste 2 hours)
- Don't use init() functions — they make test setup order unpredictable
- context.Background() is only for main(); all handlers receive ctx from params
- Never shadow the err variable; always name distinctly (parseErr, dbErr)
```
**Perceived value increase: VERY HIGH. This is what experienced devs have learned the hard way.**

### Tactic 3: Measurable Token Budget Directives
Include directives specifically designed to reduce token waste:
```
## Token Budget Rules
- READ files only once per session; cache your understanding in memory
- When verifying changes, trust your diff — do NOT re-read the full file
- Use TodoWrite to track progress instead of re-reading the codebase
- Compact long sessions with /compact before switching tasks
```
**Perceived value increase: HIGH. Lets us make the "$45–$110/month saved" claim.**

### Tactic 4: Setup Script (5-minute onboarding)
Include a `setup.sh` that:
1. Detects project type (Go/TS/Python) from existing files
2. Copies the matching CLAUDE.md + .cursorrules to project root
3. Inits the memory-bank/ folder
4. Prints "You're set. Run `claude` to start."

**Perceived value increase: VERY HIGH. Reduces friction from "I need to figure this out" to "it just works".**  
**Build cost: 1–2 hours.**

### Tactic 5: Screen Recording Demo (Etsy dwell-time hack + trust builder)
A 30–60s silent screen recording showing:
- Before: Claude ignoring conventions, re-reading files, burning tokens
- After: Claude following the CLAUDE.md, no redundant reads, consistent output

**Etsy uses dwell time on video thumbnails as a ranking signal.**  
**Trust signal: showing real usage > describing features.**

### Tactic 6: Post-Purchase Email Sequence (Gumroad automation)
3-email sequence:
1. **Day 0:** How to place the files + verify CLAUDE.md is loading (solves #1 failure point)
2. **Day 3:** "Did you know?" — the 3 most impactful directives and why they work
3. **Day 7:** Upsell prompt → "Ready for the Memory OS? Here's what context rot costs you per month"

**Revenue increase: Post-purchase upsells have highest conversion (customer already bought, no new payment friction).**

### Tactic 7: Quarterly Update Promise (Retention + Premium Signal)
Include: "These configs are updated quarterly as Claude Code, Cursor, and OpenCode evolve."  
Gumroad supports sending updates to buyers automatically.  
**Perceived value increase: HIGH. Turns a one-time purchase into a living product.**

---

## 7. Buyer Persona — Updated with Pain-Point Data

### Primary: "Burning Budget Brandon"
- Claude Max subscriber ($100–200/mo)
- Watches his 5-hour session limit disappear before lunch
- Pain: Paying $200/mo for Claude Max but getting 90 minutes of productivity
- Trigger: Reads "Claude Code is silently burning 10-20x your token budget"
- **Decision logic:** $37 Pro pack = **1 month ROI if it saves just 1 day of wasted sessions**
- Discovery: DEV Community, r/ClaudeCode, X (viral token-burning posts)

### Secondary: "Setup Sam"
- Starts 2–3 new projects per week (side projects, client work)
- Pain: Re-explaining the same conventions on every project, every session
- Trigger: Third time Claude writes `fmt.Println` after being told not to
- **Decision logic:** $19 Starter = 20 minutes of saved setup time per project = paid back in week 1
- Discovery: r/ClaudeCode "how do you structure your CLAUDE.md?" threads

### Tertiary: "Team Lead Taylor"  
- Leads a 3–15 person engineering team
- Pain: Junior devs get inconsistent Claude output; code review catching AI-style violations
- Trigger: Code review comment "stop using default exports" (for the 10th time)
- **Decision logic:** $197 team license / company expense = justifiable with 1 team meeting saved
- Discovery: Company Slack AI channels, engineering blogs

### Emerging: "Cross-Tool Chloe"
- Uses both Cursor and Claude Code (very common in 2026)
- Pain: Maintains separate configs for each tool, they drift out of sync
- Trigger: Installs Cursor, realizes her CLAUDE.md conventions don't carry over
- **Decision logic:** $37 Pro = covers all tools at once, never drift again
- Discovery: Cursor subreddit, X posts comparing Claude Code vs Cursor

---

## 8. Anti-Features (Things That Kill Perceived Value)

Avoid these to protect conversion:
- **Walls of text with no structure** — developers scan, they don't read; use headers and code blocks
- **Generic rules** (e.g., "write clean code") — no perceived value vs. free GitHub repos
- **Over-100-line README** — if it needs a manual, it's too complex; ship a setup script instead
- **Prompts framed as "templates"** — prompt packs are dead (4.1% breakout rate); frame as "configs" or "engineering standards"
- **AI-generated look** — buyers actively avoid PDF-style AI output on Etsy; "Human Touch" framing is a real premium signal

---

## 9. Competitive Value Positioning

| Competitor | Their Value | Our Differentiation |
|---|---|---|
| chongdashu Builder Pack #2 | Hooks, commands, subagents — workflow hacks | Stack-specific depth + Memory OS + token-saving directives + cross-tool |
| awesome-cursorrules (free) | .cursorrules collection, all frameworks | Curated to 5 production stacks + CLAUDE.md match + setup script + rationale |
| jimgle Claude Code Companion | Debug/planning template prompts | Config files (not prompts) + measurable token savings |
| aitmpl.com (free, 1000+) | Breadth — every possible template | Depth + battle-tested "Human Touch" + BiG's real production experience |
| ClaudeFast Code Kit | Token optimization focus | Cross-tool bundle + Memory OS + team license + cheaper entry point |

**Our positioning statement (v1):**
> "Production-grade AI IDE configs built by a senior backend engineer with 10 years of Go/Java/K8s experience. Works in Claude Code, Cursor, and OpenCode. Cuts token waste by 50–70% in session 1."

---

## 10. Summary — Priority Value Additions

Ranked by impact vs. effort:

| Action | Customer Value | Build Effort | Priority |
|---|---|---|---|
| Add WHY comments to every rule | Very High | Zero | **Do now** |
| Add "Gotchas" section per stack | Very High | 1–2 hrs | **Do now** |
| Add token-saving directives | High | 1 hr | **Do now** |
| Write setup.sh script | Very High | 2 hrs | **Phase 1** |
| Post-purchase email sequence | High (revenue) | 1 hr | **Phase 1** |
| Quarterly update promise | High (trust) | Zero (promise only) | **Add to listing** |
| Screen recording demo | High (Etsy) | 30 min | **Phase 1** |
| Memory OS drop-in files | Very High | 1–2 days | **Phase 1 Pro tier** |
| Indie Hacker OS Notion | Medium-High | 2–3 days | **Phase 2** |
| Team onboarding guide | Very High (team sales) | 1 day | **Phase 2** |

---

*Sources: DEV Community (token burning analysis), richardporter.dev, vexp.dev, ClaudeFast Code Kit study, dotcursorrules.com, NxCode Cursor stats, r/ClaudeCode threads, InsightRaider 146K Gumroad analysis, growthrrocks.com value ladder, profitproo.com bundling guide*
