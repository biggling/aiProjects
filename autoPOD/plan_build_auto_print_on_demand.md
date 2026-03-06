# Build Plan: autoPOD - Python Print-on-Demand Automation

**Goal:** $2,000+/month POD business via 200-500 active listings
**Target Platforms:** Etsy (via Printify), Redbubble, Merch by Amazon
**Reference Prompt:** `prompt_auto_print_on_demand.md`
**Status:** Planning Phase

---

## Phase Overview

| Phase | Days | Focus | Milestone |
|---|---|---|---|
| Phase 1 | 1–7 | Foundation: project setup, DB, config | Infra ready |
| Phase 2 | 8–14 | Job 1: Trend Research | Niche data flowing |
| Phase 3 | 15–21 | Job 2: AI Design Generation | Designs generating |
| Phase 4 | 22–28 | Job 3: Listing Publisher | Listings going live |
| Phase 5 | 29–35 | Job 4: SEO & Marketing | Traffic channels active |
| Phase 6 | 36–42 | Jobs 5–6: Orders & Analytics | Business monitored |
| Phase 7 | 43–56 | Jobs 7–8: Competitor Intel + Refresh | Optimization loop |
| Phase 8 | 57–90 | Scale, tune, add Amazon channel | $2,000/month target |

---

## Phase 1: Foundation (Days 1–7)

### 1.1 Project Scaffold

**Deliverables:**
- Project directory structure (as defined in prompt)
- `.env.example` with all required API keys documented
- `requirements.txt` with pinned versions
- `README.md` with setup instructions

**Directory Structure:**
```
autoPOD/
├── .env                        # Never commit
├── .env.example                # Template for secrets
├── requirements.txt
├── main.py                     # Entry point / orchestrator
├── scheduler.py                # APScheduler job registry
├── config.py                   # Load .env, global constants
├── database/
│   ├── __init__.py
│   ├── models.py               # SQLAlchemy ORM models
│   └── init_db.py              # Schema creation script
├── jobs/
│   ├── __init__.py
│   ├── job1_trend_research.py
│   ├── job2_design_generation.py
│   ├── job3_listing_publisher.py
│   ├── job4_seo_marketing.py
│   ├── job5_order_monitor.py
│   ├── job6_analytics.py
│   ├── job7_competitor_intel.py
│   └── job8_listing_refresh.py
├── utils/
│   ├── __init__.py
│   ├── image_utils.py
│   ├── ai_utils.py
│   ├── platform_api.py
│   └── notify.py
├── designs/
├── reports/
├── logs/
└── tests/
    └── test_*.py               # One test file per job
```

### 1.2 Database Setup

**Engine:** SQLite (dev) with SQLAlchemy ORM
**Migration path:** SQLAlchemy models + Alembic for schema versioning

**Tables to create:**
1. `niches` — trend research results
2. `designs` — generated design metadata
3. `listings` — published platform listings
4. `orders` — sales + fulfillment tracking
5. `competitor` — competitor scraped data
6. `marketing_log` — social media posts
7. `optimization_log` — listing refresh history

**init_db.py** must be idempotent (CREATE TABLE IF NOT EXISTS).

### 1.3 Config & Secrets

**Required API Keys (`.env.example`):**
```
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
ETSY_API_KEY=
ETSY_API_SECRET=
ETSY_ACCESS_TOKEN=
ETSY_SHOP_ID=
PRINTIFY_API_KEY=
REDBUBBLE_EMAIL=
REDBUBBLE_PASSWORD=
PINTEREST_API_KEY=
SLACK_WEBHOOK_URL=
SENDGRID_API_KEY=
SENDER_EMAIL=
RECIPIENT_EMAIL=
```

**`config.py` responsibilities:**
- Load `.env` via `python-dotenv`
- Validate required keys on startup
- Expose typed constants (paths, thresholds, schedule times)

### 1.4 Requirements

**Core packages:**
```
anthropic>=0.25.0
openai>=1.30.0
apscheduler>=3.10.0
sqlalchemy>=2.0.0
alembic>=1.13.0
python-dotenv>=1.0.0
```

**Scraping:**
```
pytrends>=4.9.2
requests>=2.31.0
beautifulsoup4>=4.12.0
selenium>=4.20.0
playwright>=1.44.0
```

**Image processing:**
```
Pillow>=10.3.0
rembg>=2.0.57
```

**Data & reporting:**
```
pandas>=2.2.0
matplotlib>=3.9.0
plotly>=5.22.0
jinja2>=3.1.0
```

**Platform clients:**
```
praw>=7.7.1
slack-sdk>=3.27.0
sendgrid>=6.11.0
```

---

## Phase 2: Job 1 — Trend Research (Days 8–14)

### 2.1 Design

**File:** `jobs/job1_trend_research.py`
**Schedule:** Daily at 06:00 AM

**Data sources (priority order):**
1. Google Trends via `pytrends` — rising queries for seed keywords
2. Etsy API — bestsellers by category (top 100 per category)
3. Pinterest trending topics — scraper with `requests` + `BeautifulSoup`
4. Redbubble trending tags — scraper fallback (no official API)

**Scoring formula:**
```
score = (trend_velocity * search_volume) / (competition_score + 1)
```
- `trend_velocity`: % rise over past 7 days from pytrends
- `search_volume`: monthly estimate (pytrends interest value 0–100)
- `competition_score`: count of existing Etsy listings for keyword

**Output:**
- Top 20 niches per run written to `niches` table
- Status set to `active`
- Duplicate niches upserted (update score, don't insert duplicate)

**Implementation steps:**
1. Build `pytrends` wrapper: batch keyword requests with rate-limit backoff
2. Build Etsy bestseller scraper (use official API first, scraper as fallback)
3. Build Pinterest scraper (static HTML parsing, no login required)
4. Implement scoring + ranking logic
5. Write to SQLite via SQLAlchemy
6. Unit test with mocked HTTP responses

### 2.2 Rate Limiting Strategy

- `pytrends`: 1 request per 5s, rotate user agents
- Etsy API: 10 requests/second limit — use `asyncio` + `aiohttp`
- Pinterest: 2s delay between requests, randomize between 1.5–3.5s
- Redbubble: browser automation via `selenium`, 3s page load wait

---

## Phase 3: Job 2 — AI Design Generation (Days 15–21)

### 3.1 Design

**File:** `jobs/job2_design_generation.py`
**Schedule:** Daily at 08:00 AM

**Design types:**
| Type | Tool | Use Case |
|---|---|---|
| Typography/Quote | Pillow + fonts | Funny quotes, minimalist text |
| Illustrated | DALL-E 3 / Stability AI | Animals, nature, abstract |
| Hybrid | DALL-E 3 + Pillow overlay | Image + text combination |

**Pillow typography workflow:**
1. Load base canvas (4500×5400px, white/transparent)
2. Select font from curated font library (TTF files committed to repo)
3. Generate text layout (word-wrap, centering, sizing)
4. Apply color palette from niche mood mapping
5. Export as PNG (300 DPI)

**DALL-E 3 workflow:**
1. Construct prompt via Claude API: `"Create a [style] design for [niche] POD product: [brief]"`
2. Request 1024×1024 image
3. Upscale to 4500px using Real-ESRGAN API or `Pillow` bicubic
4. Validate dimensions and file size
5. Remove background if needed via `rembg`

**Validation checklist:**
- Min resolution: 4500×5400px
- Color mode: RGB
- Format: PNG
- File size: < 200MB

**Output:** `designs/{niche_slug}/{design_id}.png` + DB record

### 3.2 Claude API Usage

**Model:** `claude-sonnet-4-6`
**Tasks:**
- Generate design brief (style, mood, colors, elements)
- Generate 3 DALL-E prompt variations per niche
- Generate taglines and quotes for typography designs

**Prompt template for design brief:**
```
You are a POD design expert. Given the niche "{niche}", generate:
1. A design brief (50 words): visual style, mood, color palette
2. Three DALL-E 3 prompts for print-ready artwork
3. Five catchy text/quote ideas for typography designs
Format as JSON.
```

---

## Phase 4: Job 3 — Listing Publisher (Days 22–28)

### 4.1 Design

**File:** `jobs/job3_listing_publisher.py`
**Schedule:** Daily at 10:00 AM

**Platform publishing sequence:**
1. **Etsy via Printify** — highest margin, official API
2. **Redbubble** — Playwright automation (no official publisher API)
3. **Merch by Amazon** — Selenium automation (no public API)

**Etsy + Printify workflow:**
1. Call Printify API to create product (upload design, select product type)
2. Get Printify `product_id`
3. Publish to Etsy via Printify's Etsy integration
4. Verify listing live via Etsy API read
5. Save listing URL + `external_id` to `listings` table

**SEO listing generation (Claude API):**
```
Given niche "{niche}" and design style "{style}", generate an Etsy listing:
- Title: max 140 chars, primary keyword first
- Description: 150-200 words, storytelling + keyword-rich
- Tags: exactly 13 comma-separated keywords
- Bullet points: 5 Amazon-style feature bullets
Format as JSON.
```

**Pricing formula:**
```
etsy_price = (printify_base_cost * 3.5) + 3.99
amazon_price = printify_base_cost * 2.8
redbubble_price = standard + 20% artist margin
```

**Publish rate limit:** Max 10 new listings per day across all platforms (avoid flags).

### 4.2 Browser Automation Strategy

- **Redbubble:** Playwright with persistent browser session (cookies saved)
- **Amazon:** Selenium + Chrome, headless mode with anti-detection patches
- Use `undetected-chromedriver` for Amazon to bypass bot detection
- Session state saved to `sessions/` directory (gitignored)

---

## Phase 5: Job 4 — SEO & Marketing (Days 29–35)

### 5.1 Design

**File:** `jobs/job4_seo_marketing.py`
**Schedule:** Every 6 hours

**Channels:**
| Channel | Tool | Content Type |
|---|---|---|
| Pinterest | Pinterest API v5 | Product pins with listing URL |
| Reddit | PRAW | Text posts in niche subreddits |
| Instagram/TikTok | Manual export queue | Mockup images (future automation) |

**Mockup generation workflow:**
1. Load mockup template PNG (t-shirt, mug, tote — stored in `assets/mockups/`)
2. Place design on mockup using `Pillow` composite
3. Adjust placement, scale, perspective
4. Export to `designs/{niche}/mockup_{product}.png`

**Pinterest pin workflow:**
1. Create board per niche (if not exists)
2. POST pin via Pinterest API: image URL, description (keyword-rich), link to listing
3. Schedule 4 pins per niche per day (stagger 6h apart)

**Reddit post strategy:**
- Target subreddits: r/findfashion, r/designshirts + niche-specific
- Post format: "I made this [niche] design, feedback welcome" with mockup image
- Rate: max 1 post per subreddit per 7 days

---

## Phase 6: Jobs 5–6 — Orders & Analytics (Days 36–42)

### 6.1 Job 5: Order Monitor

**File:** `jobs/job5_order_monitor.py`
**Schedule:** Every 2 hours

**Data collection:**
- Etsy: poll `/v3/application/shops/{shop_id}/receipts` API endpoint
- Redbubble: scrape earnings dashboard (no public API)
- Amazon: scrape KDP/Merch dashboard (Selenium)

**Alert conditions:**
- New order received → Slack notification
- Fulfillment status stuck > 48h → Email alert
- Daily revenue milestone hit → Slack

### 6.2 Job 6: Analytics & Reporting

**File:** `jobs/job6_analytics.py`
**Schedule:** Daily at 11:59 PM

**Report sections:**
1. Daily summary: revenue, profit, margin, order count
2. Top 10 listings by revenue
3. Platform breakdown (Etsy vs. Amazon vs. Redbubble)
4. Niche performance (profit per listing by niche)
5. Marketing ROI (clicks per pin/post)

**Output formats:**
- Markdown file: `reports/YYYY-MM-DD.md`
- HTML email via SendGrid / smtplib + Jinja2 template
- Charts as PNG attachments via `matplotlib`

---

## Phase 7: Jobs 7–8 — Intelligence & Optimization (Days 43–56)

### 7.1 Job 7: Competitor Intel

**File:** `jobs/job7_competitor_intel.py`
**Schedule:** Weekly Sunday 07:00 AM

**Scraping targets:**
- Etsy: top 20 results per niche keyword (title, price, tags, review count)
- Redbubble: top tags per niche category

**Opportunity detection:**
- Niche flagged as opportunity if: top competitor < 100 reviews AND score > threshold
- Keyword gap: tags used by competitors not in our listings → feed to Job 8

### 7.2 Job 8: Listing Refresh

**File:** `jobs/job8_listing_refresh.py`
**Schedule:** Weekly Wednesday 09:00 AM

**Refresh triggers:**
- Listing age > 30 days AND 0 sales → regenerate title/tags
- Listing age > 60 days AND 0 sales → pause, mark for new design variant
- Keyword gap detected from Job 7 → update tags via Etsy API

---

## Phase 8: Scheduler & Orchestration

**File:** `scheduler.py` + `main.py`

**APScheduler setup:**
```
JobStore: SQLAlchemyJobStore (persists across restarts)
Executor: ThreadPoolExecutor(max_workers=4)
Timezone: UTC
```

**Job registry:**
| Job | Trigger | Interval |
|---|---|---|
| job1_trend_research | cron | Daily 06:00 UTC |
| job2_design_generation | cron | Daily 08:00 UTC |
| job3_listing_publisher | cron | Daily 10:00 UTC |
| job4_seo_marketing | interval | Every 6 hours |
| job5_order_monitor | interval | Every 2 hours |
| job6_analytics | cron | Daily 23:59 UTC |
| job7_competitor_intel | cron | Weekly Sun 07:00 UTC |
| job8_listing_refresh | cron | Weekly Wed 09:00 UTC |

**main.py responsibilities:**
- CLI: `python main.py --job 1` to run individual job
- CLI: `python main.py --scheduler` to start full scheduler
- CLI: `python main.py --init-db` to initialize schema
- Logging: rotating file per job (`logs/job{N}.log`)

---

## Dependencies Between Jobs

```
Job 1 (Trends)
    └──► Job 2 (Designs)
              └──► Job 3 (Publisher) ──► Job 4 (Marketing)
                        └──► Job 5 (Orders)
                                  └──► Job 6 (Analytics)
Job 7 (Competitor) ──► Job 8 (Refresh) ──► Job 3 (re-publish)
```

**Database is the integration layer** — each job reads/writes SQLite tables.
No direct function calls between jobs — fully decoupled.

---

## Testing Strategy

| Level | Tool | Coverage |
|---|---|---|
| Unit | `pytest` + `unittest.mock` | Each job function, DB writes |
| Integration | `pytest` + SQLite in-memory | Full job run with mocked APIs |
| End-to-end | Manual | Real API calls with sandbox credentials |

**Mock strategy:**
- Mock all external HTTP calls with `responses` library
- Mock Claude API with fixture JSON responses
- Use in-memory SQLite for DB tests (`sqlite:///:memory:`)

---

## Risk & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Etsy API rate limits | Listing failures | Exponential backoff, queue retry |
| DALL-E cost overrun | Budget | Max 5 images/day limit in config |
| Redbubble bot detection | Account ban | Slow automation, human-like delays |
| Amazon TOS violation | Account suspension | Manual review before automation |
| pytrends blocking | No niche data | Rotate proxies, fallback to Etsy data |
| API key expiry | All jobs fail | Health check job, alert on 401 errors |

---

## Build Order (Recommended)

1. **Phase 1** — Scaffold + DB + Config (prerequisite for everything)
2. **Job 1** — Trend Research (data foundation)
3. **Job 6** — Analytics shell (test DB reads early)
4. **Job 2** — Design Generation (text-only Pillow first, DALL-E second)
5. **Job 3** — Listing Publisher (Etsy/Printify first, others later)
6. **Job 4** — SEO/Marketing (Pinterest first, Reddit second)
7. **Job 5** — Order Monitor (polling only, alerts)
8. **Jobs 7–8** — Competitor Intel + Refresh (after listings are live)
9. **Scheduler** — Wire all jobs with APScheduler last

---

## Success Metrics

| Metric | Week 2 | Week 4 | Week 8 | Week 12 |
|---|---|---|---|---|
| Listings live | 20 | 100 | 300 | 500 |
| Designs generated | 30 | 150 | 400 | 700 |
| Daily revenue | $0 | $5 | $30 | $70 |
| Monthly revenue | — | $50 | $500 | $2,000 |

---

## Status Log

| Date | Phase | Status | Notes |
|---|---|---|---|
| 2026-03-06 | Planning | Complete | plan_build_auto_print_on_demand.md created |
| 2026-03-06 | Phase 1: Scaffold | Complete | config.py, requirements.txt, .env.example, dirs |
| 2026-03-06 | Phase 1: DB Models | Complete | models.py (7 tables), init_db.py |
| 2026-03-06 | Phase 1: Utils | Complete | ai_utils.py, image_utils.py, platform_api.py, notify.py |
| 2026-03-06 | Job 1: Trends | Complete | job1_trend_research.py — pytrends + Etsy + Redbubble |
| 2026-03-06 | Job 2: Designs | Complete | job2_design_generation.py — Pillow + DALL-E 3 |
| 2026-03-06 | Job 3: Publisher | Complete | job3_listing_publisher.py — Etsy via Printify |
| 2026-03-06 | Job 4: Marketing | Complete | job4_seo_marketing.py — Pinterest + Reddit |
| 2026-03-06 | Job 5: Orders | Complete | job5_order_monitor.py — Etsy polling + alerts |
| 2026-03-06 | Job 6: Analytics | Complete | job6_analytics.py — HTML report + markdown |
| 2026-03-06 | Job 7: Competitor | Complete | job7_competitor_intel.py — Etsy scraper |
| 2026-03-06 | Job 8: Refresh | Complete | job8_listing_refresh.py — tag refresh + pause |
| 2026-03-06 | Scheduler | Complete | scheduler.py + main.py CLI |
| 2026-03-06 | Tests | Complete | test_job1.py, test_models.py |
| 2026-03-06 | Verification | Complete | Session resumed after context limit — all files verified present and non-stub |

## Next Steps for Production
1. `python main.py --init-db` — initialize SQLite schema
2. Copy `.env.example` to `.env` and fill all API keys
3. Run `pip install -r requirements.txt`
4. Test individually: `python main.py --job 1`
5. Start scheduler: `python main.py --scheduler`
6. Download font TTF files to `assets/fonts/`
7. Add product mockup PNG templates to `assets/mockups/`
