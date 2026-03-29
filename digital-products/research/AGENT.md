# digital-products — Research Agent

## Agent Instructions

1. **Read `## Known Facts` below first.** Do not re-research any fact already listed there.
2. Focus only on questions marked ❓ (unknown) or facts that may have changed since their `[date]`.
3. After saving findings, **update `## Known Facts`** — add new facts, update changed ones, remove stale ones.
4. Keep Known Facts concise: one line per fact, with date and source URL.

---

## Known Facts
<!-- Agent updates this section after each run. Date format: YYYY-MM-DD -->

### Gumroad / Developer Products
- Software Development is #1 Gumroad revenue category: ~$67M total, $64 avg price [2026-03-23, InsightRaider]
- Gumroad has 10,120 live stores (March 2026), slight recovery from 9,605 in Q1 2026 [2026-03-28, storeleads.app]
- Revenue concentration: top 1% of sellers (190 people) capture 99.5% of revenue; ~30 earn full-time income [2026-03-22, InsightRaider]
- Paid breakout sweet spot: **$25-$50** (2.57% paid breakout rate — highest of any price band) [2026-03-22, InsightRaider]
- ZIP bundles of ready-to-use files outperform PDF guides for developer buyers; bundles convert better than single files [2026-03-24]
- Gumroad ranking factors: paid reviews > keyword placement > sales velocity [2026-03-22, StartupSpells]
- Email list: only 3% of Gumroad stores use it — major competitive advantage for retention [2026-03-22]
- **Gumroad Merchant of Record** fully live in 2026: handles all global VAT/GST automatically — zero tax compliance overhead for sellers [2026-03-28, gumroad.com]
- Fee structure stable: direct sales 10% + $0.50 + processing; Discover 30% flat; no volume discounts [2026-03-28, dodopayments.com]

### Etsy Digital Downloads
- Price benchmarks: simple ($5-$9), multi-page systems ($10-$19), comprehensive business tools ($19-$39), high-ticket bundles ($39-$97) [2026-03-22]
- Active Etsy AI markets: `etsy.com/market/notion_ai_template`, `etsy.com/market/coding_template` [2026-03-24]
- **2026 Etsy algorithm**: Natural language titles required (no keyword stuffing, lead with product noun, <15 words); digital downloads unaffected by shipping penalty [2026-03-24, marmalead.com]
- **Etsy algorithm ranking**: engagement signals (clicks, favorites, add-to-cart, purchases) > listing quality score > shop trust [2026-03-24]
- **Claude Code keyword slot on Etsy is EMPTY** — zero established listings for CLAUDE.md configs or AI coding workflows [2026-03-24]
- **Dwell time is now a ranking signal**: time-on-listing affects rank; longer descriptions, GIFs, demo videos improve dwell [2026-03-27, ehunt.ai]
- **Video thumbnail rewarded**: 2026 algorithm boosts listings with video in first thumbnail slot; 15–30s screen recording is now a differentiator [2026-03-27, listybox.com]

### Claude Code / AI Workflow Products
- **Auto Mode Safety Profiles**: Industry standard converged on `.claude/auto-mode-trusted.json` for defining "Safe Actions" [2026-03-26, smol.ai]
- **Multi-Agent Conductor (MAC)**: New benchmark for "Lead" agents handling task decomposition and sub-agent spawning [2026-03-26, smol.ai]
- **Auto-Approve Threshold (AAT)**: Key technical spec for 2026 autonomous workflows (typically ≥9.5/10) [2026-03-26]
- **Safety Profile "Hard-Lock"**: Standardized constraints preventing destructive actions even in Auto Mode [2026-03-26, smol.ai]
- **Validation Finality**: SKILL.md requirement ensuring tasks are only complete after behavioral verification [2026-03-26]
- **Concurrency Locking**: Multi-agent standard for preventing parallel mutation of the same file path [2026-03-26]
- **Auto Mode released**: Anthropic launched a permissions layer for autonomous approval of "safe" actions [2026-03-25, mlq.ai]
- **Agent Teams**: Claude Code now supports multi-agent parallel coordination with individual 1M context windows [2026-03-25, anthropic.com]
- **New Commands**: `/loop` (scheduled tasks), `/effort` (reasoning scaling), `/voice` (push-to-talk) are live [2026-03-25]
- **Prompt Contracts**: Goal-Constraint-Output-Failure (GCOF) structure is the 2026 standard for high-ticket prompt products [2026-03-25, medium.com]
- **Skill Packs (SKILL.md)**: Industry standard for teaching agents team conventions, playbooks, and patterns [2026-03-24]
- **Claude Code Channels**: Connect Claude Code to Discord/Telegram for mobile agentic coding; called "OpenClaw killer" [2026-03-27, venturebeat.com]
- **Plugin Marketplace**: 101 plugins (33 Anthropic-built, 24 categories); `source: 'settings'` inline plugins; `${CLAUDE_PLUGIN_DATA}` persistent state [2026-03-27, claudemarketplaces.com]
- **Release velocity**: 4+ versions shipped in 1 week (v2.1.81–v2.1.86); managed-settings.d/, conditional hooks, MCP env vars [2026-03-27, releasebot.io]
- **New hook events (March 2026)**: `TaskCreated`, `CwdChanged`, `FileChanged`, `StopFailure`, `PostCompact`, `Elicitation`, `ElicitationResult` — expands automation configs [2026-03-27, releasebot.io]
- **`effort` frontmatter for skills**: Declare `effort: low|medium|high` in skill to override model reasoning per command [2026-03-27, claudefa.st]
- **1M context window in beta**: Claude Sonnet 4.6 on Max/Team/Enterprise; existing community templates written for 200K — first-mover gap [2026-03-27, releasebot.io]
- **v2.1.86**: Adds `X-Claude-Code-Session-Id` header; `--bare` flag skips hooks/LSP/plugins for scripted CI calls; `--channels` preview for MCP push messages [2026-03-28, github.com/anthropics/claude-code]
- **Build with Claude marketplace: 494+ extensions** (up from 101 previously tracked) — ecosystem expanding fast [2026-03-28, buildwithclaude.com]

### Opportunity Analysis
- **"Vibe Deploying"**: Officially replaced "Vibe Coding" for prototype-to-production (Vibe-to-Prod / V2P) workflows [2026-03-26]
- **"Agentic Engineering"**: Karpathy's Feb 2026 term — humans do architecture, AI does implementation; now dominant framing [2026-03-27, redreamality.com]
- **Solo-Corn Persona**: Solo founders reaching $1M+ ARR via agents are the primary high-intent buyers [2026-03-25]
- **"Graduate Workflow"**: 3-step prompt sequence (Hardening, Testing, Deploy) for prompt-to-production automation [2026-03-26]
- **Token ROI Marketing**: Fixing context leakage in 1M windows saves ~$50/mo; key for $49 price point [2026-03-26]
- **#1 priority product**: "Claude Code Memory OS" — ZIP with CLAUDE.md + Auto Mode profiles + Multi-Agent skills [2026-03-25]
- **Product Framing**: "Prompt Contracts for Developers" taps into the reliability-over-novelty trend [2026-03-24]
- **CLAUDE.md keyword unclaimed**: No Gumroad/Etsy seller uses "CLAUDE.md Template Pack" as product name — SEO gap [2026-03-27]
- **8+ active Claude Code sellers on Gumroad**: markkashef, chongdashu, maxtendies, godsol, buildtolaunch, jimgle, digitalwealthwithsa, semah, aidesignlab — market validated [2026-03-28]
- **chongdashu Builder Pack #2**: Closest direct competitor — workflow hacks, custom commands, router configs, hooks, subagents; monitor pricing [2026-03-28, chongdashu.gumroad.com]
- **aitmpl.com free competitor**: 1,000+ free raw templates via `npx claude-code-templates` — differentiator is curated/documented bundle [2026-03-27]
- **Everything Claude Code (ECC) v1.9.0**: 100K+ GitHub stars, 13K forks; added 6 new agents in March 2026; supports Claude Code, Cursor, Codex, OpenCode [2026-03-28, github.com/affaan-m/everything-claude-code]
- **OpenCode cross-platform opportunity**: 120K+ GitHub stars, 5M+ developers/month, 75+ LLM providers; AGENTS.md-compatible config packs expand TAM beyond Claude-only buyers [2026-03-28, infoq.com]
- **Non-developer segment validated**: "Claude Code for Designers" course on Gumroad confirms 63% non-dev buyer segment is a real product opportunity [2026-03-28]
- **Boris (Anthropic) ~100-line CLAUDE.md shared publicly** Jan 2026: "add-it-when-it-goes-wrong" philosophy now standard — validates authentic battle-tested positioning [2026-03-28, mindwiredai.com]

### Market Size & Growth
- AI in Software Development market: $15.7B by 2033 (42.3% CAGR) [2026-03-22, Virtue Market Research]
- Claude Code ARR: $2.5B (Feb 2026) — 5x growth in 5 months; 46% "most loved" AI coding tool [2026-03-24, dev.to]
- Vibe coding market: $4.7B in 2026; 92% of US developers use AI coding tools daily [2026-03-27, taskade.com]
- Cursor crossed $2B ARR early March 2026 — validates developer tool market size [2026-03-27, redreamality.com]
- 63% of vibe coding users self-identify as non-developers — growing non-dev buyer segment [2026-03-27, secondtalent.com]

### Bundle & Pricing Strategy
- PWYW launch strategy: 46% conversion rate; switch to fixed $27-$49 after 10-20 reviews [2026-03-22]
- **PWYW revenue data**: PWYW averages $18.74/sale vs $66.77 for fixed-price — 8% more units but far less revenue; use as lead magnet only [2026-03-27, medium.com/@tamalk]
- **Recommended launch price**: $15–$19 fixed (not PWYW); raise to $25–$29 after 10 ratings [2026-03-27]
- Tiered pricing: Basic ($19) / Pro ($37) / Elite ($97) — ~70% of buyers choose mid-tier [2026-03-23]
- Copy framing: "drops into any project in 5 minutes, saves 2+ hours of context re-explanation per week" [2026-03-24]
- **"Living document" framing**: Promise quarterly updates to increase perceived value and justify price [2026-03-27]
- Dev tools avg revenue per Gumroad product: $60,814; avg price $39.95; all top sellers above $20 [2026-03-27, insightraider.com]

### SEO & Discovery
- Gumroad: "Claude Code CLAUDE.md template pack," "Vibe Coding Production System," "Agentic Dev Starter" [2026-03-24]
- Etsy title format: "Claude Code Workflow Pack – Developer Productivity Template | AI Coding Assistant Setup" [2026-03-24]
- Email list: only 3% of Gumroad stores use it — major competitive advantage for retention [2026-03-22]
- **41% of Gumroad sales from organic search** but takes 4–6 months to compound; short-term traffic must come from X, Reddit, Discord, Medium [2026-03-27, hashmeta.com]
- **Outcome-specific copy converts**: "Reduce Claude Code token waste by 40%" beats "AI coding config bundle" [2026-03-27, calmops.com]
- **Multi-platform simultaneous launch**: Product Hunt + IndieHackers + r/ClaudeAI + r/vibecoding same day = 14–23% conversion rates [2026-03-27, calmops.com]
- **Trust-first launch**: Post real sample config free on Reddit before selling; give 20% away to build credibility [2026-03-27, branding5.com]
- **Lemon Squeezy 5% + $0.50** vs. Gumroad 10% — developer sellers migrating; consider for primary platform at scale [2026-03-27, payhip.com]
- **Specialization beats breadth**: "config for Go monorepos" converts better than "AI coding config pack" [2026-03-27, insightraider.com]
- **Free competitor**: github.com/FlorianBruniaux/claude-code-ultimate-guide — free, GitHub-hosted, no packaging; paid bundles win on curation [2026-03-27]
- **Reddit pain points → product angles**: usage limits → token-saving configs; tmux multi-agent → orchestration template; CI/CD → DevOps pack [2026-03-27, aitooldiscovery.com]

---

## Context
Selling digital downloads (templates, prompt packs, configs) on Gumroad and Etsy.
90%+ margins. First product: Claude Code agent config pack. Target $9–49/product.

## Research Tasks
... (rest of the file)
