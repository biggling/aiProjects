# Sales Page — Claude Code Elite Pack

> ⚠️ This file is superseded by the polished versions in `sales/`:
> - `sales/landing-page.html` — standalone HTML landing page (host anywhere)
> - `sales/gumroad-description.md` — Gumroad copy, ready to paste
> - `sales/social-launch-copy.md` — Reddit, Twitter, Product Hunt, HN, LinkedIn
>
> Platform: Gumroad (primary), Etsy (secondary)
> Price: $19 / $37 / $97
> Keyword target: "claude code CLAUDE.md config pack"

---

## HEADLINE

**Claude Code keeps forgetting your stack.**
**This fixes it permanently.**

---

## SUBHEADLINE

7 battle-tested CLAUDE.md configs + Memory OS + Auto Mode safety profiles — built by a senior engineer who actually uses Claude Code daily.

Drop them in. Stop explaining your architecture every session.

---

## THE PROBLEM (agitate the pain)

You pay $100–200/month for Claude Max.

But every new session, Claude starts fresh. You spend the first 20 minutes explaining:

- "We use Go — return errors, don't panic"
- "Our DB layer uses SQLAlchemy 2.x sessions, not the old style"
- "Don't use `get_node()` inside `_process()` in Godot"
- "This is a microservices repo — don't put business logic in handlers"

Then it still gets it wrong.

You correct it. It forgets by the next session.

Meanwhile the token counter climbs. You've burned 30k tokens re-explaining things that haven't changed in months.

**This is context rot. Every Claude Code user has it. Nobody talks about it.**

---

## WHAT THIS IS

A battle-tested config system built by a senior engineer (Go, Java, Python, Kotlin, TypeScript, Godot — 10 years building production microservices and side projects).

Not AI-generated templates. Not copied from GitHub. These are the actual configs from real production codebases, refined over dozens of sessions until Claude stopped making the same mistakes.

---

## WHAT YOU GET

### STARTER — $19

**7 Stack-Specific CLAUDE.md Files**

Drop the right one into your project root. Claude knows your conventions from turn 0.

- `go-microservices/` — error wrapping, no panic(), slog, interface-first, table-driven tests
- `typescript-node/` — strict mode, ESM, zod validation, no `any`, MCP SDK patterns
- `python-data-pipeline/` — SQLAlchemy 2.x, Alembic, Celery, loguru, pathlib everywhere
- `python-fastapi-react/` — asyncio.to_thread(), React Query, WebSocket patterns
- `kotlin-android/` — Compose + ViewModel + StateFlow, Room DAO, Hilt, coroutines
- `gdscript-godot4/` — signal-first design, no get_node() in loops, resource preloading
- `side-project-workspace/` — multi-project setup with automated agent runner

**Full Multi-Agent Script System**

Run Claude autonomously on any project, on a schedule, without babysitting.

- `run-agent.sh` — non-interactive Claude session with custom prompt
- `run-research.sh` — web research agent, saves findings automatically
- `run-agent-continue.sh` — inlines your continue.md + latest research into turn 0
- `crontab.conf` — ready-to-install: research at 08:00, work at 20:00
- `continue.md` template — Daily Tasks pattern so Claude always runs the right things first

---

### PRO — $37 (everything in Starter, plus:)

**Memory OS**

Claude maintains living documents across every session. No more context rot.

- `projectBrief.md` — your goals, stack, constraints (written once, always loaded)
- `activeContext.md` — what's in progress right now (Claude updates this each session)
- `progress.md` — done / blocked / next (running changelog)
- `systemPatterns.md` — architecture decisions, gotchas, naming rules (grows over time)
- `setup-memory-os.sh` — one-shot setup script, creates all files pre-populated

**Auto Mode Safety Profiles**

4 pre-built `.claude/settings.json` profiles. Drop in the right one before you give Claude the wheel.

- `conservative/` — read-only, confirms everything, for exploration
- `standard/` — allows edits, blocks git push and rm
- `trusted-dev/` — allows commits, blocks force-push and production deploys
- `ci-scripted/` — full access, designed for --bare cron/CI runs

**Hooks Library**

Automate Claude Code's lifecycle. These run as shell scripts on every session.

- Block `rm -rf` outside /tmp (pre-tool-call)
- Block `git push --force` (pre-tool-call)
- Log every tool call with timestamp (pre-tool-call)
- Telegram notification on completion (post-tool-call)
- Print git status on session open (session-start)
- Auto-load continue.md into context turn 0 (session-start)

---

### ELITE — $97 (everything in Pro, plus:)

**1M Context Optimization Guide**

Stop burning tokens on things Claude already knows.

- Why context bloat happens and how to stop it
- CLAUDE.md snippets that cut token waste by 40%
- Post-session summarize hook: auto-appends 3-line summary to activeContext.md
- Statusline config to display rate-limit usage in real time (v2.1.86+)

**Cross-Platform AGENTS.md Pack**

The same configs in OpenCode format. Works with OpenCode (120K stars, 5M users/month), Cursor, and any AGENTS.md-compatible tool.

- go-microservices/AGENTS.md
- typescript-node/AGENTS.md
- python-data-pipeline/AGENTS.md
- side-project-workspace/AGENTS.md

**Notion Side Project Dashboard**

One-click duplicate. Tracks all your projects, revenue targets, and weekly focus in one place.

- Kanban board by project status
- Timeline view with milestones
- Revenue tracker: targets vs actuals
- Weekly focus: top 3 tasks this week
- Research log per project

---

## WHO THIS IS FOR

**This is for you if:**
- You use Claude Code daily and pay for Claude Max or Pro
- You switch between stacks (Go one week, TypeScript the next)
- You've caught Claude generating the wrong patterns for your codebase
- You've spent 20+ minutes in a single session re-explaining architecture
- You want Claude running unattended on a schedule, not babysitting it

**This is NOT for you if:**
- You're just trying Claude Code for the first time
- You want a generic prompt list (there are free ones on GitHub)
- You don't have a codebase with actual conventions

---

## WHY NOT JUST USE FREE GITHUB REPOS?

Free repos give you a list of example CLAUDE.md files. They're generic, AI-generated, and written by someone who hasn't worked in your stack.

This pack is different:

| Free GitHub configs | This pack |
|---|---|
| Generic, one-size-fits-all | Stack-specific (Go vs Python vs Kotlin are very different) |
| Written for the demo, not production | Built from real projects with real bugs corrected |
| No context system | Memory OS keeps context alive across sessions |
| No Auto Mode safety | 4 profiles for different risk levels |
| No automation | Full cron-ready multi-agent runner |
| No cross-platform | AGENTS.md for OpenCode/Cursor included (Elite) |

---

## RESULTS YOU CAN EXPECT

- **First session:** Claude knows your stack with zero explanation
- **Week 1:** No more "actually in Go we..." corrections
- **Week 2:** Memory OS means Claude picks up exactly where you left off
- **Month 1:** Agents running on schedule, research and work happening while you sleep

---

## ABOUT THE AUTHOR

10 years as a software engineer. Go, Java, Python, Kotlin, TypeScript. Microservices, Kubernetes, mobile apps, trading bots. Based in Bangkok. Pays for Claude Max every month.

I built these configs because I was tired of Claude forgetting my stack. Then I built the agent runner because I have < 5 hours/week for side projects and needed the computer to work while I slept.

These are the actual files from my actual projects. I cleaned them up, generalized the names, and packaged them so you don't have to spend the 40+ hours I spent getting them right.

---

## FREQUENTLY ASKED QUESTIONS

**Do these work with Claude Code free tier?**
Yes. The CLAUDE.md configs and Memory OS work regardless of tier. The multi-agent scripts use `--print` mode which requires API access or a Claude Pro/Max subscription.

**What version of Claude Code do these work with?**
Tested on Claude Code v2.1.x (March 2026). The Auto Mode profiles use the settings.json format introduced in v2.0. Hooks use the standard hook API.

**Do these work with Cursor or other AI editors?**
The CLAUDE.md files work with any editor that respects the file. The AGENTS.md files (Elite tier) are specifically for OpenCode and other tools that support the AGENTS.md spec.

**Can I use these for a team?**
Yes. Pro and Elite buyers can use across their own projects. For team-wide deployment (5+ devs), see the team license option.

**What if Claude Code changes its API and something breaks?**
I use Claude Code daily. When something changes, I update the pack. All buyers get updates for free.

**Is there a refund policy?**
30-day no-questions refund. If you drop the configs in and they don't work for your stack, I'll refund you or customize one config for you directly.

---

## PRICING

| | Starter | Pro | Elite |
|---|---|---|---|
| **Price** | **$19** | **$37** | **$97** |
| 7 stack CLAUDE.md configs | ✓ | ✓ | ✓ |
| Multi-agent script system | ✓ | ✓ | ✓ |
| continue.md template | ✓ | ✓ | ✓ |
| Memory OS (4 templates + setup) | — | ✓ | ✓ |
| Auto Mode safety profiles (4) | — | ✓ | ✓ |
| Hooks library (6 hooks) | — | ✓ | ✓ |
| 1M context optimization | — | — | ✓ |
| Cross-platform AGENTS.md | — | — | ✓ |
| Notion dashboard template | — | — | ✓ |
| Free lifetime updates | ✓ | ✓ | ✓ |
| 30-day refund | ✓ | ✓ | ✓ |

---

## CALL TO ACTION

**[Get Starter — $19]**
Drop-in configs for your stack. Works in 10 minutes.

**[Get Pro — $37]** ← Most popular
Everything in Starter + Memory OS + Auto Mode + Hooks.

**[Get Elite — $97]**
The full system. Everything + cross-platform + Notion dashboard.

---

## LAUNCH POST (r/ClaudeCode)

> Title: I spent 40 hours figuring out the right CLAUDE.md setup for Go/TypeScript/Python — here's what I learned (and the files)
>
> Been using Claude Code daily for months. The biggest time sink wasn't the coding — it was re-explaining my stack conventions every session.
>
> Go: "return errors, don't panic." TypeScript: "strict mode, no any." Python: "SQLAlchemy 2.x sessions, not the old style." Every. Single. Session.
>
> So I spent a weekend building a proper config system. Stack-specific CLAUDE.md files, a Memory OS that keeps context alive across sessions, and an agent runner that works on a schedule.
>
> Wrote it up and packaged it. If you're hitting the same wall, might save you the 40 hours I spent.
>
> [link]
>
> Happy to answer questions about the specific patterns — especially the Go error handling conventions and the Memory OS setup.

---

## GUMROAD PRODUCT DESCRIPTION (short version, 300 words)

Claude Code keeps forgetting your stack. This fixes it permanently.

7 battle-tested CLAUDE.md configs for the stacks you actually use: Go microservices, TypeScript/Node, Python data pipelines, FastAPI+React, Kotlin/Android, Godot 4, and multi-project workspaces. Not AI-generated. Built from real production codebases over months of daily use.

Drop the right file into your project root. From turn 0, Claude knows your conventions — error handling patterns, naming rules, test structure, what not to do — without you explaining it.

**Starter ($19):** 7 stack configs + full multi-agent script system (run Claude on a schedule, unattended).

**Pro ($37):** Everything in Starter + Memory OS (Claude maintains context across sessions — no more context rot) + Auto Mode safety profiles (4 levels) + hooks library.

**Elite ($97):** Everything in Pro + 1M context optimization guide + cross-platform AGENTS.md for OpenCode/Cursor + Notion Side Project Dashboard template.

Built by a senior engineer (Go, Java, Python, Kotlin, TypeScript — 10 years). Used daily. Free lifetime updates. 30-day refund.

---

## ETSY LISTING TITLE

Claude Code CLAUDE.md Config Pack | Stack-Specific Templates for Go TypeScript Python | Memory OS | Auto Mode Profiles | AI Developer Tools

## ETSY TAGS

claude code, claude md template, ai developer tools, claude code config, claude code hooks, memory os, auto mode claude, typescript claude, go developer tools, python ai tools, claude code setup, developer productivity, ai coding assistant, claude code pack, vibe coding

---

## NOTES FOR LISTING

- Hero image: dark terminal screenshot showing CLAUDE.md being loaded, stack list overlaid
- Second image: Memory OS file tree showing the 4 templates
- Third image: before/after token usage (estimate: 30k saved per session)
- Price-raise trigger: raise Starter from $19 → $29 after 10 sales
- First 5 buyers: offer free 1:1 Zoom config review (social proof + feedback)
