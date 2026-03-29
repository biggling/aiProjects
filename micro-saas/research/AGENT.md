# micro-saas — Research Agent

## Agent Instructions

1. **Read `## Known Facts` below first.** Do not re-research any fact already listed there.
2. Focus only on questions marked ❓ (unknown) or facts that may have changed since their `[date]`.
3. After saving findings, **update `## Known Facts`** — add new facts, update changed ones, remove stale ones.
4. Keep Known Facts concise: one line per fact, with date and source URL.

---

## Known Facts
<!-- Agent updates this section after each run. Date format: YYYY-MM-DD -->

### Opportunity Analysis
- **Vertical AI Agents**: Trend moving toward autonomous agents for specific B2B workflows like invoice reconciliation. [2026-03-23, Medium]
- **RegTech Gold Rush**: High demand for SMB tools for EU AI Act (Aug 2026) and ESG reporting (CA SB 253). [2026-03-24, Xpert Digital]
- **"Boring" Industry AI**: Care homes, tattoo studios, and HVAC are underserved; high demand for "Compliance-lite" niche agents. [2026-03-27, Search]
- **Webhook Safety Net**: High demand for managed webhook proxies (e.g., "HookSalvage") for solo devs. [2026-03-24, Synthesis]
- **Vertical Micro-SaaS Gap**: A $19–$49/mo "sweet spot" for tools solving hyper-specific problems (e.g., Solar Installers, HVAC). [2026-03-27, Reddit]
- **"The Seat Apocalypse"**: Shift from per-seat to Hybrid/Usage-Based models as AI reduces human headcount. [2026-03-25, Medium]

### Market Size & Growth
- **Freelancer Market**: Global market size projected at $1.5 trillion by 2026. [2026-03-23, Medium]
- **E-commerce Seller Tools**: Market size projected at $14.62 billion in 2026. [2026-03-23, Striking Alchemy]
- **TikTok Shop Scale**: 15M+ global active sellers; $66B projected GMV in 2026. [2026-03-23, EchoTik]
- **Micro-SaaS Market**: Projected to reach $60B by 2030, with 2026 favoring "headless" API-first tools. [2026-03-27, Search]

### Target Persona — E-commerce Sellers (Global)
- **Shopee Technical Fee**: 5% technology service fee effective February 1, 2026 for SG/MY/TH/VN all seller types including cross-border. [2026-03-27, BigSeller]
- **Shopee New Store Benefit**: 3-month commission-free program (Jan 1, 2026); covers SG/MY/TH/VN/PH/TW; cap 500 orders/month. [2026-03-27, Forest Shipping]
- **Shopee PH Penalties**: LSR threshold halved to 5%; Pre-order listing cap set at ≤5% with strict enforcement. [2026-03-26, Shopee.sg]
- **Shopee Penalty AI (v4.2)**: Seller Performance Policy v4.2 (March 2026): 83% of deductions from AI flagging; penalties trigger within 90 minutes; no real-time monitoring tool exists. [2026-03-27, Alibaba]
- **Shopee PIV**: Product Identity Verification mandatory for new listings in electronics, cosmetics, baby products, branded apparel. [2026-03-27, Shopee SG]
- **TikTok FBT Mandate**: Aggressive push for "Fulfilled by TikTok" in US; algorithm "punishing" non-FBT sellers with reach drops. [2026-03-27, YouTube/Reddit]
- **TikTok Semantic Audits**: Mandatory product attributes enforced March 20, 2026; AI suppresses listings with video-data conflicts. No third-party enrichment tool exists. [2026-03-27, CJDropshipping]
- **Etsy Semantic Search**: Transitioned to LLM-powered search in March 2026; prioritizes intent and AI visual photo verification. [2026-03-27, Gelato]

### Target Persona — Freelancers / Solo Devs (Global)
- **Pain Points**: Bloatware fatigue; high demand for "Apple Notes-like" minimalist invoicing tools. [2026-03-27, Reddit]
- **E-Invoicing Compliance**: Mandatory e-invoicing standards in 2026 creating "compliance headaches" for solo freelancers. [2026-03-27, Reddit]
- **Webhook Management**: `HookBytes` (Laravel 12) emerged as a lightweight alternative for solo dev monitoring. [2026-03-24, Reddit]

### Target Persona — SMB Owners (Global)
- **Pain Points**: AI "Token Shock" (unpredictable costs) and "Shadow AI" data leakage concerns. [2026-03-23, 2026 Trends]
- **EU AI Act Article 4**: Organizations must complete "AI Literacy" training for staff by Aug 2, 2026. [2026-03-27, Medium]

### Target Persona — Content Creators / Influencers (Global)
- **AI Content Repurposing**: High demand for tools turning one video into ten platform-specific formats automatically. [2026-03-27, Search]

### Thai SMB & Seller Pain Points
- **Shopee PH/MY/TH**: Local sellers crushed by 20% fees and China competition. [2026-03-23, Reddit]
- **Shopee Compliance**: `sender_real_name` now mandatory for Taiwan C2C order APIs. [2026-03-24, Shopee Open Platform]

### Pricing Models
- **Usage-Based Pricing**: 70% of B2B customers prefer per-transaction or outcome-based models over seat-based. [2026-03-24, Dashboardly]
- **Hybrid Gold Standard**: 51% of AI SaaS use a base fee + metered usage to balance MRR and expansion. [2026-03-25, Zylo]

### Webhook Tools Landscape
- **Hookdeck**: Dominant inbound webhook SaaS; $39/mo (1M req); expanded to outbound "Outpost" in 2026. [2026-03-27, Hookdeck]
- **Svix Pricing Gap**: $0 → $490/mo with no mid-tier; gap for 100K–500K msg/mo teams at $29–$99/mo. [2026-03-27, Svix]
- **Convoy**: MIT open-source, self-hosted, inbound + outbound on PostgreSQL. [2026-03-27, MagicBell]
- **LeanMQ**: New open-source Redis-based webhook replacement with DLQ/TTL. [2026-03-27, DEV Community]

### Alternative Ideas
- **Developer Utilities**: Webhook Dead-Letter Office, Env-to-Secret Sync, SQL-to-CSV Scheduler. [2026-03-23, 2026 Trends]
- **AI Invoice Negotiator**: Automated system for analyzing client payment history and proposing settlements. [2026-03-27, Reddit]
- **EU AI Act Article 4 SMB Tool**: Lightweight compliance tracker (training + audit trail + AI inventory) for EU SMBs; August 3, 2026 enforcement deadline; no micro-SaaS exists yet. [2026-03-27, EU AI Act]

### GTM — First 10 Customers
- **2026 Playbook**: Landing page (20+ signups) + 10–20 problem interviews + beta discount = validate before build. [2026-03-27, Superframeworks]
- **Channels that work**: Reddit "I built this" posts in niche subreddits; LinkedIn before/after posts; LTD pre-sales on AppSumo. [2026-03-27, Indie Hackers/Reddit]
- **2026 Indie Stack**: Lovable + Cursor + Supabase + Stripe = ship in days for $0–$50/month. [2026-03-27, TLDL]

---

## Context
Building a focused Micro-SaaS solving one boring problem deeply for a specific audience.
Target: $5-20/month subscription, 10 paying customers before adding features.
Target market: **global** — English-speaking, any timezone.
Top idea: e-commerce seller analytics (Shopee/multi-platform). Secondary: freelancer tools, developer utilities, SMB automation.

## Research Tasks
...
