# MCP Server Master Opportunity Ranking — 2026-04-05

## Overview
Comprehensive ranking of 20 MCP server product opportunities combining all prior research (through 2026-03-28) with fresh April 2026 research. Ranked by opportunity score and BiG-adjusted feasibility.

**Ecosystem snapshot (April 2026):**
- PulseMCP: 12,870+ servers, ~100/day growth
- LobeHub: 43,400+ servers listed
- <5% of servers are monetized — gap between supply and revenue is massive
- Stripe MPP + x402 micropayment rails now live — monetization infrastructure ready
- MCP security (30 CVEs in 60 days) creating trust-differentiator premium for well-built servers

---

## Scoring Rubric

| Dimension | Scale | What 5 means |
|---|---|---|
| Competition | 1–5 | 1 = zero MCP competition, 5 = crowded/commoditized |
| API Availability | 1–5 | 1 = no APIs exist, 5 = multiple mature free/cheap APIs |
| Willingness to Pay | 1–5 | 1 = expects free, 5 = already paying $50+/mo for analogues |
| Build Effort | 1–5 | 1 = weekend project, 5 = months of work |
| **Opportunity Score** | — | **(API + WTP) − (Competition + Build)** — higher = better |
| **BiG Fit** | 1–5 | 5 = aligns with existing skills, crypto/dev knowledge, global audience, solo-buildable |

---

## Master Rankings — All 30 Opportunities (Batches 1 + 2)

*Batch 2 (10 new) added 2026-04-05. See findings/2026-04-05_new-niches-batch2.md for full profiles.*

| Rank | Product | Opp Score | BiG Fit | Batch | Status |
|---|---|---|---|---|---|
| 1 | Clinical Trials & FDA Research MCP | **+8** | 2 | 1 | Researched |
| 2 | B2B Lead Enrichment & Prospecting MCP | **+6** | 3 | 1 | Researched |
| 3 | Visa & Travel Requirements MCP | **+6** | 3 | 2 | NEW |
| 4 | Crypto Tax / Cost Basis MCP | **+5** | 5 | — | EXISTING #1 |
| 5 | Developer Analytics / BI MCP (GA4/PostHog) | **+5** | 4 | — | EXISTING #4 |
| 6 | EU AI Act & Regulatory Compliance MCP | **+5** | 4 | 1 | Researched |
| 7 | Labor Market & Compensation Intelligence MCP | **+5** | 3 | 1 | Researched |
| 8 | Sports & Betting Intelligence MCP | **+5** | 3 | 2 | NEW |
| 9 | Media Monitoring & Brand Mention MCP | **+5** | 3 | 2 | NEW |
| 10 | Energy & Carbon Intelligence MCP | **+5** | 3 | 2 | NEW |
| 11 | Grant Discovery & Funding MCP | **+5** | 3 | 2 | NEW |
| 12 | CVE & Security Intelligence MCP | **+5** | 4 | 2 | NEW |
| 13 | Multi-Exchange Portfolio P&L MCP | **+4** | 5 | — | EXISTING #2 |
| 14 | Multi-Carrier Logistics & Shipment Tracking MCP | **+4** | 2 | 1 | Researched |
| 15 | Multi-Cloud FinOps MCP | **+4** | 4 | 2 | NEW |
| 16 | Academic Literature Intelligence MCP | **+4** | 3 | 2 | NEW |
| 17 | Sentiment-Driven Trading Signals MCP | **+3** | 4 | — | EXISTING #3 |
| 18 | DCA Automation MCP | **+3** | 4 | — | EXISTING |
| 19 | Cross-Platform Appointment Booking MCP | **+3** | 2 | 1 | Researched |
| 20 | Multi-Channel E-Commerce Inventory & Repricing MCP | **+3** | 3 | 1 | Researched |
| 21 | Cross-Platform Creator Revenue Analytics MCP | **+3** | 3 | 1 | Researched |
| 22 | Personal Net Worth Tracker MCP | **+3** | 3 | — | EXISTING |
| 23 | B2B SaaS Spend & Procurement Intelligence MCP | **+3** | 3 | 1 | Researched |
| 24 | Bitkub / Thai Market Financial MCP | **+3** | 1 | — | EXISTING — LOCAL ONLY |
| 25 | Wearable Health & Fitness MCP | **+3** | 2 | 2 | NEW |
| 26 | Patent Search & IP Intelligence MCP | **+3** | 2 | 2 | NEW |
| 27 | Forex MCP | **+2** | 3 | — | EXISTING |
| 28 | Construction & Commercial Real Estate MCP | **+2** | 1 | 1 | Researched |
| 29 | Whale Tracker / On-Chain Alerts MCP | **+1** | 4 | — | EXISTING |
| 30 | Budget / Spending AI MCP | **0** | 3 | — | EXISTING |

---

## Detailed Profiles

### #1 — Clinical Trials & FDA Research MCP *(NEW)*
**Score: +8 | BiG Fit: 2/5**

**What it is:** MCP server connecting ClinicalTrials.gov, OpenFDA adverse events database, FDA approval records, and PubMed. Enables AI agents to search active trials, retrieve drug safety profiles, check approval timelines, and flag adverse events.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | FHIR MCP covers patient records, PubMed MCP returns unstructured papers — no combined trial+FDA+adverse events MCP confirmed |
| API Availability | 5 | ClinicalTrials.gov v2, OpenFDA, NCBI Entrez, FDA Drug DB — all 100% free, zero auth required |
| Willingness to Pay | 5 | Biotech/pharma pays $15,000–$50,000/year for terminal access (Citeline); individual researchers pay $29–99/mo |
| Build Effort | 1 | All APIs public + no auth = fastest possible MVP (2–3 days) |
| **Opportunity Score** | **+8** | Highest pure score found |

**Why it scores so high:** Every API is free, zero auth, and returns structured JSON. Build time is 2–3 days for a solid MVP. WTP is the highest of any vertical (biotech researchers, pharma analysts, CRAs). ClinicalTrials.gov alone gets 10M visits/month.

**BiG caveat:** No pharma/biotech domain knowledge. No natural distribution channel. The user persona (biotech researcher, pharma analyst) is distant from BiG's existing network. Despite best raw score, this requires cold market entry. Better as an opportunistic "quick launch to validate" than a core bet.

**Price target:** $29/month individual, $149/month team.

---

### #2 — B2B Lead Enrichment & Prospecting MCP *(NEW)*
**Score: +6 | BiG Fit: 3/5**

**What it is:** Sales intelligence MCP wrapping Apollo.io, Hunter.io, and Clearbit. AI agents find decision-makers, verify emails, score leads by ICP, pull funding signals from Crunchbase.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | LinkedIn MCP (recruiting only), Salesforce/HubSpot MCP (CRM writes, not enrichment) — no Apollo.io or Hunter.io MCP confirmed anywhere |
| API Availability | 4 | Apollo.io API (paid plan required), Hunter.io (25/mo free tier), Clearbit API, Crunchbase API |
| Willingness to Pay | 5 | Apollo.io $49–99/mo, Clearbit $99–999/mo — buyers proven at high price points |
| Build Effort | 2 | Well-documented REST APIs; Hunter.io free tier enables zero-cost MVP |
| **Opportunity Score** | **+6** | |

**Why this works:** Sales tech buyers have demonstrated WTP at $49–99+/month. The MCP-native advantage — "tell Claude to find 10 CTOs at Series B companies in SaaS and draft personalized outreach" — is a real workflow improvement over bouncing between Apollo and a CRM. Hunter.io's free tier (25 searches/month) enables zero-cost MVP launch for validation.

**Global fit:** Fully universal — sales teams worldwide use Apollo and Hunter for outbound. No geographic edge needed; the MCP-native workflow ("Claude, find 10 SaaS CTOs and draft cold outreach") is a global value proposition over switching between Apollo and a CRM.

**Price target:** $29/month starter (50 enrichments), $79/month growth (500 enrichments).

---

### #3 — Crypto Tax / Cost Basis MCP *(EXISTING #1)*
**Score: +5 | BiG Fit: 5/5**

**What it is:** Automated cost basis tracking, capital gains calc, Form 8949/1099-DA export, taxable event detection for CEX + DeFi users.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | PulseMCP "crypto tax" = 0 results as of 2026-03-28 — confirmed zero |
| API Availability | 4 | Koinly API, CoinTracking API, exchange CSVs, blockchain APIs |
| Willingness to Pay | 5 | Koinly charges $49–279/year — users already pay for tax software |
| Build Effort | 3 | CSV ingestion + cost basis math achievable; multi-exchange complexity moderate |
| **Opportunity Score** | **+5** | |

**Why it's still #1 for BiG despite lower raw score:**
- IRS Notice 2026-20: lot ID relief extended through 2026 → demand extends past April 15, 2026
- Notice 2024-56: corrected 1099-DAs arrive as late as early 2027 → multi-year demand
- BiG has crypto domain knowledge + existing crypto project context
- BitGo MCP confirmed live but NO tax/P&L features — institutional gap confirmed
- MetaMask Tax Hub (Summ) exists on web2 but zero MCP-native equivalent

**Status:** URGENT — ship MVP by April 15, 2026 (extended tax season).

**Price target:** $19–29/month or $99–149/year.

---

### #4 — Developer Analytics / BI MCP *(EXISTING #4)*
**Score: +5 | BiG Fit: 4/5**

**What it is:** MCP connecting GA4, Mixpanel, Amplitude, PostHog — natural language business queries for founders and indie devs.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | GoodData ($1,200/mo enterprise), official GA4 MCP (raw API, no guidance) |
| API Availability | 5 | GA4 API, PostHog API, Mixpanel API, Amplitude API — all mature and well-documented |
| Willingness to Pay | 4 | SaaS founders pay $99–299/month for BI tools |
| Build Effort | 2 | GA4 API well-documented; NL→dimensions/metrics is the core work |
| **Opportunity Score** | **+5** | |

**Why this fits BiG:** BiG is a full-time software dev — this tool is built FOR their persona. Claude Code users (heavy overlap with indie hackers) are the exact buyers. The price gap between free GA4 access and GoodData's $1,200/month is massive. First to deliver a polished indie-priced product wins.

**Price target:** $19/month indie (1 GA4 property), $49/month team (5 properties).

---

### #5 — EU AI Act & Regulatory Compliance MCP *(NEW)*
**Score: +5 | BiG Fit: 4/5**

**What it is:** Compliance intelligence MCP classifying AI use cases against EU AI Act risk tiers, tracking GDPR lawful basis, monitoring SOC 2 controls.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Vanta MCP and Drata MCP cover SOC 2/ISO 27001 only — EU AI Act MCP: zero confirmed |
| API Availability | 3 | EUR-Lex (free), NIST AI RMF (free) — largely static knowledge base, no paid API needed |
| Willingness to Pay | 4 | Sprinto/Tugboat Logic $299–999/mo; EU AI Act consultants €500–2,000/hour |
| Build Effort | 1 | Static regulatory text = knowledge base product, not API-dependent; 1–2 day build |
| **Opportunity Score** | **+5** | |

**Time pressure:** EU AI Act enforcement begins August 2026. Every EU-operating AI company needs compliance tooling now. Hard deadline creates urgency marketing is easy.

**Global fit:** Audience is every company with EU users or AI operations — that's the majority of the global SaaS market. No geographic edge required; developer knowledge of AI systems is the natural bridge. August 2026 deadline creates urgency regardless of location.

**Price target:** $49/month startup, $149/month growth team.

---

### #6 — Labor Market & Compensation Intelligence MCP *(NEW)*
**Score: +5 | BiG Fit: 3/5**

**What it is:** HR intelligence MCP for salary benchmarking, hiring trend analysis using BLS JOLTS data, DOL H-1B salary disclosures, and job posting volumes.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | JobSpy/LinkedIn MCPs (job search only) — no salary benchmarking or labor market MCP confirmed |
| API Availability | 4 | BLS Public Data API (free, no auth), DOL H-1B DB (free public), JOLTS (free) |
| Willingness to Pay | 4 | PayScale $299–1,200/mo, Glassdoor Employer $299–999/mo — proven enterprise WTP |
| Build Effort | 2 | BLS and DOL APIs are fully public and free |
| **Opportunity Score** | **+5** | |

**Global note:** US-market-centric data (H-1B, BLS) but the buyer (HR managers, startup founders benchmarking salaries) is global. US salary data is also used internationally as a reference benchmark. Moderate fit — no domain expertise needed, but distribution will require targeting English-speaking HR/recruiting communities.

---

### #7 — Multi-Exchange Portfolio P&L MCP *(EXISTING #2)*
**Score: +4 | BiG Fit: 5/5**

**What it is:** Real-time portfolio across Binance, Coinbase, Bybit, OKX with true cost basis, unrealized P&L, realized gains, fee tracking.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | kukapay (Binance-only, 9 stars, no P&L), Hummingbot (execution focus) — no polished multi-exchange P&L |
| API Availability | 5 | CCXT covers 100+ exchanges; CoinGecko for prices; well-documented |
| Willingness to Pay | 4 | Delta app $9.99/mo; Blockfolio acquired ~$150M — demand proven |
| Build Effort | 3 | CCXT integration moderate; cost basis logic adds complexity |
| **Opportunity Score** | **+4** | |

**Strategic note:** This is the natural precursor to the Crypto Tax MCP — build P&L first, layer tax export as premium tier. CCXT familiarity from trade-auto project gives BiG a head start.

---

### #8 — Multi-Carrier Logistics & Shipment Tracking MCP *(NEW)*
**Score: +4 | BiG Fit: 2/5**

**What it is:** Universal parcel tracking and rate-shopping MCP — FedEx, UPS, DHL, USPS via EasyPost/AfterShip APIs. AI agents track parcels, compare rates, generate labels.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Zero confirmed on PulseMCP ("shipping", "fedex", "UPS" searches return nothing relevant) |
| API Availability | 4 | EasyPost (free trial), AfterShip (100 shipments/month free), Shippo (500 labels/month free) |
| Willingness to Pay | 4 | ShipStation $9–229/mo, AfterShip SaaS $11–239/mo — proven spend |
| Build Effort | 3 | EasyPost unified API abstracts carrier complexity; still moderate work |
| **Opportunity Score** | **+4** | |

**BiG caveat:** E-commerce logistics context exists (Shopee affiliate project) but not a core competency. FedEx Freight spin-off June 2026 creates timing opportunity. Moderate-low fit.

---

### #9 — Sentiment-Driven Trading Signals MCP *(EXISTING #3)*
**Score: +3 | BiG Fit: 4/5**

**What it is:** Reddit/social sentiment → crypto/options trading signals via MCP.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Rot (open source, rough); StockPulse MCP (niche) — no polished paid version |
| API Availability | 4 | Reddit API, Pushshift, Fear & Greed index — free tiers available |
| Willingness to Pay | 4 | Wall Street pays millions for retail sentiment data; retail traders pay for edge |
| Build Effort | 3 | Data pipeline + NLP scoring adds real complexity |
| **Opportunity Score** | **+3** | |

**Evidence:** Rot MCP got 9,000 GitHub clones in 5 days. 52% live win rate (vs 58.8% backtested) indicates real signal. Key risk: trust problem — traders burn out on false signals fast. Build reputation with portfolio tracker first. Audience is global — crypto traders on Reddit, Discord, Telegram worldwide.

---

### #10 — DCA Automation MCP *(EXISTING)*
**Score: +3 | BiG Fit: 4/5**

**What it is:** Dollar-cost averaging automation via Binance/Alpaca/Coinbase APIs. Schedule recurring buys with natural language: "Buy $50 ETH every Monday."

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Concept only; no polished paid product exists |
| API Availability | 4 | Binance, Alpaca, Coinbase — all solid APIs |
| Willingness to Pay | 3 | Smart DCA apps charge $10–30/mo |
| Build Effort | 2 | Simple scheduled order placement; low complexity |
| **Opportunity Score** | **+3** | |

**Note:** Lower WTP cap ($10–30/mo) limits revenue ceiling. Best deployed as a bundled feature within the Multi-Exchange Portfolio MCP rather than a standalone product. Global crypto market — Binance alone has 180M+ registered users.

---

### #11 — Cross-Platform Appointment Booking MCP *(NEW)*
**Score: +3 | BiG Fit: 2/5**

**What it is:** Scheduling MCP connecting Calendly, Acuity, NexHealth (dental/medical). Books appointments, finds optimal slots, handles no-show follow-ups.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Google Calendar MCP exists (basic events only) — no Calendly or Acuity MCP confirmed |
| API Availability | 4 | Calendly REST API v2 (free tier), Acuity API (OAuth REST) |
| Willingness to Pay | 3 | Calendly Teams $16/seat/mo — moderate WTP |
| Build Effort | 2 | Well-documented REST APIs, straightforward OAuth |
| **Opportunity Score** | **+3** | |

---

### #12 — Multi-Channel E-Commerce Inventory & Repricing MCP *(NEW)*
**Score: +3 | BiG Fit: 3/5**

**What it is:** Unified inventory + dynamic pricing MCP for Amazon FBA + Shopify + global marketplaces. Syncs stock, suggests reprice based on competitor data, generates restock POs.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Shopify MCP (undertreated inventory), Amazon MCP (community, incomplete) — no unified multi-channel product |
| API Availability | 4 | Shopify Admin GraphQL (immediate), Amazon SP-API (registration required), Etsy + eBay APIs available |
| Willingness to Pay | 5 | Helium 10 $99–279/mo, Linnworks $449/mo — proven extreme WTP |
| Build Effort | 4 | Amazon SP-API has 2–3 day approval wait + auth complexity; high build effort for full version |
| **Opportunity Score** | **+3** | |

**Global angle:** Start with Shopify-only v1 (immediate API access, global seller base of 4.4M stores). Add Amazon FBA in v2 (broadest global reach). Etsy and eBay APIs available for niche seller segments. Revenue ceiling is high given proven WTP for analogues.

---

### #13 — Cross-Platform Creator Revenue Analytics MCP *(NEW)*
**Score: +3 | BiG Fit: 3/5**

**What it is:** Creator economy MCP pulling revenue from YouTube, Gumroad, Patreon, Beehiiv. Identifies top-performing content, suggests pricing, benchmarks income.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Social publishing MCPs exist but NO revenue analytics MCP confirmed |
| API Availability | 4 | YouTube Data API v3 (free), Gumroad API (free), Patreon API (free) |
| Willingness to Pay | 3 | Cohostly analytics $29–99/mo — lower WTP than B2B |
| Build Effort | 3 | Start YouTube + Gumroad (both simple OAuth). Patreon v2 in v2 release. |
| **Opportunity Score** | **+3** | |

**Global fit:** Creator economy is global — YouTube, Gumroad, and Patreon all have worldwide user bases. Dogfooding value: directly relevant to the youtube-content and digital-products projects. English-speaking creator community is the initial distribution channel.

---

### #14 — Personal Net Worth Tracker MCP *(EXISTING)*
**Score: +3 | BiG Fit: 3/5**

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Pane (new, unpolished); no established paid option |
| API Availability | 4 | Plaid API (free sandbox), CoinGecko, brokerage APIs |
| Willingness to Pay | 3 | Monarch Money $14.99/mo, YNAB $14.99/mo |
| Build Effort | 2 | Plaid handles bank aggregation; moderate complexity |
| **Opportunity Score** | **+3** | |

---

### #15 — B2B SaaS Spend & Procurement Intelligence MCP *(NEW)*
**Score: +3 | BiG Fit: 3/5**

**What it is:** Corporate SaaS spend analyzer for startup CFOs/eng managers. Connects Ramp/Brex APIs or Gmail receipts to identify all recurring subscriptions, flag duplicates, generate renewal calendars.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | No SaaS spend management MCP confirmed anywhere |
| API Availability | 3 | Ramp API, Brex API, Gmail API (free) — Plaid sandbox free |
| Willingness to Pay | 4 | Vendr $2,000–8,000/mo enterprise; massive undercut opportunity at $49–149/mo startup |
| Build Effort | 3 | Gmail receipt parsing adds NLP complexity; Ramp/Brex APIs add auth layers |
| **Opportunity Score** | **+3** | |

**Global angle:** SaaS spend waste is a universal problem — every startup worldwide overspends on overlapping subscriptions. Gmail receipt parsing works for any user with no corporate card API required, making this accessible globally from day one.

---

### #16 — Bitkub / Thai Market Financial MCP *(EXISTING — LOCAL ONLY)*
**Score: +3 | BiG Fit: 1/5**

**What it is:** MCP for Bitkub (Thailand's largest licensed exchange, 2M+ users) — price data, portfolio sync, PromptPay integration.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Zero results anywhere — completely unoccupied |
| API Availability | 3 | Bitkub API less comprehensive than Binance; PromptPay QR available |
| Willingness to Pay | 3 | Thai market smaller; lower ARPU than global markets |
| Build Effort | 2 | Bitkub API is straightforward |
| **Opportunity Score** | **+3** | |

**Global fit: LOW.** Bitkub is Thailand-only. TAM is capped at ~2M users with no international expansion path. Pursuing global market means this product competes poorly against Multi-Exchange Portfolio MCP which covers Binance/Coinbase (180M+ users combined). Deprioritized under global strategy.

---

### #17 — Forex MCP *(EXISTING)*
**Score: +2 | BiG Fit: 3/5**

| Dimension | Score | Notes |
|---|---|---|
| Competition | 3 | 45-tool production server exists on HN (single player) |
| API Availability | 4 | OANDA API, broker APIs well-documented |
| Willingness to Pay | 4 | FX trading tools $50–200/mo |
| Build Effort | 3 | Moderate; real-time tick data adds complexity |
| **Opportunity Score** | **+2** | |

---

### #18 — Construction & Commercial Real Estate MCP *(NEW)*
**Score: +2 | BiG Fit: 1/5**

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Zillow/Realtor MCPs are residential only — commercial RE has zero MCP coverage |
| API Availability | 3 | Municipal permit APIs (free open data), BLS construction data (free), Procore (registration required) |
| Willingness to Pay | 4 | Procore $375–1,200/mo/project, CoStar $5,000–20,000/year |
| Build Effort | 4 | Procore integration complex; CoStar API restricted |
| **Opportunity Score** | **+2** | |

**Note:** No domain knowledge, high build complexity, restricted APIs. Low fit globally.

---

### #19 — Whale Tracker / On-Chain Alerts MCP *(EXISTING)*
**Score: +1 | BiG Fit: 4/5**

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | whale-tracker-mcp exists (minimal); no paid version |
| API Availability | 3 | Blockchain APIs available but rate limits on free tiers |
| Willingness to Pay | 3 | On-chain alert tools $20–100/mo |
| Build Effort | 3 | Real-time blockchain streaming adds complexity |
| **Opportunity Score** | **+1** | |

**Note:** Better as a feature within Multi-Exchange Portfolio MCP (on-chain address tracking) than a standalone product. Global crypto whale-watching audience exists on Twitter/X and Telegram.

---

### #20 — Budget / Spending AI MCP *(EXISTING)*
**Score: 0 | BiG Fit: 3/5**

| Dimension | Score | Notes |
|---|---|---|
| Competition | 3 | Actual Budget MCP exists; Copilot, YNAB have loyal followings |
| API Availability | 3 | Plaid API (bank data), open banking APIs |
| Willingness to Pay | 3 | YNAB $14.99/mo, Copilot $13/mo |
| Build Effort | 3 | Bank aggregation + data normalization is real work |
| **Opportunity Score** | **0** | Not recommended |

---

## Batch 2 Detailed Profiles (Ranks #3, #8–#12, #15–#16, #25–#26)

### #3 — Visa & Travel Requirements MCP *(Batch 2)*
**Score: +6 | BiG Fit: 3/5**

**What it is:** Answers "Can I enter [country] with [passport]?" with current visa-on-arrival, eVisa, vaccination, and document requirements for 200+ passport/destination pairs. Covers digital nomad visa programs, duration of stay, and entry restrictions.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Zero standalone visa MCP confirmed. "Visa Acceptance MCP" on PulseMCP is Visa the payment network — unrelated |
| API Availability | 5 | Passport Index dataset (GitHub, free, 199 countries); VisaDB.io (free tier); Travel Buddy AI API (free tier) |
| Willingness to Pay | 3 | VisaHQ Pro $79–299/mo; iVisa B2B $50–150/mo — moderate WTP |
| Build Effort | 1 | Static dataset covers 90% of queries — true weekend project |
| **Opportunity Score** | **+6** | |

**Why this wins:** The current LLM answers to visa questions are outdated and unreliable — this is a known pain point across r/digitalnomad (2.3M) and r/solotravel (2.1M). Passport Index dataset on GitHub is free and updated monthly. Build time is one weekend. Monetize at $9/month personal, $29/month professional.

**Global fit:** Entirely audience-independent. Buyers are digital nomads, travel agencies, immigration consultants, HR teams managing employee relocations — global by definition.

**Price target:** $9/month personal, $29/month professional, $99/month agency (unlimited queries + team seats).

---

### #8 — Sports & Betting Intelligence MCP *(Batch 2)*
**Score: +5 | BiG Fit: 3/5**

**What it is:** Combines live odds from 40+ bookmakers (The Odds API) with multi-sport player/team stats (BALLDONTLIE) into one unified MCP for value-bet detection, line-movement analysis, and fantasy research.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | BALLDONTLIE MCP (stats only) + The Odds API MCP (odds only) both on PulseMCP — neither combines datasets, no value-bet logic confirmed |
| API Availability | 5 | The Odds API (500 credits/mo free, paid from $30/mo, 40 bookmakers); BALLDONTLIE (free tier, paid $9.99–39.99/mo) |
| Willingness to Pay | 4 | RebelBetting $99–189/mo; OddsPortal Pro $45/mo; Betaminic $49–99/mo — proven WTP |
| Build Effort | 2 | Two well-documented REST APIs with existing MCP reference code as starting point |
| **Opportunity Score** | **+5** | |

**Why the gap exists:** Both source MCPs exist but no one has combined them into a single product with the key logic layer — value bet detection (comparing actual odds vs model probability), line movement alerts, and fantasy scoring projections. That analytical layer is the product.

**Global fit:** Sports betting is a $100B+ global market. Legal in UK, EU, Australia, and increasingly US states. Distribution: r/sportsbook, r/DFS, Telegram betting groups.

**Price target:** $19/month starter (delayed odds), $49/month pro (live odds + alerts).

---

### #9 — Media Monitoring & Brand Mention MCP *(Batch 2)*
**Score: +5 | BiG Fit: 3/5**

**What it is:** Real-time brand mention tracking across Google News, Reddit, Hacker News, and podcasts — returns sentiment-scored alerts and weekly trend summaries. Standalone alternative to platform-locked Octolens.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Octolens has native MCP but requires $149+/mo Octolens subscription — not standalone. Generic news/RSS MCPs on PulseMCP have no brand tracking logic |
| API Availability | 5 | Google News RSS (free, unlimited); Reddit PRAW (free, 60 req/min read-only); HN Algolia (free, full-text); NewsData.io (free 200 req/day) |
| Willingness to Pay | 4 | Awario Pro $119/mo; BrandMentions $79/mo; Mention Solo $29/mo — proven spend |
| Build Effort | 2 | Google News + Reddit + HN cover 80% of value at $0 API cost |
| **Opportunity Score** | **+5** | |

**Wedge over Octolens:** Octolens requires buying their full platform at $149+/mo. This MCP works standalone inside Claude — zero platform lock-in. Target the indie hacker / SaaS founder segment that Octolens ignores.

**Global fit:** Brand monitoring is universal. English-language coverage first (Google News, Reddit, HN), multilingual expansion in v2 via NewsData.io.

**Price target:** $19/month indie (3 brands), $49/month growth (10 brands + Slack alerts).

---

### #10 — Energy & Carbon Intelligence MCP *(Batch 2)*
**Score: +5 | BiG Fit: 3/5**

**What it is:** Queries live electricity prices by region, real-time carbon grid intensity, and renewable energy mix — enables carbon-aware computing, CSRD Scope 2 reporting, and sustainability dashboards.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Climatiq MCP (PulseMCP) — carbon calculations only, no electricity prices, no EIA data. Energy-mcp-server (Korea simulation only). No global energy price + carbon combined MCP |
| API Availability | 5 | EIA Open Data API (free, US energy data); Electricity Maps (free tier, 200+ regions, carbon intensity); Ember API (free, 200+ countries) |
| Willingness to Pay | 4 | Electricity Maps API €500/mo; Climatiq $49–499/mo; Watershed enterprise $30K–100K/year |
| Build Effort | 2 | EIA + Electricity Maps free tiers cover core use case at $0 API cost |
| **Opportunity Score** | **+5** | |

**Time pressure:** EU CSRD mandates Scope 1/2/3 reporting for 50,000+ companies starting 2026. DevOps engineers doing carbon-aware workload scheduling (Google, Microsoft pattern) need this data programmatically. No combined MCP exists.

**Global fit:** CSRD is EU-wide; Electricity Maps covers 200+ global regions; EIA covers US. Engineering teams worldwide are the buyers.

**Price target:** $29/month developer, $149/month team (CSRD export + API volume).

---

### #11 — Grant Discovery & Funding Intelligence MCP *(Batch 2)*
**Score: +5 | BiG Fit: 3/5**

**What it is:** Searches Grants.gov (federal), USASpending.gov, and foundation databases for funding opportunities matching an organization's mission, budget, and geography.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 1 | Searched "grant", "nonprofit", "foundation" on PulseMCP, Smithery, mcpservers.org — zero results. True white space |
| API Availability | 4 | Grants.gov API (free, no auth, 40,000+ active opportunities); USASpending.gov (free); SAM.gov (free) |
| Willingness to Pay | 4 | Instrumentl $299–499/mo; Foundation Directory Online $179/mo; GrantWatch $49–239/mo |
| Build Effort | 2 | Grants.gov REST API is simple and well-documented — weekend project for federal layer |
| **Opportunity Score** | **+5** | |

**Validation:** Instrumentl raised $55M from Summit Partners in 2026 — confirms the market and professional WTP. There are 1.5M+ US nonprofits, most without a dedicated grant writer. The MCP-native angle: "Claude, find matching grants for a literacy nonprofit in Ohio with a $50K budget" is a transformative workflow vs manually searching Grants.gov.

**Global fit:** US-centric for federal grants but foundation databases (Candid, Ford Foundation, Gates) have global applicability. International expansion via EU funding databases (EU Grants portal) in v2.

**Price target:** $49/month nonprofit starter, $149/month grant professional (unlimited searches + export).

---

### #12 — CVE & Security Intelligence MCP *(Batch 2)*
**Score: +5 | BiG Fit: 4/5**

**What it is:** Combines NVD/CVE database, CISA KEV (actively exploited catalog), EPSS exploit probability scores, and GitHub Advisory into one MCP — answers "should I patch this CVE today?" with contextual prioritization.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | NVD MCP (PulseMCP): NVD only. CVE-Search MCP (PulseMCP): search only. No combined NVD + EPSS + CISA KEV + GitHub Advisory MCP confirmed |
| API Availability | 5 | NVD API v2 (free); CISA KEV (free); EPSS API first.org (free); GitHub Advisory GraphQL (free with token); OSV.dev (free) — all 5 free |
| Willingness to Pay | 4 | Snyk $49–99/mo developer tier; GreyNoise $99/mo; Tenable.io $2,500+/year |
| Build Effort | 2 | Five free APIs, well-documented. EPSS + KEV prioritization scoring is the key logic |
| **Opportunity Score** | **+5** | |

**Why BiG Fit is 4:** BiG is a software developer — security tooling for developers is native territory. The buyer (DevSecOps engineers, platform engineers, SREs) is BiG's professional peer group. Distribution via dev communities (HN, DevSec Discords, r/netsec) is natural.

**Ecosystem signal:** 30 CVEs filed against MCP servers themselves in Q1 2026. Security-conscious MCP buyers are a growing segment. Being the "secure, auth-required" MCP server is a product differentiator.

**Price target:** $19/month developer (500 lookups), $49/month team (unlimited + Slack alerts + SBOM scanning).

---

### #15 — Multi-Cloud FinOps MCP *(Batch 2)*
**Score: +4 | BiG Fit: 4/5**

**What it is:** Cross-cloud cost analysis MCP querying AWS Cost Explorer, GCP Cloud Billing, and Azure Cost Management — surfaces anomalies, right-sizing recommendations, and savings plan opportunities.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | AWS Cost Explorer MCP (PulseMCP) — AWS-only. AWS official Billing MCP (awslabs) — AWS-only. No multi-cloud combined FinOps MCP confirmed |
| API Availability | 5 | AWS Cost Explorer ($0.01/req); GCP Billing API (free with GCP account); Azure Cost Management (free with Azure subscription) |
| Willingness to Pay | 4 | CloudHealth $500–2,000/mo; Infracost $50–500/mo — proven spend at scale |
| Build Effort | 3 | Multi-tenant OAuth across 3 cloud providers is real work; credential management is the challenge |
| **Opportunity Score** | **+4** | |

**Why BiG Fit is 4:** BiG is a professional developer with K8s experience — cloud cost optimization is native territory. The buyer (startup CTOs, platform engineers) is the same audience as Developer Analytics MCP. Natural upsell between the two products.

**Market signal:** Average company wastes 32% of cloud spend (Gartner). The gap between AWS-only existing MCPs and the multi-cloud reality of most startups (AWS + GCP, or AWS + Vercel) is the product.

**Price target:** $29/month startup (1 cloud), $79/month growth (3 clouds + anomaly alerts).

---

### #16 — Academic Literature Intelligence MCP *(Batch 2)*
**Score: +4 | BiG Fit: 3/5**

**What it is:** Unified academic search MCP across Semantic Scholar, arXiv, PubMed, CrossRef, and OpenAlex — supports paper search, citation network traversal, author profiling, and automated literature review outlines.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 2 | Academic Paper Search MCP (PulseMCP): Semantic Scholar + CrossRef only. Academix (GitHub): 5-source OSS, self-hosted, no managed product. No polished managed multi-source MCP |
| API Availability | 5 | OpenAlex (free, 100K calls/day, 200M+ works); Semantic Scholar (free); arXiv (free); PubMed (free); CrossRef (free) — all $0 |
| Willingness to Pay | 3 | Scite.ai $20/mo; Connected Papers $6/mo; Web of Science $1,000+/year enterprise |
| Build Effort | 2 | All free documented APIs; Academix OSS as reference. Deduplication across sources is the key challenge |
| **Opportunity Score** | **+4** | |

**Differentiation over existing MCPs:** The existing Academic Paper Search MCP covers 2 sources; this covers 5. The key value-add is citation network traversal ("show me all papers that cite this seminal work") and cross-source deduplication — neither is in existing MCPs.

**Global fit:** Academic research is global. OpenAlex covers 200M+ works across all languages. Initial distribution: PhD Twitter/X, r/academia, r/MachineLearning.

**Price target:** $9/month individual, $29/month researcher (citation graphs + export), $99/month lab (team + API).

---

### #25 — Wearable Health & Fitness MCP *(Batch 2)*
**Score: +3 | BiG Fit: 2/5**

**What it is:** Multi-device health MCP querying Apple Health, Garmin Connect, Whoop, and Google Health Connect — exposes HRV, sleep stages, VO2max, and nutrition data to AI agents for training analysis.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 3 | Apple Health MCP (local XML export only); Garmin MCP (community, incomplete); Open Wearables (self-hosted). No polished managed multi-device product |
| API Availability | 5 | Apple HealthKit (free via Open Wearables OSS); Garmin Health API (free with partner registration); Whoop API (free researcher tier); Google Health Connect (free) |
| Willingness to Pay | 4 | Whoop $30/mo; TrainingPeaks $19/mo; Levels Health $199/mo |
| Build Effort | 3 | Open Wearables OSS handles normalization; challenge is managed cloud sync, per-device OAuth, and health data privacy compliance (HIPAA) |
| **Opportunity Score** | **+3** | |

**Note:** Health data privacy (HIPAA) adds compliance overhead that raises build effort and legal liability. Better as a future project after establishing revenue from simpler products.

---

### #26 — Patent Search & IP Intelligence MCP *(Batch 2)*
**Score: +3 | BiG Fit: 2/5**

**What it is:** Patent research MCP combining USPTO, EPO, and WIPO databases — enables prior art search, freedom-to-operate analysis, and competitor patent filing tracking.

| Dimension | Score | Notes |
|---|---|---|
| Competition | 3 | patent_mcp_server (PulseMCP): prosecution/PTAB focus only. Patent Connector (patent.dev): one commercial competitor confirmed |
| API Availability | 4 | USPTO ODP API (free, new April 2026); EPO OPS (free, 4,000 req/day); WIPO PATENTSCOPE (free) |
| Willingness to Pay | 5 | Derwent Innovation $20,000+/year; PatSnap $5,000–20,000/year |
| Build Effort | 3 | USPTO ODP is brand new (docs in flux); EPO returns quirky XML; prior art ranking logic is non-trivial |
| **Opportunity Score** | **+3** | |

**Note:** Extreme WTP from patent attorneys ($300–500/hour for prior art searches) but the technical complexity of patent XML parsing and one confirmed commercial competitor reduce the opportunity score. Best pursued after establishing developer credibility.

---

## Market Feasibility Comparison Matrix

*Sorted by fastest-to-revenue for a solo developer.*

| Product | Time to MVP | Rev Ceiling | Defensibility | Price Target | API Cost |
|---|---|---|---|---|---|
| Visa & Travel MCP | **1–2 days** | $8K+/mo | Low–Medium | $9–29/mo | $0 |
| EU AI Act Compliance MCP | **1–2 days** | $20K+/mo | Medium | $49–149/mo | $0 |
| Clinical Trials & FDA MCP | **2–3 days** | $50K+/mo | Medium | $29–99/mo | $0 |
| Grant Discovery MCP | 1 week | $15K+/mo | Medium | $49–149/mo | $0 |
| CVE & Security Intel MCP | 1 week | $15K+/mo | Medium | $19–49/mo | $0 |
| Media Monitoring MCP | 1 week | $12K+/mo | Medium | $19–49/mo | $0–49/mo |
| Developer Analytics MCP | 1 week | $15K+/mo | Medium | $19–49/mo | $0 |
| Academic Literature MCP | 1 week | $10K+/mo | Medium | $9–29/mo | $0 |
| Energy & Carbon MCP | 1 week | $12K+/mo | Medium | $29–149/mo | $0 |
| **Crypto Tax MCP** | **2–3 weeks** | **$20K+/mo** | **High** | **$19–29/mo** | Low |
| Multi-Exchange P&L MCP | 2 weeks | $15K+/mo | Medium | $9–29/mo | $0 |
| B2B Lead Enrichment MCP | 1–2 weeks | $30K+/mo | Medium | $29–79/mo | $49+/mo |
| Sports & Betting Intel MCP | 1–2 weeks | $12K+/mo | Medium | $19–49/mo | $30+/mo |
| Multi-Cloud FinOps MCP | 2–3 weeks | $20K+/mo | Medium | $29–79/mo | ~$1–5/mo |
| Labor Market Comp MCP | 1 week | $20K+/mo | Medium | $49–199/mo | $0 |
| Logistics Tracking MCP | 1–2 weeks | $10K+/mo | Low | $19–49/mo | $0 trial |
| E-Commerce Inventory MCP | 3–4 weeks | $25K+/mo | Medium-High | $29–99/mo | $0 start |
| Creator Revenue Analytics | 2 weeks | $8K+/mo | Low | $19–49/mo | $0 |

---

## BiG-Adjusted Priority Stack (Global Target)

Given: <5 hours/week, solo developer, crypto + dev experience, global English-speaking audience.

### Tier 1 — Build Now (Highest BiG fit + proven demand)
1. **Crypto Tax MCP** — URGENT. 1099-DA lot-ID complexity extends demand through 2027. Zero MCP competition globally. Crypto domain knowledge is the edge. Ship MVP by April 15.
2. **Multi-Exchange Portfolio P&L MCP** — Natural precursor to tax MCP. CCXT covers 100+ global exchanges. DCA automation bundles in. 500M+ global crypto users.
3. **CVE & Security Intelligence MCP** — All 5 APIs free ($0 forever). BiG is a software developer — this is native territory. DevSecOps audience is reachable via HN, r/netsec. Clear wedge over single-source NVD-only existing MCPs.

### Tier 2 — Validate Fast (1–2 day builds, high score, zero API cost)
4. **Visa & Travel Requirements MCP** — True weekend build. Passport Index (GitHub, free) covers the data. Zero competition. Massive global audience. Best "quick win" product to ship while building Tier 1.
5. **EU AI Act Compliance MCP** — 1–2 day build, zero API cost, August 2026 hard deadline creates urgency. Every global SaaS company with EU users is a buyer.
6. **Grant Discovery & Funding MCP** — Zero competition anywhere. Grants.gov API free and simple. Instrumentl's $55M raise validates timing. Professional buyers at $299–499/mo budgets.

### Tier 3 — Strong market, moderate build
7. **Developer Analytics / BI MCP** — BiG is the target user. GA4 has 10M+ global properties. Massive GoodData price gap. Natural upsell from Multi-Cloud FinOps MCP.
8. **Multi-Cloud FinOps MCP** — BiG has K8s/cloud background. AWS-only existing MCPs leave multi-cloud users unserved. Revenue ceiling $20K+/mo. Pairs with Developer Analytics.
9. **Media Monitoring & Brand Mention MCP** — Free APIs cover 80% of value. Indie hacker / SaaS founder distribution is the same audience as Developer Analytics MCP. Cross-sell opportunity.
10. **Clinical Trials & FDA MCP** — Fastest build (+8 raw score). Cold pharma market but free launch cost makes it low-risk. Best "ship and see" for new vertical validation.

### Tier 4 — Medium-term (Longer build or secondary market)
11. **B2B Lead Enrichment MCP** — Global sales tech buyers, proven WTP. Requires Apollo API subscription ($49+/mo) to get started.
12. **Sports & Betting Intelligence MCP** — Global $100B market. Clear gap between existing single-source MCPs. Build after crypto products establish trust.
13. **E-Commerce Inventory & Repricing MCP** — Shopify 4.4M global stores. Revenue ceiling high ($25K+/mo) but Amazon SP-API auth complexity pushes build time to 3–4 weeks.
14. **Academic Literature Intelligence MCP** — All APIs free. Existing partial MCPs confirm demand. Lower WTP ceiling ($9–29/mo) vs other products.

### Not Recommended
- **Bitkub / Thai Market MCP** — Local market only, no global path.
- **Whale Tracker** — Better as bundled feature in Multi-Exchange Portfolio MCP.
- **Budget/Spending AI** — Too competitive (YNAB, Copilot loyal followings).
- **Forex MCP** — Single-player competitor already exists.
- **Wearable Health MCP** — HIPAA compliance overhead + fragmented device APIs. Revisit when portfolio is established.

---

## New Gap Signals (April 2026 — Batch 1 + Batch 2)

**Batch 1 confirmed gaps (PulseMCP searches):**
- "shipping", "logistics", "FDA", "clinical trials", "Apollo", "lead enrichment", "EU AI Act", "compliance" — all return zero or near-zero results

**Batch 2 confirmed gaps (PulseMCP searches):**
- "visa", "travel requirements", "passport" — zero standalone visa MCP (Visa payment network returns, not travel)
- "grant", "nonprofit", "foundation funding" — zero results
- "brand mention", "media monitoring" — only generic news/RSS MCPs, no brand tracking
- "carbon", "electricity price", "CSRD" — only narrow Climatiq MCP (calculation only)
- "CVE", "EPSS", "KEV" — only single-source NVD/CVE-search MCPs, no combined prioritization
- "multi-cloud cost", "FinOps", "cloud billing" — only AWS-specific MCPs

**Structural signals:**
- **Stripe MPP now live** with Anthropic/OpenAI/Visa backing — enterprise billing rails ready for B2B products
- **MCP security (30 CVEs in 60 days)** — auth + security is a product differentiator, not just best practice
- **EU AI Act August 2026 enforcement** — hard deadline = urgency marketing
- **Instrumentl raised $55M** (2026) — validates grant discovery as a funded market
- **USPTO ODP API launched April 2026** — new free patent API creates a window before competition catches up
- **PatentsView shutdown March 2026** — left a data gap the new USPTO API fills, no MCP wraps it yet

---

## Sources

**Existing research base:** findings/2026-03-22 through 2026-03-28 (PulseMCP, Smithery, HN, IRS notices)

**Batch 1 research (2026-04-05):**
- PulseMCP/Smithery searches: shipping, FDA, clinical, Apollo, EU AI Act, Calendly, grant
- MCP Roadmap 2026 — The New Stack; Healthcare MCP Servers — DEV Community
- EU AI Act enforcement — EUR-Lex, Vanta; HR MCP Servers — ChatForest
- AfterShip/EasyPost/Shippo pricing; Apollo.io/Hunter.io/Clearbit pricing
- ClinicalTrials.gov API v2, OpenFDA, BLS, DOL H-1B documentation

**Batch 2 research (2026-04-05):**
- PulseMCP/Smithery searches: visa, grant, nonprofit, brand mention, carbon, CVE, EPSS, multi-cloud, academic, wearable, patent
- Passport Index dataset (GitHub); VisaDB.io documentation
- The Odds API pricing; BALLDONTLIE API documentation
- Octolens MCP announcement; Google News RSS, NewsData.io pricing
- EIA Open Data API; Electricity Maps API; Ember Climate API
- Grants.gov REST API docs; USASpending.gov API; Instrumentl $55M raise (Crunchbase)
- NVD API v2, CISA KEV, EPSS (first.org), OSV.dev documentation
- AWS Cost Explorer pricing; GCP Billing API; Azure Cost Management API
- OpenAlex API; Semantic Scholar API; arXiv API documentation
- USPTO ODP API (launched April 2026); EPO OPS API; WIPO PATENTSCOPE API
- Garmin Health API; Whoop Developer API; Google Health Connect documentation
