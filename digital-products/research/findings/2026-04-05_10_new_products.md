# Digital Products — 10 New Product Research
> 2026-04-05 | New opportunities beyond existing 7 products

---

## Context

Existing ranked products (from v2 feasibility):
1. AI IDE Config Bundle (CLAUDE.md + .cursorrules + AGENTS.md) — GREEN
2. Memory OS Add-on — GREEN
3. Auto Mode Safety Profiles — GREEN
4. Cursor Rules Pack — GREEN
5. Indie Hacker OS Notion — YELLOW-GREEN
6. Revenue Tracker Google Sheets — YELLOW-GREEN
7. Non-Dev Claude Pack — YELLOW

The 10 products below are NEW opportunities not yet in that list.

---

## Product #8 — Full 5-Tool AI Config Bundle
### (CLAUDE.md + .cursorrules + .windsurfrules + GEMINI.md + AGENTS.md)

**What is it:**
Expand the existing bundle to cover all 5 major AI coding tools, not just 3.

**New tools discovered:**
- **Windsurf** uses `.windsurf/rules/*.md` (or `.windsurfrules`) — reads both formats
- **Gemini CLI** uses `GEMINI.md` — Google's open-source terminal AI agent (GitHub: google-gemini/gemini-cli)
- **Kiro (AWS)** uses "steering files" — specs-centric AI IDE in free early access
- **AGENTS.md** is now an open standard adopted by 60,000+ open-source projects, supported by Claude Code, Cursor, Windsurf, Copilot, Devin, and Gemini CLI

**Market signal:**
- AI context management article "across Claude, Cursor, Kiro, Gemini and custom agents" — DEV Community confirms this multi-tool reality
- Windsurf: 2M+ users, now includes Gemini 3 Pro + Claude Sonnet
- Gemini CLI: open-source, MIT license, free to use — growing fast
- Zero paid product bundles all 5 formats confirmed

**TAM:** Claude Code + Cursor + Windsurf + Gemini CLI users = 10M+ developers

| Factor | Score | Notes |
|---|---|---|
| Market demand | 9/10 | 5 tools, all reading config files |
| Competition | 9/10 | Zero cross-5-tool bundles found |
| BiG's moat | 9/10 | Same engineering experience, incremental format work |
| Build effort | Low | Translate existing CLAUDE.md to 4 more formats |
| Price ceiling | $49–$79 | "All 5 AI IDEs" justifies higher price than 3-tool bundle |

**Feasibility: GREEN — Upgrade from 3-tool to 5-tool bundle. Small effort, significant differentiation.**

---

## Product #9 — Kiro Spec-Driven Development Templates (AWS AI IDE)

**What is it:**
Kiro uses "steering files" + "spec files" — a different paradigm from CLAUDE.md.
Instead of rules, Kiro works from specs: requirements → design → tasks.
A pack of pre-built Kiro spec templates for common project types.

**Market signal:**
- AWS launched Kiro in 2026: "specs-centric answer to Windsurf and Cursor" — The New Stack
- Free early access = growing user base with zero competition in template market
- Kiro's unique angle: persistent workspace knowledge files for coding conventions and architecture patterns
- "60,000+ open-source projects adopted AGENTS.md" — same community that will adopt Kiro specs

**What the pack includes:**
- Steering files for: Go API service, TypeScript frontend, Python ML pipeline, K8s infra
- Spec templates: REST API spec, microservice decomposition, DB schema design
- Requirements template: user story → acceptance criteria format Kiro expects

**BiG's advantage:** Kiro is AWS-native — BiG's K8s/microservices background directly applies.

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Early but AWS distribution = fast growth |
| Competition | 10/10 | Near-zero (tool is very new) |
| BiG's moat | 8/10 | AWS/K8s experience, new tool expertise |
| Build effort | Medium (2–3 days) | Different format, needs learning |
| Price ceiling | $29–$49 | Early adopter pricing |
| First-mover value | Very High | Own the Kiro config niche from day 1 |

**Feasibility: GREEN (early mover) — Low competition window open NOW. Build fast before competitors discover it.**

---

## Product #10 — GitHub Actions CI/CD Workflow Pack

**What is it:**
Pre-built `.github/workflows/` YAML files for modern development stacks.
Not generic — stack-specific and AI-project-aware (includes Claude Code + Cursor in the loop).

**Market signal:**
- GitHub Actions used by tens of millions of repos
- Developers still manually copy workflow YAML from Stack Overflow and hope it works
- "Workflow automations consistently generate $500–$1,500/month for solo creators" — digitalapplied.com
- "Products priced $19–$39 hit impulse-buy threshold while generating meaningful revenue"
- Claude Code `--bare` flag (for CI/CD scripted calls) = new hook into BiG's existing research

**Pack contents (differentiated):**
- Go monorepo: test → build → docker → K8s deploy
- TypeScript: lint → type-check → test → Vercel/Fly deploy
- Python ML: test → model validation → container → deploy
- **BONUS: "AI-Assisted CI" workflow** — Claude Code review step using `--bare` flag in pipeline
- Reusable composite actions for: semantic versioning, changelog generation, Slack notifications

**BiG's moat:** Real K8s/microservices CI/CD experience. These aren't toy pipelines — they handle monorepos, matrix builds, conditional deploys.

| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Every dev repo needs CI/CD |
| Competition | 6/10 | Free templates exist; stack-specific + AI-step = differentiation |
| BiG's moat | 9/10 | 10 years of production CI/CD |
| Build effort | Medium (2–3 days) | Need to test each workflow |
| Price ceiling | $29–$59 | Workflow packs sell $29–$299 |
| Evergreen value | High | CI/CD needs don't go away |

**Feasibility: YELLOW-GREEN — Phase 2. "AI-Assisted CI" step is unique differentiator no competitor has.**

---

## Product #11 — API Documentation Template Pack

**What is it:**
Ready-to-use Markdown/Word templates for REST API documentation.
Endpoint reference, auth guide, error codes, rate limiting, getting-started tutorial.

**Market signal:**
- Real case study found: creator built API doc templates, sold on Gumroad for $12, first sale in 11 days
- "Engineering Documentation Templates 2026" is a confirmed search demand — docsie.io
- Every developer starting a new API project recreates the same doc structure from scratch
- "REST APIs only for v1 — keeping scope tight meant shipping faster" — proven scope strategy

**BiG's version (upgraded):**
- Include CLAUDE.md instructions for generating API docs automatically
- Add Markdown + Notion + Confluence format variants
- Price at $19 (vs. competitor's $12) — add the CLAUDE.md integration to justify premium

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Every API needs docs; proven buyer |
| Competition | 6/10 | Some templates exist at low prices |
| BiG's moat | 7/10 | Real API experience + CLAUDE.md integration = upgrade |
| Build effort | Low (1 day) | Templates + 3 format variants |
| Price ceiling | $15–$29 | Low impulse-buy category |
| Quick to ship | Very High | Fastest new product to build |

**Feasibility: YELLOW-GREEN — Phase 2. Low effort, proven demand. Bundle add-on or standalone at $19.**

---

## Product #12 — System Design Interview Cheat Sheet Pack

**What is it:**
Visual cheat sheets + templates for system design interviews.
Covers: scalability, CAP theorem, database selection, caching, load balancing, message queues.

**Market signal:**
- ByteByteGo charges $99/year — proven massive demand
- Individual cheat sheet packs sell at $39
- "Interview Prep Pro Bundle (11 products) at $199 with 30% discount" = premium bundle territory
- "lockedinai.com: 12 Templates Google Engineers Actually Use" — confirms template format works
- Evergreen demand: developers always preparing for interviews

**BiG's differentiation:**
- Include a CLAUDE.md specifically tuned for system design practice sessions with Claude
- Add "AI-Assisted System Design" guide: how to use Claude Code to practice interviews
- Stack-specific templates: design a payment service (Go), design a recommendation engine (Python ML)
- This is the intersection of BiG's backend expertise + AI tools knowledge = unique angle

| Factor | Score | Notes |
|---|---|---|
| Market demand | 9/10 | Evergreen; ByteByteGo proves massive market |
| Competition | 4/10 | ByteByteGo, Grokking — established competitors |
| BiG's moat | 7/10 | "AI-Assisted practice with Claude" is unique angle |
| Build effort | Medium (3–4 days) | Visual design matters here |
| Price ceiling | $39–$99 | ByteByteGo validates $99 |
| Risk | Competition is strong | Must differentiate on AI angle, not content alone |

**Feasibility: YELLOW — Phase 3. High demand but strong competition. Only viable with "AI practice" angle as differentiator.**

---

## Product #13 — Go Microservice Starter Kit + CLAUDE.md

**What is it:**
NOT a full code boilerplate (too complex to maintain). Instead:
A "decision kit" — architecture patterns, folder structure template, CLAUDE.md, and GitHub Actions workflow, packaged as a ZIP with a README explaining every decision.

**Why not a code boilerplate:**
- Code boilerplates require ongoing maintenance as deps update
- Decision kits are evergreen — the patterns don't change with library versions
- Less liability, same perceived value for the buyer learning the patterns

**Pack contents:**
- Folder structure template (hexagonal architecture, Go conventions)
- CLAUDE.md for Go microservice (BiG's battle-tested version)
- GitHub Actions workflow (from Product #10 — cross-sell opportunity)
- Architecture Decision Records (ADRs) templates — pre-filled with Go-specific decisions
- "Why we made these choices" README — the highest-value content

**Market signal:**
- No Go-specific SaaS boilerplate found in search results (all Next.js)
- Go is BiG's primary language — maximum authenticity
- "Sell the decision-making, not the boilerplate" is underserved in Go ecosystem

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Go dev community pays for quality resources |
| Competition | 8/10 | Very few paid Go architecture packs |
| BiG's moat | 10/10 | BiG writes Go professionally — maximum credibility |
| Build effort | Medium (2–3 days) | Document existing patterns |
| Price ceiling | $37–$79 | Architecture resources command premium |

**Feasibility: YELLOW-GREEN — Phase 2. BiG's strongest moat product. Easy to create by documenting what he already knows.**

---

## Product #14 — Developer-Niche n8n Workflow Pack

**What is it:**
n8n automation workflows specifically for developers — NOT generic business automation.

**Why niche matters:** Generic n8n packs are commoditized ($10 flooding). Dev-specific workflows have less competition and a willing-to-pay audience.

**Workflows to include:**
- GitHub PR → Claude Code review summary → Slack notification
- Deploy failure → PagerDuty + automatic Claude diagnosis
- New GitHub issue → Claude triages, labels, assigns priority
- Weekly repo activity digest → Slack/email with AI summary
- Gumroad new sale → CRM + thank-you email sequence
- Claude Code session cost tracker → daily Notion log

**Market signal:**
- "n8n monetization: $5K+/month — 5 proven strategies" — ritz7.com
- n8n AI Agent Workflow Blueprint (JSON) actively selling on Gumroad: limitlessai.gumroad.com
- "Workflows priced $29 (simple) to $299+ (complex, industry-specific)"
- 6,238 AI automation workflows in n8n community = proven demand
- Developer-specific workflows NOT found in community library = clear gap

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | n8n market proven; dev niche underserved |
| Competition | 7/10 | Generic n8n saturated; developer-specific = gap |
| BiG's moat | 7/10 | Builds these workflows anyway for his own stack |
| Build effort | Low-Medium (1–2 days) | JSON exports + documentation |
| Price ceiling | $29–$79 | Niche specificity justifies premium vs generic |

**Feasibility: YELLOW-GREEN — Phase 2. Ship as "Dev Automation Pack" — clearly separate from commodity n8n space.**

---

## Product #15 — AI IDE Team Rollout Guide

**What is it:**
A practical PDF + Notion guide for engineering managers rolling out Claude Code or Cursor to a development team of 5–50 people.

**What it covers:**
- How to create a team CLAUDE.md baseline (governance edition)
- Cost management: setting token budgets per dev, per team
- Onboarding sequence: week 1/2/3 rollout plan
- Auto Mode safety policy for teams (what to allow, what to lock)
- Measuring ROI: how to show your manager the productivity gain
- Anti-patterns to avoid when teams use AI IDEs

**Market signal:**
- "Team Lead Taylor" persona validated — sets up Claude Code for 2–20 devs
- Cursor Business ($40/seat) includes team-shared rules as a paid feature = proves team willingness to pay
- 92% of US devs use AI tools daily — every team is figuring this out right now
- Zero guides found for "how to roll out AI IDEs to a team" as a paid product
- B2B angle: company expense account = less price sensitivity ($97–$197)

| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Every dev team is navigating this in 2026 |
| Competition | 9/10 | Zero paid team rollout guides found |
| BiG's moat | 7/10 | Less direct experience but logical extension |
| Build effort | Medium (2–3 days) | Research + document + Notion template |
| Price ceiling | $97–$197 | B2B purchase = company expense |
| Revenue potential | High | Single team sale = 3-5x individual product price |

**Feasibility: YELLOW-GREEN — Phase 2-3. B2B pricing makes even 5 sales/month = $500–$1,000.**

---

## Product #16 — Architecture Decision Record (ADR) Template Pack

**What is it:**
Pre-written Architecture Decision Records for common microservices decisions — the "rationale documents" engineering teams write when making tech choices.

**What's included:**
- ADR template (standard format: title, status, context, decision, consequences)
- 20 pre-written ADRs for common decisions:
  - "Why we chose PostgreSQL over MongoDB"
  - "Why we use event sourcing for audit trails"
  - "Why we chose gRPC for internal services"
  - "Why we use CQRS in this domain"
  - "Why we chose Kubernetes over ECS"
- CLAUDE.md directive: "Read ADRs in /docs/decisions/ before proposing architecture changes"
- Guide: how to write ADRs that AI tools can actually use as context

**Market signal:**
- ADRs are a growing practice — every "serious" engineering blog mentions them
- Zero paid ADR template packs found on Gumroad or Etsy
- "60,000 open-source projects adopted AGENTS.md" = same community values documented decisions
- Pre-written ADRs remove the "blank page" problem for teams starting this practice
- CLAUDE.md integration = natural bundle with the main product

| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Growing practice, underserved in paid market |
| Competition | 9/10 | Near-zero paid ADR products |
| BiG's moat | 9/10 | Real microservices experience = authentic ADRs |
| Build effort | Low-Medium (1–2 days) | Document decisions BiG has already made |
| Price ceiling | $29–$49 | Technical doc templates |
| Bundle synergy | Very High | Natural add-on to CLAUDE.md Config Pack |

**Feasibility: GREEN — underrated product. BiG can write these in an afternoon. Strong bundle add-on.**

---

## Product #17 — AI-Assisted Code Review Checklist Pack

**What is it:**
CLAUDE.md + .cursorrules templates specifically optimized for code review workflows.
Plus: checklist templates (Notion/Markdown) for human + AI hybrid review.

**What it solves:**
Developers using Claude Code for code review get generic feedback.
A purpose-built review CLAUDE.md gives Claude the context to catch:
- Security issues specific to your stack (SQL injection patterns in Go, XSS in your template engine)
- Business logic violations (e.g., "payment amounts must be in satang")
- Performance anti-patterns (N+1 queries for your ORM)
- Team conventions (import order, naming, error handling style)

**Pack contents:**
- Review-mode CLAUDE.md (separate from dev-mode CLAUDE.md — loads only during review)
- `/review` slash command template: runs full security + perf + convention check
- Human review checklist (Notion): security → performance → business logic → conventions
- PR description template that maximizes Claude's review quality

**Market signal:**
- Code review is where "team consistency" pain is most felt (Teams don't care about your dev CLAUDE.md — they care about review output consistency)
- Zero review-specific CLAUDE.md templates found
- "Code review comments like 'we don't use default exports here' disappear when AI knows conventions" — directly validates this product

| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Every team does code review; AI review is hot |
| Competition | 9/10 | Zero review-specific config packs found |
| BiG's moat | 8/10 | Production code review experience |
| Build effort | Low (1 day) | Extend existing CLAUDE.md into review mode |
| Price ceiling | $29–$49 | Or bundle into Pro tier |
| Bundle synergy | Very High | Natural Pro tier addition |

**Feasibility: GREEN — low effort, high value, natural bundle add-on. Add to Pro tier.**

---

## Summary — All 10 New Products Ranked

| Rank | Product | Market Demand | Competition | BiG's Moat | Build Effort | Phase | Feasibility |
|---|---|---|---|---|---|---|---|
| #8 | 5-Tool AI Config Bundle (+ Windsurf/Gemini/Kiro) | 9/10 | 9/10 | 9/10 | Low | Phase 1 | **GREEN** |
| #16 | ADR Template Pack | 7/10 | 9/10 | 9/10 | Low | Phase 1 | **GREEN** |
| #17 | AI Code Review Checklist Pack | 8/10 | 9/10 | 8/10 | Low | Phase 1 | **GREEN** |
| #9 | Kiro Spec Templates (AWS IDE) | 7/10 | 10/10 | 8/10 | Medium | Phase 1 | **GREEN (early mover)** |
| #10 | GitHub Actions CI/CD Pack | 8/10 | 6/10 | 9/10 | Medium | Phase 2 | **YELLOW-GREEN** |
| #13 | Go Microservice Decision Kit | 7/10 | 8/10 | 10/10 | Medium | Phase 2 | **YELLOW-GREEN** |
| #14 | Developer n8n Workflow Pack | 7/10 | 7/10 | 7/10 | Low-Med | Phase 2 | **YELLOW-GREEN** |
| #15 | AI IDE Team Rollout Guide | 8/10 | 9/10 | 7/10 | Medium | Phase 2-3 | **YELLOW-GREEN** |
| #11 | API Documentation Templates | 7/10 | 6/10 | 7/10 | Low | Phase 2 | **YELLOW-GREEN** |
| #12 | System Design Cheat Sheet Pack | 9/10 | 4/10 | 7/10 | Medium | Phase 3 | **YELLOW** |

---

## Key Strategic Insight from This Research

### The "5-Tool World" changes the product entirely

Previous research assumed 3 tools (Claude Code, Cursor, OpenCode).
New finding: there are now **5 standard AI coding config formats**:

```
CLAUDE.md     → Claude Code
.cursorrules  → Cursor
.windsurfrules → Windsurf
GEMINI.md     → Gemini CLI
AGENTS.md     → universal (all tools + Kiro + Copilot + Devin)
```

**60,000+ projects have adopted AGENTS.md** as the cross-tool standard.
No product packages all 5 formats for the same stack.

This reframes Product #1 from "AI IDE Config Bundle" to **"The Universal AI Coding Config Pack"** — the only product that works in every AI IDE. That's a meaningfully stronger headline.

### 3 Green products can be bundled into Phase 1 with near-zero extra effort

- **ADR Templates** (#16): BiG documents decisions he's already made. 1 afternoon.
- **Code Review Pack** (#17): Extend existing CLAUDE.md into review mode. 1 day.
- **Kiro Spec Templates** (#9): New tool, zero competition, AWS distribution. 2–3 days.

All three fit naturally into the Elite tier or as standalone products that cross-promote the main bundle.

---

*Sources: thenewstack.io (Kiro launch), dev.to (AI context management across tools), vibecoding.app (AGENTS.md guide), insightraider.com (146K Gumroad analysis), grizzlypeaksoftware.com (API docs case study), lockedinai.com (system design templates), ritz7.com (n8n monetization), digitalapplied.com (workflow templates revenue), NxCode (Cursor stats), github.com/google-gemini/gemini-cli*
