# Micro-SaaS — Implementation Plan

> Build a focused SaaS tool solving one specific problem for e-commerce sellers.
> Top candidate: **Shopee Penalty Shield** — real-time monitoring + alerting on Shopee policy breach risk.
> Revenue target: 50 paying customers at $19-29/month = $950-$1,450 MRR.

---

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate which micro-SaaS to build with real seller data before writing any code.

### Market Sizing & Validation
- [ ] Research Shopee seller ecosystem in Thailand:
  - Total active sellers on Shopee Thailand (Shopee investor reports, press releases)
  - How many sellers have been penalized in last 6 months? (community reports, Facebook groups)
  - What tools do Thai Shopee sellers currently use? (Shopdora, Feexivo, BigSeller — adoption rates)
- [ ] Research TikTok Shop seller ecosystem:
  - Total TikTok Shop sellers in Southeast Asia
  - How many were affected by March 20 attribute lockdown?
  - Current compliance rates after the deadline
- [ ] Research EU AI Act Article 4 market:
  - How many EU SMBs (<250 employees) need AI literacy compliance?
  - What do existing enterprise solutions (KnowBe4) charge? ($5K-$50K/year?)
  - Is there demand at $29-$79/month for SMBs?
- [ ] Validate "Shopee Penalty Shield" willingness-to-pay:
  - Post in 3 Thai Shopee seller Facebook groups: "Would you pay ฿500/month (~$15) for penalty alerts?"
  - Track responses: how many say yes, how many say no, what price do they suggest
- [ ] Research competitor tools pricing and user counts:
  - Shopdora: features, pricing, user reviews, what it doesn't do
  - BigSeller: same analysis
  - Feexivo: same analysis

### Laser-Targeted Customer Persona
- [ ] **Primary persona: "Shopee Seller Somchai"** — Thai Shopee seller:
  - Business type: sole proprietor or small team (1-3 people)
  - Monthly GMV: ฿50K-฿500K ($1,500-$15,000)
  - Product categories: fashion, beauty, electronics, home goods
  - Current pain points: sudden penalties, fee confusion, policy changes
  - Tech comfort: uses LINE and Facebook daily, basic web tools, mobile-first
  - Willingness to pay: ฿300-฿1,000/month ($9-$29) for business tools
  - Where they hang out: Thai Shopee seller Facebook groups (find top 5 with most members)
  - Language: Thai only — tool MUST be in Thai
- [ ] **Secondary persona: "TikTok Seller Tanya"** — TikTok Shop seller (MY/PH/TH):
  - Newer to e-commerce, younger (20-30)
  - Struggles with attribute compliance, video requirements
  - More willing to try new SaaS tools than traditional Shopee sellers
  - Price sensitivity: $10-$20/month
  - Discovery: TikTok itself, YouTube tutorials, seller forums
- [ ] **Tertiary persona: "EU Compliance Clara"** — EU SMB compliance officer:
  - Company size: 10-200 employees
  - Pain: overwhelmed by AI Act requirements, no budget for enterprise tools
  - Decision-maker or needs manager approval?
  - Discovery: LinkedIn, EU compliance newsletters, Google search
- [ ] Interview 10 actual Shopee sellers (Thai Facebook groups, LINE groups):
  - "Have you been surprised by a penalty in the last 3 months?"
  - "How much time do you spend checking your seller metrics?"
  - "What tool would save you the most time/money?"

### Competitor Deep-Dive
- [ ] Sign up for Shopdora free trial — document all features, what's missing
- [ ] Sign up for BigSeller — same analysis, focus on penalty/compliance features
- [ ] Research SellerCenter.shopee.co.th built-in analytics — what does Shopee already provide for free?
- [ ] Map all existing Shopee seller tools by category: analytics, pricing, inventory, compliance, chat
- [ ] Identify the exact gap: real-time penalty monitoring + predictive alerting = nobody does this
- [ ] For TikTok: research CJ Dropshipping's compliance features — what's covered, what's not

### Customer Discovery Channels
- [ ] Join top 5 Thai Shopee seller Facebook groups (10K+ members each)
- [ ] Join top 3 TikTok Shop seller groups (Thai and English)
- [ ] Monitor r/Shopee and r/ecommerce for seller pain points
- [ ] Follow Shopee Thailand official announcements — track policy changes
- [ ] Connect with 3-5 Shopee top sellers (>1000 orders/month) — they feel penalty pain most

### Research Deliverables
- [ ] 1-page validation brief: which product, which persona, what price, where to find them
- [ ] Competitor feature matrix: existing tools × features × pricing × gaps
- [ ] 10+ seller quotes about penalty/compliance pain points
- [ ] Willingness-to-pay data from Facebook group polls
- [ ] Go/no-go decision: build Shopee Penalty Shield or pivot to alternative

---

## Product Candidates (Ranked by Signal Strength)

### 1. Shopee Penalty Shield (Priority 1)
- Real-time monitoring of chat response rate, LSR, fulfillment latency
- AI-automated penalty detection (83% of Shopee deductions are algorithmic)
- Push alerts before penalties trigger (90-minute enforcement window)
- Target: MY/TH/PH Shopee sellers
- Gap: No existing tool does real-time penalty monitoring

### 2. TikTok Attribute Enricher (Priority 2)
- CSV upload → auto-fill missing product attributes via AI
- Addresses mandatory March 20, 2026 attribute lockdown
- Gap: No third-party enrichment tool exists

### 3. EU AI Act Article 4 SMB Compliance Tool (Priority 3)
- Employee AI literacy training tracker
- Audit evidence log + AI systems inventory
- Enforcement deadline: August 3, 2026
- Gap: No SMB-friendly tool under $100/month

---

## Tech Stack

| Layer | Tool |
|---|---|
| Backend | Go (BiG's strength) |
| Frontend | React or HTMX (start simple) |
| Database | PostgreSQL on Supabase |
| Auth | Supabase Auth |
| Billing | Stripe |
| Hosting | Railway or Fly.io |
| Notifications | Telegram Bot API + Email (Resend) |

---

## Phase 1: Validate — Landing Page & Customer Interviews

**Goal:** Prove 20+ potential customers would pay before writing any code.

### Tasks
- [ ] Pick one product (Shopee Penalty Shield recommended)
- [ ] Create landing page:
  - [ ] Problem statement in Thai + English
  - [ ] Feature preview (monitoring dashboard mockup)
  - [ ] Pricing preview ($19/month starter, $29/month pro)
  - [ ] Email signup form ("Get early access")
  - [ ] Use Lovable or simple HTML + Vercel (ship in hours, not days)
- [ ] Write launch copy targeting MY/TH/PH Shopee sellers
- [ ] Post in Thai Shopee seller Facebook groups (gauge interest)
- [ ] Post in r/Shopee, r/ecommerce, r/SaaS
- [ ] Conduct 10-20 problem interviews:
  - [ ] "How often do you check your Shopee penalty points?"
  - [ ] "Have you ever been surprised by a penalty?"
  - [ ] "Would you pay $19/month to get alerts before penalties trigger?"
- [ ] Target: 20+ email signups AND 5+ "I would pay for this" responses

### Deliverable
Landing page live. 20+ signups. Validation data to decide build/no-build.

---

## Phase 2: MVP Build (One Weekend)

**Goal:** Working MVP with core monitoring + alerting. Ship fast, iterate later.

### Tasks
- [ ] Set up Go project with standard layout
- [ ] Implement Shopee Seller Center API integration:
  - [ ] Fetch seller metrics (chat response rate, LSR, fulfillment latency)
  - [ ] Fetch current penalty points
  - [ ] Poll every 15 minutes (respect rate limits)
- [ ] Implement penalty risk scoring:
  - [ ] Calculate risk score based on current metrics vs thresholds
  - [ ] Flag when metrics approach penalty trigger zones
  - [ ] Priority alerts: chat response (12-min threshold), LSR (5% threshold)
- [ ] Implement alerting:
  - [ ] Telegram bot notifications (primary — Thai sellers prefer Telegram/LINE)
  - [ ] Email alerts (secondary)
  - [ ] Alert types: warning (approaching threshold), critical (penalty imminent)
- [ ] Build minimal dashboard:
  - [ ] Current penalty points display
  - [ ] Metric health indicators (green/yellow/red)
  - [ ] Alert history
  - [ ] Settings (thresholds, notification preferences)
- [ ] Implement Supabase Auth (email + social login)
- [ ] Deploy to Railway
- [ ] Write tests for risk scoring logic

### Deliverable
Working MVP. Users can connect Shopee account and receive penalty risk alerts.

---

## Phase 3: Launch & First 10 Customers

**Goal:** Convert landing page signups to paying customers.

### Tasks
- [ ] Integrate Stripe billing:
  - [ ] Free tier: 1 store, daily summary only
  - [ ] Starter ($19/month): 1 store, real-time alerts, Telegram
  - [ ] Pro ($29/month): 3 stores, SMS alerts, API access
- [ ] Invite landing page signups to beta (free for 14 days)
- [ ] Collect feedback from beta users aggressively
- [ ] Fix top 3 issues from feedback
- [ ] Launch on:
  - [ ] Thai Shopee seller Facebook groups
  - [ ] r/SaaS, r/Entrepreneur, r/IndieHackers
  - [ ] Product Hunt
  - [ ] Indie Hackers community
- [ ] Consider pre-selling 50 Lifetime Deals on AppSumo before full launch
- [ ] Target: 10 paying customers within 30 days of launch

### Deliverable
10 paying customers. Stripe billing active.

---

## Phase 4: Iterate & Scale

**Goal:** Improve retention, add features, grow to 50 customers.

### Tasks
- [ ] Add 4.4 Mega Sale (April 4) campaign monitoring features
- [ ] Add Product Identity Verification (PIV) compliance checking
- [ ] Implement weekly performance digest email
- [ ] Add LINE Official Account integration (Thai sellers prefer LINE)
- [ ] Build competitor pricing monitoring (adjacent feature)
- [ ] Add multi-language support (Thai, English, Bahasa, Vietnamese)
- [ ] Optimize for mobile (sellers check on phone)
- [ ] A/B test pricing
- [ ] Target: 50 paying customers, $950+ MRR

### Deliverable
Stable product with growing customer base.

---

## Phase 5: Second Product (If Validated)

**Goal:** Build second micro-SaaS based on learnings from first.

### Tasks
- [ ] Evaluate TikTok Attribute Enricher based on remaining demand
- [ ] Evaluate EU AI Act SMB tool if approaching August 2026 deadline
- [ ] Consider: Shopee fee calculator (bake in 5% technical fee, cross-border fee, commission)
- [ ] Leverage existing infra (Go backend, Supabase, Stripe) for fast build
- [ ] Cross-sell to existing Shopee Penalty Shield customers

### Deliverable
Second product launched or validated as no-go.

---

## Key Research Insights Driving This Plan

- **Shopee Penalty v4.2**: 83% of deductions are AI-automated; 12-min chat delay = 5-point suspension
- **No real-time penalty alert tool exists**: Shopdora, Feexivo cover analytics but not live breach monitoring
- **Shopee 5% Technical Fee**: Active since Feb 1, 2026 in SG/MY/TH/VN — sellers are cost-squeezed
- **TikTok mandatory attributes**: March 20, 2026 lockdown — no third-party enrichment tool exists
- **EU AI Act Article 4**: August 2026 enforcement — no SMB tool under $100/month
- **Micro-SaaS market**: $15.7B (2024) → $59.6B by 2030, ~30% CAGR
- **Hyper-vertical tools at $19-49/mo are finding customers fastest** in 2026
- **"First 10 customers" playbook**: Landing page + 10-20 interviews + beta at discount = 30-day validation
- **LTD pre-sales**: Pre-selling 50 LTDs on AppSumo before code = proven 2026 tactic
- **Indie hacker stack**: Lovable + Cursor + Supabase + Stripe = ship in days, $0-50/month tooling

---

## Validation Criteria (Go/No-Go)

| Signal | Threshold | Action |
|---|---|---|
| Landing page signups | ≥20 in 2 weeks | Proceed to MVP |
| "Would pay" interviews | ≥5 of 10-20 | Proceed to MVP |
| Landing page signups | <10 in 2 weeks | Pivot to TikTok Attribute Enricher |
| Beta → paid conversion | ≥15% | Scale launch efforts |
| Beta → paid conversion | <5% | Re-evaluate product-market fit |
