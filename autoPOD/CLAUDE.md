# autoPOD — Claude Session Context

## Project Goal
Automate Print-on-Demand business: $2,000+/month via 200–500 active listings on Etsy, Redbubble, Amazon Merch.

## Build Status (2026-03-06) — ALL COMPLETE (verified 2026-03-06 after session resume)

| Component | File | Status |
|---|---|---|
| Config & Env | `config.py`, `.env.example`, `requirements.txt` | Complete |
| DB Models | `database/models.py` (7 tables) | Complete |
| DB Init | `database/init_db.py` | Complete |
| Job 1: Trend Research | `jobs/job1_trend_research.py` | Complete |
| Job 2: Design Generation | `jobs/job2_design_generation.py` | Complete |
| Job 3: Listing Publisher | `jobs/job3_listing_publisher.py` | Complete |
| Job 4: SEO & Marketing | `jobs/job4_seo_marketing.py` | Complete |
| Job 5: Order Monitor | `jobs/job5_order_monitor.py` | Complete |
| Job 6: Analytics | `jobs/job6_analytics.py` | Complete |
| Job 7: Competitor Intel | `jobs/job7_competitor_intel.py` | Complete |
| Job 8: Listing Refresh | `jobs/job8_listing_refresh.py` | Complete |
| Scheduler | `scheduler.py` | Complete |
| CLI Entry | `main.py` | Complete |
| Utils | `utils/` (4 modules) | Complete |
| Tests | `tests/test_job1.py`, `tests/test_models.py` | Complete |

## Key Architecture
- **DB:** SQLite (dev) via SQLAlchemy — 7 tables: `niches`, `designs`, `listings`, `orders`, `competitor`, `marketing_log`, `optimization_log`
- **AI:** Claude `claude-sonnet-4-6` for design briefs, listing copy, DALL-E 3 prompts
- **Design Gen:** Pillow (typography) + DALL-E 3 (illustrated) + rembg (background removal)
- **Publishing:** Etsy via Printify API (primary), Redbubble via Playwright, Amazon via Selenium
- **Marketing:** Pinterest API v5, Reddit via PRAW
- **Scheduler:** APScheduler (SQLAlchemyJobStore for persistence)

## Job Schedule
| Job | Trigger |
|---|---|
| Job 1 (Trend Research) | Daily 06:00 UTC |
| Job 2 (Design Gen) | Daily 08:00 UTC |
| Job 3 (Listing Publisher) | Daily 10:00 UTC |
| Job 4 (SEO/Marketing) | Every 6 hours |
| Job 5 (Order Monitor) | Every 2 hours |
| Job 6 (Analytics) | Daily 23:59 UTC |
| Job 7 (Competitor Intel) | Weekly Sun 07:00 UTC |
| Job 8 (Listing Refresh) | Weekly Wed 09:00 UTC |

## Job Dependencies
```
Job 1 (Trends) → Job 2 (Designs) → Job 3 (Publisher) → Job 4 (Marketing)
                                         └→ Job 5 (Orders) → Job 6 (Analytics)
Job 7 (Competitor) → Job 8 (Refresh) → Job 3 (re-publish)
```

## Setup for Production
```bash
python main.py --init-db
cp .env.example .env  # fill API keys
pip install -r requirements.txt
playwright install chromium
# Download TTF fonts to assets/fonts/
# Add mockup PNGs to assets/mockups/
python main.py --job 1   # test Job 1
python main.py --scheduler  # start all jobs
```

## Required API Keys (.env)
- `ANTHROPIC_API_KEY` — design briefs + listing copy
- `OPENAI_API_KEY` — DALL-E 3 image generation
- `ETSY_API_KEY` / `ETSY_API_SECRET` / `ETSY_ACCESS_TOKEN` / `ETSY_SHOP_ID`
- `PRINTIFY_API_KEY` — product creation + Etsy publishing
- `REDBUBBLE_EMAIL` / `REDBUBBLE_PASSWORD` — browser automation
- `PINTEREST_API_KEY` — pin creation
- `SLACK_WEBHOOK_URL` — order + alert notifications
- `SENDGRID_API_KEY` — daily report emails

## Pricing Formula
```
etsy_price   = (printify_base_cost × 3.5) + 3.99
amazon_price = printify_base_cost × 2.8
redbubble    = standard + 20% artist margin
```

## Design Specs (CRITICAL)
- Canvas: 4500×5400px, RGB, PNG, <200MB
- Pillow workflow: load base → font → layout → color palette → export 300 DPI
- DALL-E output: 1024px → upscale to 4500px via bicubic

## Rate Limits
- Max 10 new listings/day across all platforms
- Redbubble: human-like delays (3–5s between actions)
- Amazon: undetected-chromedriver, session saved to `sessions/`

## Reference
- Build plan: `plan_build_auto_print_on_demand.md`
- Design prompt: `prompt_auto_print_on_demand.md`
