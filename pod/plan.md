# POD (Print on Demand) — Implementation Plan

> Fully automated POD business: discover niches → AI designs → Etsy copy → Printify/Gelato fulfillment → analytics.
> Current status: Phases 0-7 complete (full pipeline built). Phase 8 (VPS deploy) and Phase 9 (integration tests) pending.
> URGENT: Mother's Day (May 10) buyer peak starts in 1-2 weeks. Listings must go live NOW.

---

## Phase 0: Deep Market Research & Target Customer (DO FIRST)

**Goal:** Validate niche selection with real Etsy data and build a laser-focused customer profile for each product line.

### Market Sizing & Validation
- [ ] Use eRank or EverBee to pull real search volume for target keywords:
  - "personalized mom gift" — monthly searches, competition score, avg price
  - "first Mother's Day gift" — same metrics
  - "custom tumbler for mom" — same metrics
  - "mama sweatshirt personalized" — same metrics
  - "promoted to grandma gift" — same metrics
- [ ] Analyze top 20 listings for each keyword: avg reviews, avg price, shop age, monthly sales estimate
- [ ] Identify sweet-spot niches: 2,000-10,000 search results with <100 avg reviews in top 20
- [ ] Calculate real unit economics for each product type with Gelato:
  - Base cost + shipping + Etsy fees + Etsy Ads → what's the minimum profitable price?
  - Run scenarios at $19.99, $24.99, $29.99, $34.99 price points
- [ ] Research Etsy seasonal revenue data: how much do top POD shops make in May (Mother's Day)?
- [ ] Analyze 5 successful POD shops (1K+ sales) — reverse-engineer their niche, pricing, listing strategy

### Laser-Targeted Customer Persona
- [ ] **Primary persona: "Gift-Giving Grace"** — Mother's Day buyer:
  - Age: 25-45 (buying for their own mom or mother-in-law)
  - Budget: $20-$40 per gift
  - Decision timeline: starts shopping 2-3 weeks before (early-mid April)
  - Search behavior: "personalized" + relationship + product type
  - What makes her click: personalization preview, fast shipping guarantee, 4.5+ star reviews
  - What makes her NOT buy: no reviews, unclear personalization process, shipping uncertainty
- [ ] **Secondary persona: "Trendy Tara"** — Gen Z/Millennial self-purchaser:
  - Buys "Romantic Goth", "Literary Girl", identity-expression products
  - Price sensitivity: $15-$25 for apparel, $10-$15 for accessories
  - Discovery: TikTok/Instagram → Etsy search (external traffic = ranking boost)
  - Trigger: sees trend on social media → searches Etsy for specific aesthetic
- [ ] **Tertiary persona: "Gen X Milestone Mary"** — buys for milestone events:
  - "Turning 50" gifts, retirement, empty nest, grandma promotion
  - Higher price tolerance: $25-$55
  - Values quality and personalization over trendy design
  - Discovery: Google search → Etsy (SEO matters most)
- [ ] Study actual Etsy reviews on competitor Mother's Day listings:
  - What do 5-star reviews praise? (personalization quality? fast shipping? design accuracy?)
  - What do 1-3 star reviews complain about? (late shipping? wrong color? cheap material?)

### Competitor Deep-Dive
- [ ] Identify top 10 POD shops selling Mother's Day products on Etsy
- [ ] For each shop: total sales, avg price, review count, listing count, shop age
- [ ] Analyze their top 5 best-selling listings: title format, tags, photos, pricing, personalization options
- [ ] Document what designs/styles are oversaturated vs underserved
- [ ] Check which POD provider they use (Printify, Printful, Gelato — check shipping times and reviews)
- [ ] Research TikTok Shop POD competition: who's selling, what volumes, what prices?

### Customer Discovery Channels
- [ ] Browse Etsy forums for seller discussions about Mother's Day strategy
- [ ] Monitor r/EtsySellers for POD-specific posts — what works, what doesn't
- [ ] Search Pinterest for "Mother's Day gift ideas 2026" — note what styles are trending
- [ ] Check TikTok for "Etsy haul" and "Mother's Day gift" videos — note what products get views
- [ ] Research Facebook groups for Etsy sellers — join 2-3 active groups for market intelligence

### Research Deliverables
- [ ] Niche validation matrix: keyword × search volume × competition × margin × persona fit
- [ ] Unit economics spreadsheet per product type (mug, sweatshirt, tote, tumbler)
- [ ] 3 customer persona cards with buying triggers, price sensitivity, discovery channels
- [ ] Top 10 competitor shop analysis with actionable gaps
- [ ] Final niche selection: top 3 product types to launch first with highest confidence

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Task Queue | Celery + Redis |
| API | FastAPI |
| Database | SQLite (data/pod.db) |
| POD Provider | Gelato (primary, free plan) → Printify Premium at scale |
| Design | Canva Pro ($15) + Kittl Pro ($10) + Midjourney ($10) |
| Marketplace | Etsy |
| Social | Buffer API |
| Notifications | Telegram (Apprise) |

---

## Phase 0-7: Core Pipeline ← COMPLETE

- [x] Phase 0: Project bootstrap
- [x] Phase 1: Trend scraper (pytrends, Reddit, Etsy Playwright)
- [x] Phase 2: AI design generation (Claude prompts → Stability AI/DALL-E → CLIP filter → Printify mockup)
- [x] Phase 3: Listing copy generator (Claude)
- [x] Phase 4: Upload automation (Printify publish → Etsy upload)
- [x] Phase 5: Analytics (Etsy stats pull, performance flagging)
- [x] Phase 6: Dashboard (FastAPI web UI)
- [x] Phase 7: Scheduler (Celery Beat, 19 cron entries)

---

## Phase 8: VPS Deployment ← NEXT

**Goal:** Deploy full pipeline to VPS for 24/7 automated operation.

### Tasks
- [ ] Create `docker-compose.prod.yml` (app + worker + beat + Redis + flower)
- [ ] Create `deploy.sh` VPS setup script (install Docker, pull repo, configure .env)
- [ ] Set up VPS (BiG's existing VPS or Railway)
- [ ] Configure environment variables on VPS
- [ ] Deploy and verify all Celery Beat schedules running
- [ ] Verify Telegram notifications working from VPS
- [ ] Set up health check monitoring (uptime ping)
- [ ] Configure log rotation on VPS

### Deliverable
Pipeline running 24/7 on VPS. All scheduled tasks executing.

---

## Phase 9: Integration Tests ← IN PROGRESS

**Goal:** Verify full pipeline chain works end-to-end.

### Tasks
- [x] Create tests/conftest.py with in-memory SQLite fixture
- [x] Create test_pipeline_integration.py (status transitions, TaskLog, full chain)
- [x] Create test_dashboard.py (page load, seeded DB)
- [ ] Run integration tests: `pytest tests/ -v`
- [ ] Fix any test failures
- [ ] Add Celery task chain tests
- [ ] Add error recovery tests (API failures, retry logic)

### Deliverable
All tests passing. Pipeline verified end-to-end.

---

## Phase 10: Etsy Shop Launch & Mother's Day Sprint

**Goal:** Launch Etsy shop with 20+ listings targeting Mother's Day (May 10, 2026).

### Tasks
- [ ] **URGENT: Create Etsy shop account** (if not already done)
- [ ] Set up shop: banner (1600x400px), logo (500x500px), About section with real photo
- [ ] Configure shop policies (returns, shipping, processing time)
- [ ] **Mother's Day listings (publish this week):**
  - [ ] Personalized "Mama" sweatshirts (embroidery/puff text style)
  - [ ] Custom mugs (names + "Est. year" + birth flowers)
  - [ ] "First Mother's Day 2026" designs (lower competition sub-niche)
  - [ ] Stepmom / Bonus Mom variants (lower competition)
  - [ ] "Promoted to Grandma 2026" gifts
  - [ ] Custom tote bags ("Mom Mode: On")
  - [ ] Mama & Me matching sets (neutral tones)
- [ ] **Each listing must have:**
  - [ ] 5+ photos (lifestyle mockup, detail close-up, scale ref, variants, personalization example)
  - [ ] 15-second phone-filmed video
  - [ ] Conversational title (2-3 natural phrases — semantic search optimized)
  - [ ] All attribute fields filled (= extra tags for Etsy algorithm)
  - [ ] AI disclosure in description (mandatory Etsy policy)
  - [ ] Free shipping badge (bake shipping into price, 30-40% gross margin target)
- [ ] Target: 20+ listings in first week
- [ ] Set up Etsy Ads: $1-3/day on top 3-5 listings AFTER publishing
- [ ] Evaluate Gelato as POD provider (free plan, 3-5 day delivery, automatic routing)

### Deliverable
Live Etsy shop with 20+ Mother's Day listings. Ads running.

---

## Phase 11: Father's Day & Pride Month (May 1 Deadline)

**Goal:** Second wave of seasonal listings for June holidays.

### Tasks
- [ ] **Father's Day (June 21) designs — publish by May 1:**
  - [ ] "World's Best [Niche] Dad" variant sets
  - [ ] Personalized dad mugs
  - [ ] Humor tees ("Dad Joke Loading...")
  - [ ] Gen X milestone: "Turning 50/60" humor
- [ ] **Pride Month (June) designs — publish by May 1:**
  - [ ] Rainbow/inclusive designs across categories
  - [ ] "Love is Love" apparel and accessories
- [ ] **Additional opportunities:**
  - [ ] National Sibling Day (April 10) — matching sibling tees
  - [ ] National Pet Day (April 11) — custom pet portraits
  - [ ] Star Wars Day (May 4) — fan designs
  - [ ] Memorial Day (May 25) — patriotic apparel
- [ ] Add crossbody bags to catalog (61% YoY Etsy search growth, low POD competition)
- [ ] Target: 50+ total listings by end of May

### Deliverable
50+ listings covering Q2 seasonal calendar.

---

## Phase 12: Analytics & Optimization

**Goal:** Data-driven optimization based on real sales data.

### Tasks
- [ ] Pull Etsy analytics daily (via existing Phase 5 pipeline)
- [ ] Identify top-performing designs and niches
- [ ] A/B test listing photos (AI mockup vs phone-filmed)
- [ ] Optimize ad spend: increase on winners, pause on losers
- [ ] Implement price adjustment logic (existing price_adjuster tool)
- [ ] Generate weekly performance report (existing weekly_report tool)
- [ ] Drive external traffic from Pinterest/TikTok (algorithm boost)
- [ ] Scale winning designs to new product types (mug → tumbler → blanket)

### Deliverable
First Etsy sale. Data-driven optimization loop running.

---

## Key Research Insights Driving This Plan

- **Mother's Day is the #1 POD revenue event** — buyer peak starts in 1-2 weeks (early April)
- **Micro-niches win**: Stepmoms, first-time moms, twin moms, new grandmas = lower competition
- **Gelato recommended over Printify for new sellers**: Free plan, 140+ facilities, 3-5 day delivery, no customs
- **Listing volume matters**: Shops uploading weekly have 314% higher traffic
- **First sale timeline**: 2-6 weeks with good SEO, compress to days with $3/day Etsy Ads
- **2026 authenticity rule**: Phone-filmed 15s video outperforms studio mockups
- **Semantic search is live**: Conversational titles required, keyword stuffing penalized
- **Engagement > keywords**: Clicks/favorites/purchases drive ranking, not just keyword matching
- **Sweet spot niche size**: 2,000-10,000 Etsy results = enough demand, low competition
- **Trending styles**: Patchwork/quilting, embroidery text, retro pastels, Romantic Goth, Chateaucore
- **Net margin target**: 25-35%; under 15% is fragile

---

## Design Themes to Target (2026 Trends)

1. **Whimsy & Playfulness** — Etsy's official Spring/Summer 2026 trend
2. **Chateaucore / Old-Money Romance** — monogrammed, ornate
3. **Patchwork Mama** — faux quilting/embroidery text
4. **Romantic Goth** — black cats, tarot, celestial (Comfort Colors)
5. **Cherry / Pop Fruit** — simple icons on mugs/tees (summer strong)
6. **Literary Girl** — book-lover identity products
7. **Island Luxe** — linen textures, terracotta tote bags
8. **Star Maps / Coordinate Art** — personalized wall art ($30-60)

---

## Q2 2026 Seasonal Calendar

| Date | Event | List By |
|------|-------|---------|
| April 5 | Easter | Too late for physical; digital downloads viable |
| April 10 | National Sibling Day | This week |
| April 11 | National Pet Day | This week |
| April 22 | Earth Day | This week |
| May 4 | Star Wars Day | Now |
| **May 10** | **Mother's Day** | **NOW — peak buyer window starting** |
| May 25 | Memorial Day | April 10 |
| June 1-30 | Pride Month | May 1 |
| **June 21** | **Father's Day** | **May 1** |
| June 19 | Juneteenth | May 15 |
