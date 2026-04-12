# Digital Products — Market Feasibility & Research Summary

> **v2.0 updated 2026-04-05** — See full updated analysis: [findings/2026-04-05_market_feasibility_v2.md](findings/2026-04-05_market_feasibility_v2.md)
> v1.0 compiled 2026-03-29 from 11 research sessions (2026-03-22 to 2026-03-28)

## v2 Key Changes (April 2026)
- **Cursor IDE added** — $2B ARR, 2M users; .cursorrules packs = parallel opportunity to CLAUDE.md
- **Product #1 reframed** — "AI IDE Config Bundle" (CLAUDE.md + .cursorrules + AGENTS.md) → 10M+ developer TAM
- **AI prompt packs downgraded RED** — InsightRaider 146K analysis confirms 4.1% breakout rate; commodity trap confirmed
- **New #5 product** — Indie Hacker OS (Notion): dev-specific, premium pricing $37–$97
- **New #6 product** — Multi-Platform Revenue Tracker (Google Sheets): low effort, dogfood product
- **Blender addons** — Highest breakout rate but zero BiG skill fit; eliminated

---

---

## TL;DR Verdict

**GO. Ship the CLAUDE.md Config Pack within 1 week.**

All signals align: validated market, low competition, clear differentiation, zero inventory overhead, BiG's existing assets are ready to package.

---

## 1. Market Size (Confirmed Figures)

| Signal | Figure | Source |
|---|---|---|
| AI in Software Dev market CAGR | 42.3% → $15.7B by 2033 | Virtue Market Research |
| Claude Code run-rate growth | $500M (Sep 2025) → $2.5B (Feb 2026) — 5x in 5 months | Digiexe |
| Vibe coding market 2026 | $4.7B | Taskade |
| Developers using AI tools daily | 92% of US devs | Taskade |
| r/ClaudeCode subscribers | 96,000 (4,200+ weekly active) | aitooldiscovery.com |
| Claude user base | 35M+ users | Digiexe |
| #VibeCoding posts/month on X | 150,000+ | vibecoding.app |
| Digital products industry | $2.5T total, +70% transactions 2022–2024 | Whop |
| Gumroad Software Dev avg revenue/product | $60,814 per product total | insightraider.com |
| Claude Code users who are non-developers | 63% | secondtalent.com |

**Conclusion:** Market is large, fast-growing, and not slowing.

---

## 2. Competition Landscape — Evolution Over Time

### 2026-03-22: Near Zero Competition
- Zero paid CLAUDE.md template products found on Gumroad or Etsy
- Only Claude Code product: Substack paywall ($14.99/mo for "60 CLAUDE.md Templates")
- Free GitHub resources had 131K stars (system prompts repo) — unmet demand

### 2026-03-22 (Evening): First Competitors Confirmed
- **Builder Pack #2** (chongdashu) — closest competitor: workflow hacks, hooks, subagents, sample app
- **PM Operating System** ($49) — validates $49 price point for CLAUDE.md-centric product
- **Claude Code Generation Secrets** — PWYW guide
- **Claude Code Prompt Pack** (maxtendies) — 50+ prompts, PWYW
- **Gap still confirmed**: None offer stack-specific CLAUDE.md variants (Go, TS, Python, K8s, side-project)

### 2026-03-27: 8 Confirmed Active Sellers
- maxtendies, chongdashu, markkashef (×2), godsol, buildtolaunch, jimgle, digitalwealthwithsa
- Still no seller explicitly markets "CLAUDE.md Template Pack" as keyword — slot unclaimed

### 2026-03-28: Ecosystem Expansion
- Build with Claude marketplace: 494+ extensions (up from 101 a week prior)
- ECC (Everything Claude Code): 100K+ GitHub stars, free but unpackaged
- claudecodeagents.com: 60+ prompts, 230+ plugins — awareness growing
- **Etsy market for Claude Code configs still completely empty**

### Competition Risk Rating: **LOW-MEDIUM**
Competitors exist but none own the stack-specific CLAUDE.md angle. Market is in "validated early" phase (not yet commoditized like n8n packs).

---

## 3. Product Opportunities — Ranked by Feasibility

### #1 — CLAUDE.md Stack-Specific Config Pack
| Factor | Score | Notes |
|---|---|---|
| Market demand | 9/10 | r/ClaudeCode confirms demand constantly |
| Competition | 8/10 | 8 sellers exist but none own this keyword |
| BiG's moat | 10/10 | Real Go/Java/Python/K8s/microservices experience |
| Build effort | High | 2–4 days to build 5 stack variants |
| Price ceiling | $27–$49 | PM OS validated $49, $27 "sweet spot" |
| Revenue potential | Medium | Template ceiling ~$10K/mo without audience |
| Time to first sale | ~1 week | Package existing CLAUDE.md + create listing |

**Feasibility: GREEN LIGHT — Build first, ship this week**

Differentiation: Go monorepo + TypeScript strict + Python ML + microservices/K8s + solo side-project. No competitor has stack-specific depth. BiG's engineering background (10 years) is the moat.

---

### #2 — Claude Code Memory OS (Memory Bank Pattern)
| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Memory Bank is 2026 gold standard |
| Competition | 9/10 | Zero paid Memory Bank products confirmed |
| Build effort | Medium | 1–2 days on top of Config Pack |
| Price ceiling | $37–$49 | Position as premium "turnkey" |
| First-mover value | High | No one has productized this yet |

**Feasibility: GREEN LIGHT — Bundle into Config Pack as tier upgrade**

Include: CLAUDE.md + memory-bank/ templates (projectBrief.md, activeContext.md, progress.md) + hooks + setup script.

---

### #3 — Auto Mode & Multi-Agent Config Pack
| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | Auto Mode launched March 25 — knowledge gap exists NOW |
| Competition | 9/10 | Zero dedicated Auto Mode config products |
| Build effort | Medium | 2–3 days |
| Price ceiling | $37–$49 | "AI Infrastructure" framing justifies premium |
| Time-sensitivity | High | Early mover window is now (March/April 2026) |

**Feasibility: GREEN LIGHT — Add to Config Pack Pro tier**

Include: `.claude/auto-mode-trusted.json` safety profiles, multi-agent conductor SKILL.md, hard-lock constraints, concurrency safety.

---

### #4 — AI Developer Prompt Pack
| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | Validated by maxtendies PWYW |
| Competition | 5/10 | 4+ competitors selling 50+ prompt packs |
| Build effort | Low | 1–2 days |
| Price ceiling | $15–$29 | Generic prompts have ceiling |
| Commoditization risk | High | n8n shows this path leads to $10 flooding |

**Feasibility: YELLOW — Build as Phase 2 bundle add-on, not standalone**

---

### #5 — Notion Side Project Dashboard (Etsy)
| Factor | Score | Notes |
|---|---|---|
| Market demand | 6/10 | Etsy Notion templates sell well broadly |
| Competition | 7/10 | Low competition for dev-specific Notion templates |
| Build effort | Medium | 2–3 days |
| Price ceiling | $15–$29 | Etsy template norm |
| Platform fit | High | Etsy is better than Gumroad for this |

**Feasibility: YELLOW — Phase 3, not priority now**

---

### #6 — Cross-Platform AGENTS.md Pack (OpenCode)
| Factor | Score | Notes |
|---|---|---|
| Market demand | 8/10 | OpenCode 120K stars, 5M users/month |
| Competition | 9/10 | Near-zero cross-platform config packs |
| Build effort | Low | Add AGENTS.md alongside CLAUDE.md — incremental |
| TAM expansion | Very High | 5M+ OpenCode users vs Claude Code's market |

**Feasibility: GREEN LIGHT — Low effort add-on to Config Pack, do in Phase 1**

---

### #7 — Non-Developer Claude Code Pack ("for Designers")
| Factor | Score | Notes |
|---|---|---|
| Market demand | 7/10 | aidesignlab validated this segment |
| Competition | 8/10 | Only 1 competitor (aidesignlab course) |
| BiG's fit | 4/10 | BiG is a developer — this is less authentic |
| Build effort | Medium | Separate product, different framing |

**Feasibility: YELLOW — Validated but lower authenticity fit for BiG**

---

## 4. Platform Comparison

| Factor | Gumroad | Etsy | Lemon Squeezy |
|---|---|---|---|
| Fees | 10% + $0.50 + 2.9%+$0.30 | 6.5% + $0.20/listing | 5% + $0.50 |
| Target audience | Developer-adjacent | Broader consumer | Developer-adjacent |
| Claude Code competition | 8+ sellers | 1 confirmed listing | Unknown |
| Discovery speed | Slow (4–6 months SEO) | Moderate | Slow |
| Launch channel | r/ClaudeCode, HN, X | Etsy search | — |
| VAT handling | Full Merchant of Record (2026) | Handled by Etsy | Handled by LS |
| Best for | Dev tools, digital downloads | Planners, templates, visual | High-volume, lower fees |

**Recommendation:** Launch on Gumroad first (developer audience), then Etsy for the Notion/planner products. Evaluate Lemon Squeezy migration after 100+ sales.

---

## 5. Pricing Strategy (Data-Backed)

| Insight | Data |
|---|---|
| Highest paid breakout rate price band | $25–$50 (2.57% breakout) |
| PWYW conversion rate | 46% (vs 7% fixed price) |
| PWYW vs fixed revenue | Fixed earns $66.77/unit avg vs PWYW $18.74 |
| 70% of buyers choose mid-tier | Bundle tier is real revenue driver |
| Buyers who pay above PWYW suggested | 20% voluntarily pay above suggestion |

**Evolution of recommended strategy across research:**
- Mar 22: PWYW at $0 with $27 suggested → collect reviews → switch to fixed $27
- Mar 27: **Revised** — Launch at $15–$19 FIXED (not PWYW); PWYW dramatically undercuts revenue
- Mar 27: Raise to $25–$29 after 10 sales

**Final recommended pricing:**
| Tier | Price | Contents |
|---|---|---|
| Starter | $19 | 3 CLAUDE.md stacks + basic hooks |
| Pro | $37 | 5 stacks + Memory OS + hooks + skills + auto-mode |
| Elite | $97 | Everything + Notion dashboard + cross-platform + 1M context variant |

---

## 6. Customer Personas

### Primary: "Solo-Corn Sam"
- Senior dev / SaaS founder, 18–34
- Pays $100–$200/mo for Claude Max
- Pain: context rot, high token bills, repeated architecture explanations
- Triggers: saves 2-4h setup time, reduces token waste by 40%
- Discovery: r/ClaudeCode → X → HN → Product Hunt
- Price sensitivity: LOW (tool budget already large)

### Secondary: "Team Lead Taylor"
- Sets up Claude Code for 2–20 person dev team
- Needs: consistency across team, governance profiles, safety configs
- Price: $97–$197 team license
- Buying: company expense, needs ROI justification

### Anti-Persona: "Free-First Freddy"
- Uses aitmpl.com, GitHub repos, never pays
- Not worth targeting — answer "why not free?" in listing copy to self-select him out

### Emerging: Non-Developer (63% of Claude Code users)
- Growth marketers, designers, non-technical founders
- Validated by aidesignlab "Claude Code for Designers" course
- Separate product opportunity, not primary target now

---

## 7. Key Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Revenue concentration — top 1% earn 99.5% | HIGH | External audience strategy (Reddit, X, HN); don't rely on Gumroad Discover |
| Free ecosystem (aitmpl.com 1000+ free) | MEDIUM | Differentiate on curation, stack-specificity, polish, documented rationale |
| Market commoditization (n8n pattern) | MEDIUM | Focus on Engineering Standard positioning, not volume |
| Claude Code API changes break configs | LOW | "Living document" framing; promise quarterly updates |
| Low sales without existing audience | HIGH | Launch post strategy (r/ClaudeCode + HN + X same day) |
| PWYW revenue loss | MEDIUM | Use fixed pricing from launch; PWYW only for lead magnets |

---

## 8. Go-to-Market Sequence

### Week 1 (Now)
1. Package existing CLAUDE.md + hooks into Config Pack ZIP
2. Add AGENTS.md cross-platform variant (OpenCode — low effort)
3. Create Gumroad listing at $19 fixed, raise to $29 after 10 sales
4. Write launch post for r/ClaudeCode (educational angle, not sales pitch)
5. Post to r/vibecoding, IndieHackers, HN Show HN on same day

### Week 2–3
6. Add Memory OS tier ($37 Pro) based on launch feedback
7. Add Auto Mode safety profiles + MAC skill
8. Record 15–30s screen recording for Etsy thumbnail (dwell time signal)
9. Create Etsy listing for Notion Side Project Dashboard

### Month 2
10. Build Notion dashboard template
11. Cross-promote with youtube-content project tutorials
12. Document first revenue milestone (first to do so = own the story)

---

## 9. Sentiment Trend Across All Sessions

| Date | Sentiment | Key Reason |
|---|---|---|
| 2026-03-22 (AM) | Bullish / Opportunity | Near-zero competition, massive demand signal |
| 2026-03-22 (PM) | Bullish / Opportunity | Competition emerged but differentiation gap confirmed |
| 2026-03-23 | Opportunity | Memory Bank angle confirmed as gap |
| 2026-03-24 (AM) | Opportunity | Etsy slot empty, Memory Bank zero paid competition |
| 2026-03-24 (PM) | Bullish | "Prompt Contracts" framing enables higher prices |
| 2026-03-25 | Strongly Bullish | Auto Mode launch creates knowledge gap NOW |
| 2026-03-26 (AM+PM) | Opportunity | Auto Mode safety profiles standardizing |
| 2026-03-27 (AM) | Opportunity | CLAUDE.md keyword unclaimed on Gumroad/Etsy |
| 2026-03-27 (PM) | Opportunity | New hooks + plugin infra = fresh differentiation |
| 2026-03-28 | Opportunity | Marketplace doubled, OpenCode TAM, MoR removes friction |

**Overall trend: Consistently Bullish / Opportunity across all 11 sessions. No red flags found.**

---

## 10. Final Feasibility Scores

> v2 updated rankings — see [findings/2026-04-05_market_feasibility_v2.md](findings/2026-04-05_market_feasibility_v2.md) for full analysis

| Rank | Product | Market Demand | Competition | BiG's Moat | Revenue Potential | Phase | Feasibility |
|---|---|---|---|---|---|---|---|
| #1 | AI IDE Config Bundle (CLAUDE.md + .cursorrules + AGENTS.md) | 9/10 | 9/10 (zero) | 9/10 | $1K–10K/mo | Phase 1 | **GREEN** |
| #2 | Memory OS add-on | 8/10 | 9/10 (zero) | 9/10 | Bundle upsell | Phase 1 | **GREEN** |
| #3 | Auto Mode safety profiles | 8/10 | 9/10 (zero) | 8/10 | Pro tier | Phase 1 | **GREEN** |
| #4 | Cursor Rules Pack (.cursorrules) | 9/10 | 8/10 (low) | 9/10 | TAM expansion | Phase 1 | **GREEN** |
| #5 | Indie Hacker OS (Notion template) | 7/10 | 7/10 | 7/10 | $200–2K/mo | Phase 2 | **YELLOW-GREEN** |
| #6 | Multi-Platform Revenue Tracker (Sheets) | 7/10 | 7/10 | 8/10 | Bundle add-on | Phase 2 | **YELLOW-GREEN** |
| #7 | Non-Dev Claude Code Pack | 7/10 | 8/10 (low) | 4/10 | Separate audience | Phase 3 | **YELLOW** |
| #8 | AI Prompt Pack (standalone) | 5/10 | 3/10 (saturated) | 6/10 | Commodity | Never | **RED** |
| #9 | Generic n8n/automation packs | 5/10 | 2/10 (saturated) | 5/10 | Low ceiling | Never | **RED** |
| #10 | Blender Add-ons | 10/10 | 9/10 | 0/10 | $2.2B but N/A | Never | **RED (no skill)** |
