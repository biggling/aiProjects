# Prompt: Design High-Level Python Automation for Print-on-Demand Business

## Context & Inspiration

Based on the strategy: *"How a Broke College Student Built a $2,000/Month Print-on-Demand Business in 90 Days"*

Core model:
- Find trending niches → generate designs → list on POD platforms → market organically → fulfill automatically
- Revenue from platforms: Redbubble, Merch by Amazon, Etsy + Printify/Printful
- No upfront inventory, 100% dropshipped fulfillment
- Profit from margin between platform payout and zero COGS

---

## Prompt for Claude / AI Design Session

```
Design a high-level Python automation system for a Print-on-Demand (POD) business
that can run with minimal manual intervention. The system should cover the full business
pipeline from trend discovery to order fulfillment tracking.

Break the design into clearly separated automated job modules, each independently
schedulable (cron/APScheduler). Each module should define:
- Purpose
- Inputs / Outputs
- Key Python libraries to use
- Data flow to other modules
- Scheduling cadence

Target platforms: Redbubble, Merch by Amazon, Etsy (via Printify)
Target revenue: $2,000+/month from 200-500 active listings

Constraints:
- Python 3.11+
- Use async where applicable
- Store state in SQLite or PostgreSQL
- Secrets managed via .env / python-dotenv
- Modular: each job can run standalone
```

---

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    POD AUTOMATION PIPELINE                       │
│                                                                 │
│  [Job 1]        [Job 2]        [Job 3]        [Job 4]           │
│  Trend          Design         Listing        Marketing         │
│  Research  ───► Generation ──► Publishing ──► & SEO            │
│                                                                 │
│  [Job 5]        [Job 6]        [Job 7]        [Job 8]           │
│  Order          Analytics      Competitor     Inventory         │
│  Monitoring ◄── & Reporting ◄─ Tracking  ◄─── Refresh          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Automated Job Modules

---

### Job 1: Trend Research & Niche Discovery
**Purpose:** Identify profitable, low-competition niches with high buyer intent

**Schedule:** Daily at 06:00 AM

**Inputs:**
- Seed keyword list (configurable)
- Blacklist of saturated niches

**Outputs:**
- `niches.db` table: `(niche, search_volume, competition_score, trend_score, source, discovered_at)`

**Tasks:**
- Scrape Google Trends via `pytrends` for rising keywords
- Scrape Pinterest trending topics via `requests` + `BeautifulSoup`
- Scrape Etsy bestsellers by category using Etsy API or scraper
- Scrape Redbubble trending tags
- Score niches: (trend_velocity × search_volume) / competition
- Filter: score > threshold AND not in blacklist
- Output top 20 niches to queue for Job 2

**Libraries:**
```
pytrends, requests, beautifulsoup4, selenium, pandas, sqlite3
```

---

### Job 2: AI Design Generation
**Purpose:** Auto-generate print-ready designs for top niches using AI

**Schedule:** Daily at 08:00 AM (after Job 1)

**Inputs:**
- Top niches from `niches.db`
- Design style templates (minimalist, vintage, funny quote, etc.)
- Product type targets (t-shirt, mug, sticker, poster)

**Outputs:**
- PNG/SVG design files saved to `/designs/{niche}/`
- `designs.db` table: `(design_id, niche, style, file_path, status, created_at)`

**Tasks:**
- For each niche, generate 3-5 design variations
- Text-based designs: use `Pillow` + font library for quote/typography designs
- Image designs: call OpenAI DALL-E 3 or Stability AI API
- Generate taglines and slogans via Claude API (`anthropic`)
- Validate output: min 4500×5400px, RGB, < 200MB
- Upscale low-res outputs via Real-ESRGAN API if needed
- Save metadata to `designs.db` with status=`ready`

**Libraries:**
```
Pillow, anthropic, openai, requests, boto3 (S3 for storage)
```

---

### Job 3: Listing Publisher
**Purpose:** Auto-publish approved designs to POD platforms with SEO-optimized listings

**Schedule:** Daily at 10:00 AM (after Job 2)

**Inputs:**
- Designs with status=`ready` from `designs.db`
- Platform credentials (Etsy API, Redbubble, Merch by Amazon)

**Outputs:**
- Published listings on target platforms
- `listings.db` table: `(listing_id, design_id, platform, url, title, tags, price, published_at, status)`

**Tasks:**
- For each design, generate SEO listing via Claude API:
  - Title (include primary keyword first)
  - Description (150-200 words, keyword-rich)
  - Tags/keywords (13 for Etsy, 7 for Redbubble)
  - Bullet points (Amazon format)
- Upload to Etsy via Etsy API v3 + Printify product sync
- Upload to Redbubble via browser automation (`playwright`)
- Upload to Merch by Amazon via `selenium` (no official API)
- Set pricing by platform margin formula:
  - Etsy: base_cost × 3.5 + $3.99 shipping
  - Amazon: base_cost × 2.8
  - Redbubble: standard 20% markup
- Log all published URLs to `listings.db`

**Libraries:**
```
anthropic, requests, playwright, selenium, Pillow
```

---

### Job 4: SEO & Marketing Automation
**Purpose:** Drive organic traffic via Pinterest, Reddit, and social media

**Schedule:** Every 6 hours

**Inputs:**
- Published listings from `listings.db`
- Platform-specific templates

**Outputs:**
- Posted pins, posts, and content across channels
- `marketing_log.db` table: `(post_id, listing_id, platform, content, posted_at, clicks)`

**Tasks:**
- Pinterest: auto-pin each listing with keyword-rich description via Pinterest API
- Reddit: post in relevant subreddits (r/designshirts, niche subreddits) with value-first approach
- TikTok/Instagram: generate short caption for product mockup images
- Create mockup images using `Pillow` + mockup template PNGs
- A/B test 2 titles per listing, track CTR weekly
- Post schedule: stagger 30 min apart to avoid spam flags

**Libraries:**
```
pinterest-api-client, praw (Reddit), requests, Pillow, schedule
```

---

### Job 5: Order & Fulfillment Monitor
**Purpose:** Monitor incoming orders and confirm auto-fulfillment status

**Schedule:** Every 2 hours

**Inputs:**
- Platform order webhooks or API polling
- Printify/Printful fulfillment API

**Outputs:**
- `orders.db` table: `(order_id, platform, product, qty, revenue, cost, profit, fulfillment_status, updated_at)`

**Tasks:**
- Poll Etsy API for new orders
- Poll Merch by Amazon Sales Dashboard (scraper fallback)
- Poll Redbubble earnings API
- Confirm Printify has auto-routed to print partner
- Alert via email/Slack if fulfillment status stuck > 48h
- Calculate profit per order: `revenue - platform_fee - print_cost`
- Update `orders.db` and trigger daily summary

**Libraries:**
```
requests, smtplib, slack-sdk, sqlite3
```

---

### Job 6: Analytics & Reporting
**Purpose:** Track KPIs and generate daily/weekly business reports

**Schedule:** Daily at 11:59 PM

**Inputs:**
- `orders.db`, `listings.db`, `marketing_log.db`

**Outputs:**
- Daily report: revenue, profit, top listings, conversion rate
- Weekly report: niche performance, best platforms, ROI per design
- Exported CSV + HTML email report

**Tasks:**
- Aggregate daily sales by platform, niche, product type
- Calculate metrics:
  - Revenue, profit, margin %
  - Listings live vs. paused
  - Best-performing niches (profit/listing)
  - Marketing ROI (clicks per pin/post)
- Generate visual charts via `matplotlib` or `plotly`
- Send HTML email report via `smtplib` or SendGrid
- Write summary to `reports/YYYY-MM-DD.md`

**Libraries:**
```
pandas, matplotlib, plotly, smtplib, jinja2, sqlite3
```

---

### Job 7: Competitor & Market Intelligence
**Purpose:** Monitor competitor listings to find pricing and keyword gaps

**Schedule:** Weekly on Sunday at 07:00 AM

**Inputs:**
- Top niches from `niches.db`
- Competitor store URLs (manual seed list)

**Outputs:**
- `competitor.db` table: `(niche, competitor, title, price, reviews, tags, scraped_at)`

**Tasks:**
- Scrape top 20 Etsy listings per niche (title, price, tags, reviews)
- Scrape Redbubble top sellers per tag
- Identify keyword gaps: tags competitors use that we don't
- Flag niches where top competitor has < 100 reviews (opportunity)
- Update our listings' tags if better keywords found
- Export competitor analysis report to CSV

**Libraries:**
```
requests, beautifulsoup4, selenium, pandas, sqlite3
```

---

### Job 8: Listing Refresh & Optimization
**Purpose:** Re-optimize underperforming listings with new titles, tags, and designs

**Schedule:** Weekly on Wednesday at 09:00 AM

**Inputs:**
- `listings.db` + `orders.db` (join on listing_id)
- Competitor keyword gaps from Job 7

**Outputs:**
- Updated listings on platforms
- `listings.db` status updated to `optimized`

**Tasks:**
- Identify listings with 0 sales after 30 days
- Re-generate title/tags using latest niche keywords + competitor gaps
- Update listing on Etsy via API
- Update Redbubble via automation
- For listings with 0 sales after 60 days → mark `paused`, remove from platform
- Test new design variant for paused niches (trigger Job 2)
- Log all changes to `optimization_log.db`

**Libraries:**
```
anthropic, requests, playwright, sqlite3, pandas
```

---

## Data Store Schema (SQLite)

```sql
-- niches.db
CREATE TABLE niches (
    id INTEGER PRIMARY KEY,
    niche TEXT UNIQUE,
    search_volume INTEGER,
    competition_score REAL,
    trend_score REAL,
    source TEXT,
    status TEXT DEFAULT 'active',
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- designs.db
CREATE TABLE designs (
    id INTEGER PRIMARY KEY,
    niche_id INTEGER REFERENCES niches(id),
    style TEXT,
    product_type TEXT,
    file_path TEXT,
    status TEXT DEFAULT 'ready',  -- ready | published | rejected
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- listings.db
CREATE TABLE listings (
    id INTEGER PRIMARY KEY,
    design_id INTEGER REFERENCES designs(id),
    platform TEXT,  -- etsy | redbubble | amazon
    external_id TEXT,
    url TEXT,
    title TEXT,
    tags TEXT,
    price REAL,
    status TEXT DEFAULT 'active',  -- active | paused | optimized
    published_at TIMESTAMP,
    last_optimized_at TIMESTAMP
);

-- orders.db
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    listing_id INTEGER REFERENCES listings(id),
    platform TEXT,
    qty INTEGER,
    revenue REAL,
    platform_fee REAL,
    print_cost REAL,
    profit REAL,
    fulfillment_status TEXT,
    order_date TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Project File Structure

```
autoPOD/
├── .env                        # API keys and credentials
├── requirements.txt
├── main.py                     # Orchestrator / job runner
├── scheduler.py                # APScheduler config for all jobs
├── database/
│   └── models.py               # SQLite/SQLAlchemy models
├── jobs/
│   ├── job1_trend_research.py
│   ├── job2_design_generation.py
│   ├── job3_listing_publisher.py
│   ├── job4_seo_marketing.py
│   ├── job5_order_monitor.py
│   ├── job6_analytics.py
│   ├── job7_competitor_intel.py
│   └── job8_listing_refresh.py
├── utils/
│   ├── image_utils.py          # Pillow helpers, mockup generator
│   ├── ai_utils.py             # Claude/OpenAI API wrappers
│   ├── platform_api.py         # Etsy, Printify, Redbubble clients
│   └── notify.py               # Email/Slack alerts
├── designs/                    # Generated design files
├── reports/                    # Daily markdown + CSV reports
└── logs/                       # Per-job log files
```

---

## Tech Stack Summary

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Scheduling | APScheduler |
| AI - Text | Anthropic Claude API (claude-sonnet-4-6) |
| AI - Image | OpenAI DALL-E 3 / Stability AI |
| Image editing | Pillow |
| Web scraping | BeautifulSoup4, Selenium, Playwright |
| Trend data | pytrends, Etsy API |
| Platform APIs | Etsy API v3, Printify API, Pinterest API |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Reporting | pandas, matplotlib, Jinja2 |
| Notifications | smtplib, slack-sdk |
| Config | python-dotenv |

---

## 90-Day Milestone Plan

| Days | Focus | Goal |
|---|---|---|
| 1-10 | Setup Jobs 1-3 (research → design → publish) | 50 listings live |
| 11-30 | Add Job 4 (marketing) + monitor Jobs 5-6 | 150 listings, first sales |
| 31-60 | Add Jobs 7-8 (optimize + competitor intel) | 300 listings, $500/mo |
| 61-90 | Scale top niches, add Amazon channel | 500 listings, $2,000/mo |

---

## Next Steps

1. Run this prompt through Claude to generate boilerplate code for each job module
2. Set up `.env` with Etsy API, Printify API, Anthropic API keys
3. Initialize SQLite schema with `database/models.py`
4. Test Job 1 (trend research) in isolation first
5. Build mock versions of each job before connecting real APIs
