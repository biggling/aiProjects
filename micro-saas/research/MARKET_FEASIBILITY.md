# Micro-SaaS — Market Feasibility Comparison
> Synthesized from all research sessions: 2026-03-23 through 2026-03-27
> Last updated: 2026-03-29

---

## Summary Scorecard

| # | Product | Market Size | Pain Intensity | Build Speed | WTP | Competition | Urgency | **Score** |
|---|---------|-------------|----------------|-------------|-----|-------------|---------|-----------|
| 1 | Shopee Penalty Shield | Large | 🔴 Critical | Medium | High | None | High | **9/10** |
| 2 | TikTok Shipping Fee Auditor | Large | 🔴 Critical | Fast | High | None | High | **8.5/10** |
| 3 | TikTok Attribute Enricher | Large | 🟠 High | Fast | Medium | None | High | **7.5/10** |
| 4 | EU AI Act SMB Compliance Tool | Medium | 🟠 High | Medium | Medium | Low | High | **7/10** |
| 5 | Shopee Fee Calculator | Large | 🟡 Medium | Fast | Low–Med | Low | Medium | **6/10** |
| 6 | HookSalvage (Webhook DLO) | Small | 🟡 Medium | Medium | Low | Medium | Low | **5/10** |
| 7 | Minimalist Thai Invoicing | Medium | 🟡 Medium | Fast | Low | Medium | Low | **4.5/10** |
| 8 | Crypto Tax Report (Thai) | Small | 🟡 Medium | Slow | Medium | Medium | Low | **4/10** |

---

## Detailed Analysis

---

### 1. Shopee Penalty Shield
**Concept:** Real-time monitoring of Shopee seller metrics (chat response rate, LSR, fulfillment latency) with predictive alerts before AI-automated penalties trigger.

**Market Evidence:**
- Shopee has 12M+ active sellers; 3.3B orders/quarter
- Shopee Penalty Policy v4.2 (March 2026): 83% of deductions are AI-automated — no human review
- A 12-minute delay in chat response during peak hours = 5-point deduction
- Penalties trigger automatically within 90 minutes of confirmed breach
- LSR threshold halved from 10% → 5% (SG/PH) — tighter compliance window
- Shopdora, Feexivo, BigSeller: cover analytics/fee calc but NOT live breach monitoring

**Target Market:** MY/TH/PH Shopee sellers (1–10 person shops, ฿50K–฿500K/mo GMV)

**Pricing Opportunity:** ฿300–฿1,000/month ($9–$29). Target: $19/mo starter, $29/mo pro.

**Revenue Path:** 50 customers × $19/mo = **$950 MRR**

**Build Effort:** 2–4 weeks MVP (Go backend, Shopee V2.0 Open API, Telegram/email alerts)

**Key Risks:**
- Shopee may restrict API access or change penalty calculation methodology
- Thai-language requirement adds friction (UI must be bilingual)
- Sellers trust is low for third-party account access — need clear OAuth flow

**Feasibility:** ✅ HIGH — clear gap, clear pain, no existing solution, API exists

---

### 2. TikTok Shipping Fee Auditor
**Concept:** Upload TikTok Shop settlement CSV → tool highlights retroactive shipping adjustments, calculates disputed amounts, generates dispute filing documentation.

**Market Evidence:**
- "Second charge" wave: retroactive shipping fee adjustments for Sept–Nov 2025 orders hitting in March 2026
- Many sellers in negative balance with no documentation from TikTok
- TikTok support: 90-day fund freezes, "documentation loops" (repeated verification)
- TikTok Shop: 15M+ global sellers, projected $66B GMV
- No existing tool to parse/audit TikTok settlement files

**Target Market:** US/UK TikTok Shop sellers (high English-language community, vocal on Reddit)

**Pricing Opportunity:** Pay-per-audit ($5–$15 per report) or $9–$19/month

**Revenue Path:** 1,000 one-time audits × $9 = **$9,000** (one-time burst); or $9/mo subscription

**Build Effort:** 1–2 weeks (CSV parser + dispute template generator; no API needed, file upload only)

**Key Risks:**
- TikTok may fix the retroactive fee issue, reducing urgency
- Problem may be a one-time crisis, not recurring — limits subscription potential
- US market = more competition, harder to reach vs. Thai-focused tools

**Feasibility:** ✅ HIGH short-term — fastest to build, highest urgency, but may not be recurring

---

### 3. TikTok Attribute Enricher
**Concept:** Upload product CSV → AI auto-fills missing required attributes (material composition, manufacturer, safety standards) using product name + images + public databases.

**Market Evidence:**
- March 20, 2026: TikTok made product attributes mandatory (lockdown)
- AI now cross-checks video claims against product data fields — inconsistencies suppress listings
- CJ Dropshipping's API sync helps CJ users only; all other sellers do it manually
- No dedicated SaaS fills required product fields for non-CJ sellers

**Target Market:** TikTok Shop sellers globally (focus: US, UK, MY, PH)

**Pricing Opportunity:** $0.05 per listing enriched (usage-based) or $19/month for unlimited

**Revenue Path:** 100 active sellers × $19/mo = **$1,900 MRR**

**Build Effort:** 2–3 weeks (CSV parsing + LLM enrichment via Claude/GPT-4o API + output formatter)

**Key Risks:**
- March 20 deadline is past — sellers may have adapted manually or abandoned compliance
- Requires LLM API costs (not free) — margins depend on API pricing
- TikTok may build native enrichment tools in-platform

**Feasibility:** ✅ MEDIUM-HIGH — strong gap but urgency decreasing post-deadline

---

### 4. EU AI Act Article 4 SMB Compliance Tool
**Concept:** Self-serve platform for SMBs to: inventory AI systems, track employee AI literacy training, log acknowledgements, generate audit evidence documentation.

**Market Evidence:**
- Article 4 (AI Literacy): enforcement/supervision begins August 3, 2026 — 5-month window
- EC published simplified SMB templates in March 2026
- Digital Omnibus proposal may extend high-risk deadlines to Dec 2027 (but Aug 2026 still safest)
- Existing solutions: KnowBe4 ($5K–$50K/year enterprise), EU consultancies (expensive)
- No self-serve SMB tool under $100/month exists

**Target Market:** EU SMBs, 10–200 employees using AI in workflows (HR, marketing, ops)

**Pricing Opportunity:** $29–$79/month; annual plans at discount

**Revenue Path:** 200 customers × $49/mo = **$9,800 MRR** (if captured before August 2026)

**Build Effort:** 3–4 weeks MVP (training tracker + AI inventory form + PDF report generator)

**Key Risks:**
- BiG is in Bangkok, not EU — sales/trust harder; LinkedIn outreach required
- Regulatory scope may shift (Digital Omnibus proposal could extend deadlines)
- Post-August enforcement, demand may drop unless annual renewals built in

**Feasibility:** ✅ MEDIUM-HIGH — strong regulatory urgency but geography is a barrier

---

### 5. Shopee Fee Calculator
**Concept:** Multi-market calculator showing net profit after all Shopee fee types (Commission, Transaction, CCB, FSS, Tech Support 5%, OPF, MDV, campaign surcharges).

**Market Evidence:**
- Shopee has 8+ distinct fee types as of 2026 — sellers confused about actual margins
- 5% Technical Support Fee (Feb 2026), RM 0.54 PSF (MY), ₱5 OPF (PH), 1% campaign spike (PH)
- Thailand Mall commissions up to 15.52% as of March 2026
- Existing tools (BigSeller) do general analytics but not comprehensive per-country fee breakdown

**Target Market:** MY/TH/PH/VN Shopee sellers

**Pricing Opportunity:** Free tier → $5/month for advanced multi-market features

**Revenue Path:** 500 customers × $5/mo = **$2,500 MRR** (requires high volume)

**Build Effort:** 1 week (pure calculation logic, no API needed for basic version)

**Key Risks:**
- Low WTP ($5/month ceiling) — may attract free-tool expectations
- Fees change frequently — maintenance burden for a small team
- Limited monetization ceiling without upsell path

**Feasibility:** ✅ MEDIUM — good as a lead-gen/freemium entry but not a standalone business

---

### 6. HookSalvage (Webhook Dead-Letter Office)
**Concept:** Managed proxy ($5/month) that buffers incoming webhooks, handles retries with exponential backoff, replay failed payloads to localhost, provides failure UI.

**Market Evidence:**
- Hookdeck: dominant inbound tool; free 100K req/month, $39/month for 1M
- Svix: $0 → $490/month pricing cliff — gap for 100K–500K message teams
- Convoy: MIT-licensed self-hosted alternative
- Solo devs don't want to manage SQS/Lambda for side projects

**Target Market:** Solo developers and small dev teams (1–5 people)

**Pricing Opportunity:** $5–$29/month; usage-based at scale

**Revenue Path:** 500 customers × $9/mo = **$4,500 MRR** (needs large developer audience)

**Build Effort:** 3–5 weeks (Go backend, Redis/Postgres queue, retry logic, dashboard)

**Key Risks:**
- Hookdeck's free tier covers most solo dev use cases already
- Developer tools market is extremely crowded — hard differentiation
- BiG's Go expertise helps build but doesn't help with discovery (developer marketing is hard)

**Feasibility:** ✅ MEDIUM — technically within BiG's skillset but market is crowded

---

### 7. Minimalist Thai Invoicing
**Concept:** Bilingual (Thai/English) PDF invoice generator for Thai freelancers and small businesses with PromptPay QR embedded.

**Market Evidence:**
- Freelancers abandoning QuickBooks/Zoho for minimalist tools
- 2026 global e-invoicing mandates adding compliance need
- Thai-specific: PromptPay QR integration is a meaningful local differentiator
- No Thai-language minimalist invoicing tool with PromptPay exists

**Target Market:** Thai freelancers and micro-businesses

**Pricing Opportunity:** Freemium → $5–$9/month pro

**Revenue Path:** 1,000 customers × $5/mo = **$5,000 MRR** (requires large user base)

**Build Effort:** 2 weeks (PDF generator, PromptPay QR library, minimal UI)

**Key Risks:**
- Freelancer WTP is very low — high churn market
- Thai market has LINE-based invoicing (informal, dominant)
- Regulatory compliance (Thai Revenue Department e-tax invoicing) may be complex

**Feasibility:** ✅ LOW-MEDIUM — nice niche but low monetization ceiling

---

### 8. Crypto Tax Report Generator (Thai)
**Concept:** Calculate capital gains from Thai exchanges (Bitkub) for Thai tax filing requirements.

**Market Evidence:**
- Thai Revenue Department issued crypto tax guidance in 2022 (50% capital gains deduction or actual cost)
- Bitkub is the dominant Thai exchange with no built-in tax export
- No Thai-market crypto tax calculator exists

**Target Market:** Thai crypto investors using Bitkub

**Pricing Opportunity:** $9–$29/month or per-report pricing

**Revenue Path:** 200 customers × $9/mo = **$1,800 MRR**

**Build Effort:** 4–6 weeks (Bitkub API integration, tax calculation logic, report generation)

**Key Risks:**
- Thai crypto tax guidance is ambiguous — liability risk if calculations are wrong
- Small addressable market (active Thai crypto traders vs. passive holders)
- Requires ongoing tax law updates — high maintenance burden

**Feasibility:** ✅ LOW-MEDIUM — niche is real but small and legally risky

---

## Market Feasibility Matrix

| Dimension | Shopee Penalty Shield | TikTok Fee Auditor | TikTok Attr. Enricher | EU AI Act Tool |
|---|---|---|---|---|
| **Addressable market** | 12M Shopee sellers (SEA) | 15M TikTok sellers | 15M TikTok sellers | 3M+ EU SMBs |
| **Target segment** | MY/TH/PH sellers | US/UK sellers | Global | EU 10-200 emp |
| **Pain level** | Immediate/financial | Immediate/financial | Compliance risk | Regulatory deadline |
| **Existing solutions** | None | None | None | Enterprise only |
| **Price sensitivity** | Medium ($9–$29/mo) | Low (pay per audit) | Medium ($19/mo) | Low ($29–$79/mo) |
| **WTP confidence** | High | High | Medium | Medium |
| **API dependency** | Shopee Open API | No (CSV upload) | LLM API (paid) | No |
| **Build time (MVP)** | 2–4 weeks | 1–2 weeks | 2–3 weeks | 3–4 weeks |
| **BiG advantage** | Thai market + Go | None specific | None specific | None specific |
| **Geographic fit** | ✅ Bangkok/SEA | ❌ US focus | ⚠️ Global | ❌ EU focus |
| **Recurring revenue** | ✅ Yes | ⚠️ Maybe | ✅ Yes | ✅ Yes |
| **Urgency deadline** | Ongoing (API v4.2) | Now (March crisis) | Past (March 20) | August 2026 |

---

## Recommendation: Build Order

### Build #1: Shopee Penalty Shield ← PRIMARY
**Why:** Highest match of market pain + BiG's geographic advantage + recurring revenue + no competition + API exists.

**30-day validation plan:**
1. Post in 3 Thai Shopee seller Facebook groups: "Would you pay ฿500/month for penalty alerts?"
2. Build landing page in Thai + English (Lovable or static HTML, Vercel — 1 day)
3. Collect 20+ signups as go/no-go signal
4. Build MVP in Go: Shopee API polling + risk scoring + Telegram alerts

**Go/No-go:** 20+ signups AND 5+ "I would pay" = build. Less = pivot to #2.

---

### Build #2: TikTok Shipping Fee Auditor ← PARALLEL VALIDATION
**Why:** Fastest to build (no API, just CSV parsing), high urgency (March 2026 crisis ongoing), potential one-time revenue burst while validating #1.

**1-week validation plan:**
1. Post in r/TikTokShop: "I built a tool to parse your settlement CSV and flag retroactive charges"
2. Offer first 20 users free
3. Convert to $9/report after validation

**Note:** This may be a one-time revenue tool, not a long-term subscription — use it to fund Penalty Shield development.

---

### Build #3: EU AI Act SMB Tool ← POST-REVENUE
**Why:** High revenue ceiling ($29–$79/month), real regulatory deadline, but geography is a disadvantage. Build this after #1 generates revenue and confidence. Target English-speaking EU markets via LinkedIn.

---

## Key Strategic Insight

> The **Shopee Penalty Shield** is the only product where BiG has a genuine **unfair advantage** (Bangkok location → Thai/SEA market knowledge, relationships, language). All other products compete on a global playing field.
>
> The **TikTok Shipping Fee Auditor** is the fastest path to first revenue — ship it in one week as a CSV tool, get testimonials, and use the momentum to validate the Penalty Shield.

---

## Market Sizing (Bottom-Up)

| Product | TAM | SAM (reachable) | SOM (12-month) | 12-mo MRR Target |
|---|---|---|---|---|
| Shopee Penalty Shield | 12M sellers | 500K MY/TH/PH active sellers | 1,000 sellers | $19K MRR |
| TikTok Fee Auditor | 15M sellers | 1M US/UK active | 500 audits/mo | $4.5K/mo (usage) |
| TikTok Attr. Enricher | 15M sellers | 2M affected sellers | 500 subscribers | $9.5K MRR |
| EU AI Act Tool | 3M+ EU SMBs | 500K SMBs using AI | 300 subscribers | $14.7K MRR |

---

## Sources Summary

| Session | Key Findings |
|---|---|
| 2026-03-23 | Market sizing, persona analysis, platform API capabilities, vertical AI agent opportunity |
| 2026-03-24 (AM) | Shopee fee complexity (8+ fee types), TikTok retroactive shipping crisis, HookSalvage concept |
| 2026-03-24 (PM) | TikTok logistics mandate, Shopee Brazil fee hike, usage-based pricing trend |
| 2026-03-25 | Shopee LSR halved to 5%, TikTok "second charge" confirmed widespread, EU AI Act SMB mandate |
| 2026-03-26 | Shopee Thailand Mall commission hikes, TikTok return policy shift, EU simplified SMB templates |
| 2026-03-27 (AM) | Shopee API expansion, TikTok semantic audit enforcement, Etsy LLM search transition |
| 2026-03-27 (PM) | Shopee Penalty v4.2 details, 83% AI-automated deductions, no real-time alert tool confirmed |
