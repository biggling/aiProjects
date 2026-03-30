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
- [x] Phase 2: AI design generation (Claude prompts → Stability AI/DALL-E/Gemini Imagen → CLIP filter → Printify mockup)
- [x] Phase 3: Listing copy generator (Claude)
- [x] Phase 4: Upload automation (Printify publish → Etsy upload)
- [x] Phase 5: Analytics (Etsy stats pull, performance flagging)
- [x] Phase 6: Dashboard (FastAPI web UI)
- [x] Phase 7: Scheduler (Celery Beat, 19 cron entries)
- [x] Phase 7b: Gemini trend scraper — TrendSnapshot table, multi-source composite ranking
- [x] Phase 7c: Multi-horizon upcoming trend forecasting (8 horizons × 20 niches, 2-week steps, 14d–112d)

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

## Q2–Q3 2026 Seasonal Calendar (Gemini-forecasted, updated Mar 30)

| Peak Window | Horizon | Top Niches | List By |
|-------------|---------|-----------|---------|
| Apr 13 (14d) | 2w | Masters golf fan, autism awareness, NBA/NHL playoffs, Eid Mubarak, Earth Day, dog mom | **NOW** |
| Apr 27 (28d) | 4w | First Mother's Day gift, teacher appreciation, Nurses week, Cinco de Mayo, May 4th Star Wars | Apr 1 |
| May 11 (42d) | 6w | Teacher appreciation gift ↑96, nurse appreciation ↑96, class of 2026, dog mom Mother's Day, best teacher mug | Apr 6 |
| May 25 (56d) | 8w | Class of 2026 graduation, memorial day shirt, first Father's Day, girl dad, last day of school | Apr 13 |
| Jun 8 (70d) | 10w | Love is love pride, grill master dad, fishing dad, best dog dad, NBA finals fan | Apr 20 |
| **Jun 22 (84d)** | **12w** | **FIFA World Cup 2026 ↑98** (USA host!), first Father's Day ↑92, Juneteenth, girl dad, Father's Day | **May 1** |
| Jul 6 (98d) | 14w | July 4th squad, Cancer zodiac birthday, beach life, grill master (Nat'l Grilling Month), coastal cowgirl | May 15 |
| Jul 20 (112d) | 16w | Fantasy football ↑90, football season hype ↑89, tailgate season, back to school teacher, senior class 2027 | Jun 1 |

> ↑ = predicted upcoming_score at peak. World Cup 2026 (USA/Canada/Mexico host) is the **biggest single opportunity** this summer.

---

## Weekly Action Plan (from Mar 31, 2026)

> Rule: Each week publish listings for the horizon that peaks in ~4 weeks.
> Rule: Blue ocean niches first — lower competition = faster first sale.
> Rule: Etsy needs ~2 weeks to index a new listing before it gets organic traffic.
> BiG has ~5 hrs/week. Each week = shop setup OR listings, not both.

---

### Week 1 — Mar 31–Apr 6 | SHOP SETUP + FIRST LISTINGS
**Goal:** Live shop + 8 listings before Apr 13 peak

**Shop (one-time, ~2 hrs):**
- [ ] Create Etsy account + open shop (name: memorable, niche-neutral)
- [ ] Create Gelato account → connect to Etsy (free plan, auto-fulfillment)
- [ ] Upload shop banner (1600×400) + logo (500×500) — use Canva
- [ ] Write About section, set shop policies (free returns, 3-5 day processing)

**Listings — Blue Ocean picks for Apr 13 peak (~2 hrs):**
- [ ] `autism awareness puzzle piece mom` — sweatshirt + mug | Puzzle piece, pastel lavender, handwritten font
- [ ] `eid mubarak gift 2026` — mug + tote | Gold calligraphy, crescent moon, cream background
- [ ] `earth day recycled tee` — t-shirt | Minimalist globe, forest green, block print style
- [ ] `masters golf fan wife` — mug + t-shirt | Retro serif, Augusta green + gold
- [ ] `nba playoffs fan first year` — t-shirt | Bold varsity, team-neutral orange + black
- [ ] `dog mom national pet day` — sweatshirt + mug | Minimalist dog outline, warm terracotta
- [ ] `autism dad puzzle warrior` — t-shirt + mug | Bold, supportive text, jigsaw motif
- [ ] `siblings day matching shirt` — t-shirt set | Playful font, pastel color-block

**Pipeline:**
- [ ] Run `gemini_trend_scraper` + `blue_ocean_scraper` (already done Mar 30 — check DB is seeded)
- [ ] Verify Celery Beat schedule is running on VPS or locally

---

### Week 2 — Apr 7–13 | MOTHER'S DAY WAVE 1 (publish for Apr 27 peak)
**Goal:** 8-10 Mother's Day listings live by Apr 10

**Blue ocean Mother's Day listings (~3 hrs):**
- [ ] `first mothers day ivf mom 2026` — sweatshirt + mug | Soft watercolor, "Worth the Wait", blush + gold
- [ ] `bonus mom est 2026` — sweatshirt + mug | Patchwork/embroidery text, sage green, floral border
- [ ] `dog mom mothers day golden retriever` — t-shirt + mug | Minimalist dog breed outline, warm tones
- [ ] `twin boy girl mom 2026` — sweatshirt | Two-tone design, "Double the Love"
- [ ] `grandma promoted 2026` — mug + tote | Whimsical font, flower crown illustration
- [ ] `kindergarten teacher summer` — sweatshirt + mug | Apple + crayon motif, bright pastels
- [ ] `nurse practitioner mothers day` — t-shirt + mug | Clean medical cross, "NP + Mom"
- [ ] `plant mom gift` — tote + mug | Botanical illustration, earthy sage + terracotta
- [ ] `first mothers day stepmom 2026` — sweatshirt | "Bonus Mom" in faux embroidery style
- [ ] `mama est 2026 twins` — sweatshirt + mug | Minimalist, serif, "x2" accent

**Ops:**
- [ ] Set Etsy Ads $1/day on best 3 listings from Week 1 (if any clicks/views)
- [ ] Check Gelato mockup quality — retake any that look off

---

### Week 3 — Apr 14–20 | TEACHER + NURSES WEEK (publish for May 11 peak)
**Goal:** 8-10 listings for dual-event week (Teacher Appreciation May 4-8, Nurses Week May 6-12)

**Blue ocean teacher/nurse listings (~3 hrs):**
- [ ] `future nicu nurse est 2026` — sweatshirt + mug | Medical cross + heartbeat line, clean pro font
- [ ] `bsn nurse loading 2026` — sweatshirt + t-shirt | Progress bar graphic, navy + white
- [ ] `kindergarten teacher appreciation` — mug + tote | Colorful crayons, "Best Kinder Teacher"
- [ ] `special ed teacher gift` — mug + sweatshirt | Heart + hands motif, inclusive design
- [ ] `school counselor appreciation week` — mug + tote | Empowering text, calm blue tones
- [ ] `preschool teacher summer vibes` — sweatshirt | Fun font, sun + ABC block motif
- [ ] `icu nurse life aesthetic` — sweatshirt + t-shirt | Minimal heartbeat, dark mode aesthetic
- [ ] `nurse practitioner appreciation` — mug + sweatshirt | "NP Life" bold serif, teal accent

**Ops:**
- [ ] Review Week 1 analytics: which listings got views? Pause dead ones, promote winners
- [ ] Increase Etsy Ads budget to $2/day on top 2 performers

---

### Week 4 — Apr 21–27 | GRADUATION + MEMORIAL DAY (publish for May 25 peak)
**Goal:** 8-10 listings for graduation season + Memorial Day

**Blue ocean grad/patriotic listings (~3 hrs):**
- [ ] `proud phd grad 2026` — sweatshirt + mug | Academic seal style, elegant serif, "Dr." prominent
- [ ] `class of 2026 first gen grad` — t-shirt + sweatshirt | Bold, "First Generation Graduate"
- [ ] `nursing school grad 2026` — sweatshirt + mug | Stethoscope + diploma motif
- [ ] `kindergarten grad squad` — t-shirt set | Cute cap + gown doodle, bright colors
- [ ] `memorial day military spouse` — t-shirt + mug | Patriotic, "Proud Military Spouse"
- [ ] `proud military grandma` — sweatshirt + mug | Stars + stripes, elegant script
- [ ] `last day of school teacher 2026` — sweatshirt + mug | Summer sun, "Teacher Off Duty"
- [ ] `college grad first in family` — sweatshirt | Bold pride, raised fist motif

**Ops:**
- [ ] Run `blue_ocean_scraper` manually (biweekly — Apr 15 was first auto-run, Apr 30 is next)
- [ ] Check if any listings have first sale → double down on that niche immediately

---

### Week 5 — Apr 28–May 4 | FATHER'S DAY + PRIDE PREP (publish for Jun 8 peak)
**Goal:** 8-10 Father's Day and Pride Month listings

**Blue ocean Father's Day listings (~2 hrs):**
- [ ] `ivf dad est 2026` — t-shirt + mug | Minimalist embryo/heart, "Worth the Wait" (BO score: 78)
- [ ] `girl dad of triplets` — sweatshirt + mug | Three crowns, "Girl Dad x3" bold
- [ ] `rescue dog dad club` — t-shirt + hoodie | Paw print, distressed text, earthy tones
- [ ] `dungeon master dad of dragons` — t-shirt + mug | Fantasy font, d20 dice, dragon silhouette
- [ ] `disc golf dog dad` — t-shirt | Playful disc + paw combo, outdoor tones

**Blue ocean Pride Month listings (~1 hr):**
- [ ] `aromantic ace pride` — t-shirt + sticker | Aro/Ace flag colors, minimal design
- [ ] `neurodivergent queer pride` — t-shirt + sweatshirt | Infinity loop + pride colors
- [ ] `ally parents of trans youth` — t-shirt + tote | Heart graphic, supportive bold text

**Ops:**
- [ ] May 1 deadline: World Cup listings must be LIVE (see Week 6)
- [ ] Review 5-week performance: which niches converted? Scale those product types

---

### Week 6 — May 5–11 | WORLD CUP 2026 + JUNETEENTH (publish for Jun 22 peak)
**Goal:** 8-10 World Cup + Juneteenth listings — biggest single opportunity of summer

**World Cup blue ocean listings — URGENT (~2 hrs):**
- [ ] `world cup 2026 host city fan` — t-shirt + hoodie | City skyline + 2026 motif, national colors
- [ ] `usa world cup 2026 supporter` — t-shirt + sweatshirt | Bold "USA" + soccer ball
- [ ] `mexico world cup 2026 fan` — t-shirt + mug | Green/white/red, eagle motif
- [ ] `first world cup for us fan` — t-shirt | "My First World Cup" milestone design
- [ ] `world cup watching party host` — t-shirt + tote | Playful group design

**Juneteenth listings (~1 hr):**
- [ ] `juneteenth freedom day 2026` — t-shirt + sweatshirt | Black/red/green/gold, "June 19 1865"
- [ ] `juneteenth family reunion 2026` — t-shirt set | Afrocentric patterns, bold celebration
- [ ] `free-ish since 1865` — t-shirt + mug | Bold statement, afrocentric color palette

**Ops:**
- [ ] biweekly blue_ocean_scraper auto-runs May 15 → review new blue ocean picks
- [ ] Etsy Ads review: 5-week ROI check, pause anything with 0 sales

---

### Week 7 — May 12–18 | JULY 4TH + SUMMER (publish for Jul 6 peak)
**Goal:** 8 patriotic + summer listings

**Blue ocean July 4th / summer listings (~2 hrs):**
- [ ] `first 4th of july baby 2026` — onesie + mug | Stars + stripes, "Born in the USA" cute
- [ ] `patriotic golden retriever mom` — t-shirt + mug | Dog + flag motif, red/white/blue
- [ ] `fourth of july fishing trip` — t-shirt | Hook + flag, "Reel American"
- [ ] `cancer zodiac birthday queen` — t-shirt + mug | Celestial, crab motif, moonstone palette
- [ ] `coastal cowgirl fourth of july` — t-shirt | Western flag aesthetic, denim + bandana colors
- [ ] `national grilling month dad` — apron + mug | Bold BBQ king design
- [ ] `summer reading witch` — tote + mug | Dark academia, "Currently Reading" with cauldron
- [ ] `lake house vibes 2026` — sweatshirt + tumbler | Serene lake illustration, neutral tones

---

### Week 8 — May 19–25 | FOOTBALL SEASON PREP (publish for Jul 20 peak)
**Goal:** 8 football / back-to-school listings

**Blue ocean football / BTS listings (~2 hrs):**
- [ ] `fantasy football commissioner wife` — t-shirt + mug | Fantasy football trophy + feminine touch
- [ ] `fantasy football draft day 2026` — t-shirt | Bold "Draft Day" retro design
- [ ] `senior class 2027 first day` — sweatshirt + t-shirt | "Sr. 27" clean varsity design
- [ ] `back to school kindergarten teacher 2026` — sweatshirt + mug | Bright apple motif
- [ ] `first day of kindergarten 2026` — t-shirt (child + parent set) | Sweet milestone design
- [ ] `tailgate queen wife` — t-shirt + sweatshirt | Football + feminine "Queen" motif
- [ ] `teacher team shirt 2026-2027` — t-shirt | School colors placeholder, "Team [Grade]"
- [ ] `school staff appreciation 2026` — mug + tote | Warm appreciation design, all-staff inclusive

---

### Ongoing Weekly Ops (every week, ~30 min)
- [ ] Review Etsy analytics dashboard: views, clicks, favorites, sales
- [ ] Adjust Etsy Ads: +$0.50/day on listings with clicks but no sales; pause >2 weeks zero views
- [ ] Check for any blue ocean niche ideas from Etsy search autocomplete (manual 10-min check)
- [ ] Post 1 product to Pinterest (POD algorithm signal + free traffic)
- [ ] Update `continue.md` with session notes

### Biweekly Automation (every 2 weeks, runs automatically)
- **1st + 15th of month**: `blue_ocean_scraper` auto-runs (Celery Beat) → review new picks next day
- **Sun/Tue/Thu 23:30**: `gemini_trend_scraper` runs → fresh TrendSnapshot data
- Review DB blue ocean scores after each run: `SELECT keyword, blue_ocean_score, target_customer, recommended_products FROM niches WHERE blue_ocean_score > 60 ORDER BY blue_ocean_score DESC LIMIT 20;`
