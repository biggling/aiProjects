# POD Business — Implementation Plan for Claude

> **Purpose:** This file is the single source of truth for implementing the full POD automation system.
> When starting any task, Claude must read this file first, identify the current phase and step, implement it, then mark it `[x]` before moving on.
> Never skip steps. Never implement a step whose dependencies are not yet marked `[x]`.

---

## How Claude Should Use This File

1. Read this entire file before writing any code
2. Find the first unchecked `[ ]` step
3. Check its dependencies — all must be `[x]`
4. Implement exactly what the step describes — no more, no less
5. Write tests where indicated
6. Mark the step `[x]` when done
7. Commit with message format: `feat(phase-N): <step title>`
8. Move to the next step

---

## Project Root Layout

```
pod/
├── plan.md                  ← this file (always keep updated)
├── .env.example             ← API key template (never commit .env)
├── docker-compose.yml
├── requirements.txt
├── tools/                   ← all Python automation scripts
│   ├── trend/
│   ├── design/
│   ├── copy/
│   ├── upload/
│   ├── analytics/
│   └── shared/
├── app/                     ← FastAPI dashboard
│   ├── main.py
│   ├── templates/
│   └── static/
├── data/
│   ├── pod.db               ← SQLite (auto-created)
│   ├── designs/
│   │   ├── raw/
│   │   ├── processed/
│   │   └── mockups/
│   └── logs/
├── celery_app.py            ← Celery + Beat config
├── tasks.py                 ← all Celery task definitions
├── schedule.py              ← Beat schedule (mirrors weekly plan)
├── backup.sh
└── tests/
```

---

## Environment Variables

All secrets go in `.env`. Never hardcode. Always load with `python-dotenv`.

```bash
# .env.example — copy to .env and fill in

# AI
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
STABILITY_API_KEY=

# Etsy
ETSY_API_KEY=
ETSY_SHOP_ID=

# Printify
PRINTIFY_API_KEY=
PRINTIFY_SHOP_ID=

# Reddit
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=pod-bot/1.0

# Social
BUFFER_ACCESS_TOKEN=
META_ACCESS_TOKEN=
META_PAGE_ID=

# Notifications
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Storage
S3_BUCKET=
S3_ACCESS_KEY=
S3_SECRET_KEY=
S3_ENDPOINT_URL=           # Backblaze B2 or AWS

# App
DATABASE_URL=sqlite:///data/pod.db
REDIS_URL=redis://redis:6379/0
DASHBOARD_USER=admin
DASHBOARD_PASS=changeme
```

---

## Tech Stack & Versions

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.11 | core |
| fastapi | 0.110+ | dashboard |
| uvicorn | latest | ASGI server |
| celery | 5.3+ | task queue |
| redis | 7+ | broker |
| sqlalchemy | 2.0+ | ORM |
| alembic | latest | DB migrations |
| pytrends | latest | Google Trends |
| praw | latest | Reddit API |
| playwright | latest | web automation |
| anthropic | latest | Claude API |
| openai | latest | DALL-E / GPT |
| rembg | latest | bg removal |
| Pillow | latest | image processing |
| requests | latest | HTTP |
| python-dotenv | latest | env loading |
| apprise | latest | notifications |
| pytest | latest | testing |

---

## Database Schema

Claude must create these tables via SQLAlchemy models + Alembic migration.

```python
# tools/shared/models.py

class Niche(Base):
    __tablename__ = "niches"
    id            = Column(Integer, primary_key=True)
    keyword       = Column(String, unique=True, index=True)
    trend_score   = Column(Float)      # pytrends interest score
    velocity      = Column(Float)      # week-over-week change
    competition   = Column(Float)      # estimated saturation 0–1
    final_score   = Column(Float)      # volume × velocity ÷ competition
    status        = Column(String, default="active")  # active/paused/killed
    created_at    = Column(DateTime, default=func.now())
    updated_at    = Column(DateTime, onupdate=func.now())

class Prompt(Base):
    __tablename__ = "prompts"
    id            = Column(Integer, primary_key=True)
    niche_id      = Column(Integer, ForeignKey("niches.id"))
    prompt_text   = Column(Text)
    status        = Column(String, default="pending")  # pending/generated/failed
    created_at    = Column(DateTime, default=func.now())

class Design(Base):
    __tablename__ = "designs"
    id            = Column(Integer, primary_key=True)
    prompt_id     = Column(Integer, ForeignKey("prompts.id"))
    niche_id      = Column(Integer, ForeignKey("niches.id"))
    raw_path      = Column(String)
    processed_path= Column(String)
    mockup_path   = Column(String)
    clip_score    = Column(Float)
    status        = Column(String, default="pending")
    # pending → generated → approved/rejected → processed → mockup_ready
    created_at    = Column(DateTime, default=func.now())

class Listing(Base):
    __tablename__ = "listings"
    id            = Column(Integer, primary_key=True)
    design_id     = Column(Integer, ForeignKey("designs.id"))
    niche_id      = Column(Integer, ForeignKey("niches.id"))
    title         = Column(String)
    description   = Column(Text)
    tags          = Column(JSON)       # list of 13 strings
    caption       = Column(Text)
    etsy_listing_id = Column(String)
    printify_product_id = Column(String)
    status        = Column(String, default="pending")
    # pending → copy_ready → uploaded → live → paused
    views         = Column(Integer, default=0)
    favorites     = Column(Integer, default=0)
    sales         = Column(Integer, default=0)
    revenue       = Column(Float, default=0.0)
    created_at    = Column(DateTime, default=func.now())
    uploaded_at   = Column(DateTime)

class TaskLog(Base):
    __tablename__ = "task_logs"
    id            = Column(Integer, primary_key=True)
    task_name     = Column(String, index=True)
    status        = Column(String)     # running/done/failed
    started_at    = Column(DateTime)
    finished_at   = Column(DateTime)
    error         = Column(Text)
    result_summary= Column(Text)
```

---

## Phase 0 — Project Bootstrap

> Complete this phase before writing any tool code. Every later phase depends on it.

- [x] **0.1 Repo init**
  - `git init pod && cd pod`
  - Create directory structure exactly as shown in Project Root Layout
  - Create `.env.example` with all keys listed above
  - Create `.gitignore`: `.env`, `data/`, `__pycache__/`, `*.pyc`, `node_modules/`

- [x] **0.2 Python environment**
  - Create `requirements.txt` with all packages in Tech Stack table
  - `python3.11 -m venv venv && source venv/bin/activate`
  - `pip install -r requirements.txt`
  - `playwright install chromium`

- [x] **0.3 Database setup**
  - Create `tools/shared/models.py` with all 5 models above
  - Create `tools/shared/db.py` — engine + `get_session()` helper
  - `alembic init alembic && alembic revision --autogenerate -m "init"`
  - `alembic upgrade head`
  - Test: `python -c "from tools.shared.db import get_session; print('DB OK')"`

- [x] **0.4 Shared utilities**
  - `tools/shared/config.py` — loads all env vars, raises clear error if missing
  - `tools/shared/logger.py` — structured logger, writes to `data/logs/<tool>.log`
  - `tools/shared/notify.py` — Apprise wrapper: `notify(title, body, level)`
  - `tools/shared/api_clients.py` — instantiate Anthropic, OpenAI clients once

- [x] **0.5 Docker Compose**
  - Write `docker-compose.yml` with 5 services: `dashboard`, `worker`, `beat`, `redis`, `flower`
  - All services mount `./data:/app/data` and read from `.env`
  - Redis: `redis:7-alpine`, no persistence needed
  - Flower: `mher/flower`, basic auth from env vars, port 5555
  - Test: `docker compose up redis flower -d && curl localhost:5555`

- [x] **0.6 Celery base**
  - Write `celery_app.py` — Celery instance, broker=REDIS_URL, result backend=REDIS_URL
  - Write `tasks.py` — empty file with `@app.task` stub for each tool (placeholders)
  - Write `schedule.py` — Celery Beat schedule matching the weekly timetable (see Phase 6)
  - Test: `celery -A celery_app worker --loglevel=info`

---

## Phase 1 — Trend Research Tools

> Depends on: Phase 0 complete

- [x] **1.1 `tools/trend/trend_scraper.py`**
  - Input: list of seed keywords from `config.py`
  - Use `pytrends.TrendReq` — pull `interest_over_time` for 90 days
  - Also pull `related_queries` for rising breakouts
  - Output: upsert rows into `niches` table with `trend_score` and `velocity`
  - Log: number of niches updated, top 5 by score
  - Error handling: retry 3× on `ResponseError`, sleep 60s between retries
  - Test: `pytest tests/test_trend_scraper.py` — mock pytrends, assert DB rows

- [x] **1.2 `tools/trend/reddit_scraper.py`**
  - Use `praw` — search `r/Etsy`, `r/printondemand`, `r/redbubble` for rising posts
  - Extract product/niche keywords from post titles using Claude API
  - Upsert into `niches` table — boost `velocity` for keywords found here
  - Rate limit: respect Reddit API 60 req/min
  - Test: mock PRAW, assert Claude prompt is called, assert DB upsert

- [x] **1.3 `tools/trend/etsy_scraper.py`**
  - Use Playwright (headless) to load Etsy bestseller pages for top niches
  - Extract: listing titles, number of sales, price range
  - Save to `competition` field in `niches` table (higher sales density = higher competition)
  - Respect: 2s delay between pages, rotate user agent
  - Test: mock Playwright page, assert competition score saved

- [x] **1.4 `tools/trend/niche_scorer.py`**
  - Read all niches from DB
  - Apply formula: `final_score = (trend_score × velocity) / max(competition, 0.1)`
  - Normalise scores 0–100
  - Update `final_score` on all niches, set `status=killed` if score < 10
  - Output: print top 20 niches ranked by `final_score`
  - Test: given known inputs, assert correct final scores

- [x] **1.5 Register Celery tasks**
  - Add `run_trend_scraper`, `run_reddit_scraper`, `run_etsy_scraper`, `run_niche_scorer` to `tasks.py`
  - Each task: log start/end to `TaskLog`, call `notify()` on failure
  - Add to `schedule.py`: Mon/Wed/Fri 00:00 UTC

---

## Phase 2 — AI Design Pipeline

> Depends on: Phase 1 complete, niches in DB

- [x] **2.1 `tools/design/prompt_generator.py`**
  - Read top 10 niches by `final_score` from DB
  - For each niche, call Claude API with system prompt:
    ```
    You are a POD design expert. Generate 50 distinct Midjourney/Stable Diffusion prompts
    for the niche: "{keyword}". Each prompt must be print-ready, vector-friendly,
    no text in image, transparent background suitable. Output JSON array of strings only.
    ```
  - Parse JSON response, insert into `prompts` table with `status=pending`
  - Test: mock Anthropic client, assert 50 prompts per niche inserted

- [x] **2.2 `tools/design/image_generator.py`**
  - Read prompts where `status=pending` (batch of 20 at a time)
  - Call Stability AI API (`stable-diffusion-xl-1024-v1-0`) or DALL-E 3
  - Save raw PNG to `data/designs/raw/<niche_id>/<prompt_id>.png`
  - Update `designs` table: `raw_path`, `status=generated`
  - Retry on API error, mark `status=failed` after 3 attempts
  - Throttle: max 5 concurrent requests
  - Test: mock API, assert file saved, assert DB updated

- [x] **2.3 `tools/design/image_processor.py`**
  - Read designs where `status=generated` and `raw_path` exists
  - Step 1: remove background with `rembg` → save to temp
  - Step 2: upscale to 4500×5400px with Pillow LANCZOS, save as PNG
  - Step 3: save to `data/designs/processed/<id>.png`
  - Update `designs.processed_path`, `status=processed`
  - Test: use a real 200×200 test image, assert output is 4500×5400

- [x] **2.4 `tools/design/clip_filter.py`**
  - Use `transformers` CLIP model (ViT-B/32) — runs locally, no API needed
  - For each processed design: encode image + niche keyword as text
  - Compute cosine similarity — save as `clip_score`
  - Auto-set `status=rejected` if `clip_score < 0.20`
  - Auto-set `status=approved` if `clip_score >= 0.20` (human still reviews)
  - Test: use two test images (relevant/irrelevant), assert correct auto-status

- [x] **2.5 `tools/design/mockup_generator.py`**
  - Read designs where `status=approved` and `mockup_path IS NULL`
  - Call Printify Mockup API: POST `/v1/catalog/<blueprint_id>/print_provider/<id>/variants.json`
  - Download mockup image, save to `data/designs/mockups/<id>.png`
  - Update `designs.mockup_path`, `status=mockup_ready`
  - Test: mock Printify API, assert mockup saved

- [x] **2.6 Register Celery tasks**
  - Tasks: `run_prompt_gen`, `run_image_gen`, `run_image_processor`, `run_clip_filter`, `run_mockup_gen`
  - Schedule in `schedule.py`: Mon/Wed/Fri 02:00, 05:00, 09:00 UTC chained
  - Chain: `run_prompt_gen | run_image_gen | run_image_processor | run_clip_filter`

---

## Phase 3 — AI Copywriting

> Depends on: Phase 2 complete, designs in DB with `status=mockup_ready`

- [x] **3.1 `tools/copy/copy_generator.py`**
  - Read listings where `title IS NULL` and design `status=mockup_ready`
  - For each: call Claude API with prompt:
    ```
    You are an Etsy SEO expert. For the niche "{keyword}" and product type "t-shirt",
    write a JSON object with:
    - "title": 140-char Etsy title, front-load keywords
    - "description": 800-char description, 5 bullet points, benefits-focused
    - "tags": array of exactly 13 strings, mix long-tail and short keywords
    Output only valid JSON, no markdown.
    ```
  - Parse and save to `listings` table: `title`, `description`, `tags`
  - Test: mock Claude, assert valid JSON parsed, all 3 fields saved

- [x] **3.2 `tools/copy/caption_generator.py`**
  - For each listing with `title` set but `caption IS NULL`
  - Call Claude: generate one engaging social media caption (max 200 chars) with 3–5 hashtags
  - Save to `listings.caption`
  - Test: mock Claude, assert caption length ≤ 200 chars

- [x] **3.3 Register Celery tasks**
  - Tasks: `run_copy_gen`, `run_caption_gen`
  - Schedule: Mon/Wed/Fri 10:00 UTC

---

## Phase 4 — Upload & Automation

> Depends on: Phase 3 complete, listings with copy ready

- [x] **4.1 `tools/upload/printify_publisher.py`**
  - Read listings where `printify_product_id IS NULL` and `status=copy_ready`
  - For each: POST to Printify `/v1/shops/<id>/products.json`
    - Blueprint: t-shirt (ID 5), print provider: Monster Digital (ID 29)
    - Upload processed design image as print file
    - Set title, description from DB
    - Publish: POST `/v1/shops/<id>/products/<id>/publish.json`
  - Save `printify_product_id` to listings table
  - Test: mock Printify API, assert product created and published

- [x] **4.2 `tools/upload/etsy_uploader.py`**
  - Read listings where `etsy_listing_id IS NULL` and `printify_product_id` set
  - POST to Etsy v3 API `/v3/application/listings`
    - Fields: title, description, tags, price, quantity, images (mockup)
    - State: `active`
  - Save `etsy_listing_id`, set `status=live`, set `uploaded_at`
  - Handle: 429 rate limit (back off 60s), retry up to 3×
  - Test: mock Etsy API, assert listing ID saved, status=live

- [x] **4.3 `tools/upload/order_router.py`**
  - FastAPI router: `POST /webhook/etsy-order`
  - Parse Etsy order webhook payload
  - For each line item: find `printify_product_id` from `listings` table
  - POST to Printify `/v1/shops/<id>/orders.json` to create fulfillment order
  - Log order ID and status
  - Register webhook URL in Etsy: `POST /v3/application/shops/<id>/receipts/open/webhooks`
  - Test: POST mock payload, assert Printify order created

- [x] **4.4 `tools/upload/price_adjuster.py`**
  - Use Playwright to scrape top 20 Etsy results for each active niche keyword
  - Extract prices, calculate median competitor price
  - If your listing price is >20% above median: log warning
  - If your listing price is <10% above median: log recommendation to raise
  - No automatic price changes — output recommendation report only
  - Test: mock Playwright, assert report generated

- [x] **4.5 `tools/upload/social_poster.py`**
  - Read listings where `status=live` and `social_posted IS NULL`
  - For each (up to 5 per run): post to Buffer API with mockup image + caption
  - Update `listings.social_posted = now()`
  - Test: mock Buffer API, assert post created

- [x] **4.6 Register Celery tasks**
  - Tasks: `run_printify_publish`, `run_etsy_upload`, `run_price_check`, `run_social_post`
  - Schedule in `schedule.py`: Mon–Sat 14:00 UTC (upload), 16:00 UTC (social)

---

## Phase 5 — Analytics

> Depends on: Phase 4 complete, live listings on Etsy

- [x] **5.1 `tools/analytics/analytics_puller.py`**
  - For each listing with `etsy_listing_id`:
    - GET Etsy `/v3/application/listings/<id>/stats`
    - Update `listings`: `views`, `favorites`, `sales`, `revenue`
  - Log: total daily revenue, total views, new sales count
  - Test: mock Etsy API, assert DB updated

- [x] **5.2 `tools/analytics/performance_flagger.py`**
  - Read listings where `uploaded_at < now() - 7 days`
  - Flag as `status=underperforming` if: views < 50 AND favorites < 3 in 7 days
  - Send notification: `notify("Low performers", "N listings flagged for review")`
  - Do NOT deactivate automatically — human decides
  - Test: insert test listing with old date + low stats, assert flagged

- [x] **5.3 `tools/analytics/weekly_report.py`**
  - Run every Friday 20:00 UTC
  - Collect from DB: top 5 niches by revenue, top 5 listings, total week revenue
  - Call Claude API: summarise data, recommend 3 niches to scale, 2 to kill
  - Save report as `data/logs/report_YYYY-MM-DD.md`
  - Send notification with summary
  - Test: mock DB data + Claude, assert report file created

- [x] **5.4 Register Celery tasks**
  - Tasks: `run_analytics_pull`, `run_performance_flag`, `run_weekly_report`
  - Schedule: daily 20:00 UTC (pull + flag), Friday 20:00 UTC (report)

---

## Phase 6 — Celery Beat Schedule

> Complete this after all tasks are registered. Mirrors the weekly timetable.

```python
# schedule.py — full Beat schedule

from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {

    # ── NIGHT: Mon/Wed/Fri ──────────────────────────────
    "trend-scrape":     {"task": "tasks.run_trend_scraper",    "schedule": crontab(hour=0,  minute=0,  day_of_week="1,3,5")},
    "reddit-scrape":    {"task": "tasks.run_reddit_scraper",   "schedule": crontab(hour=0,  minute=30, day_of_week="1,3,5")},
    "niche-score":      {"task": "tasks.run_niche_scorer",     "schedule": crontab(hour=1,  minute=0,  day_of_week="1,3,5")},
    "prompt-gen":       {"task": "tasks.run_prompt_gen",       "schedule": crontab(hour=2,  minute=0,  day_of_week="1,3,5")},
    "image-gen":        {"task": "tasks.run_image_gen",        "schedule": crontab(hour=3,  minute=0,  day_of_week="1,3,5")},
    "image-process":    {"task": "tasks.run_image_processor",  "schedule": crontab(hour=6,  minute=0,  day_of_week="1,3,5")},
    "clip-filter":      {"task": "tasks.run_clip_filter",      "schedule": crontab(hour=7,  minute=0,  day_of_week="1,3,5")},

    # ── MORNING: daily ──────────────────────────────────
    "etsy-scrape":      {"task": "tasks.run_etsy_scraper",     "schedule": crontab(hour=9,  minute=0,  day_of_week="1,2,3,4,5,6")},
    "mockup-gen":       {"task": "tasks.run_mockup_gen",       "schedule": crontab(hour=9,  minute=30, day_of_week="1,3,5,6")},

    # ── DAY: Mon/Wed/Fri/Sat ────────────────────────────
    "copy-gen":         {"task": "tasks.run_copy_gen",         "schedule": crontab(hour=10, minute=0,  day_of_week="1,3,5,6")},
    "caption-gen":      {"task": "tasks.run_caption_gen",      "schedule": crontab(hour=11, minute=0,  day_of_week="1,3,5,6")},

    # ── AFTERNOON: Mon–Sat ──────────────────────────────
    "printify-publish": {"task": "tasks.run_printify_publish", "schedule": crontab(hour=13, minute=0,  day_of_week="1,2,3,4,5,6")},
    "etsy-upload":      {"task": "tasks.run_etsy_upload",      "schedule": crontab(hour=14, minute=0,  day_of_week="1,2,3,4,5,6")},
    "social-post":      {"task": "tasks.run_social_post",      "schedule": crontab(hour=16, minute=0,  day_of_week="1,3,5,0")},

    # ── EVENING: daily ──────────────────────────────────
    "analytics-pull":   {"task": "tasks.run_analytics_pull",   "schedule": crontab(hour=20, minute=0)},
    "perf-flag":        {"task": "tasks.run_performance_flag", "schedule": crontab(hour=20, minute=30)},
    "weekly-report":    {"task": "tasks.run_weekly_report",    "schedule": crontab(hour=20, minute=0,  day_of_week="5")},

    # ── NIGHT: daily maintenance ────────────────────────
    "price-check":      {"task": "tasks.run_price_check",      "schedule": crontab(hour=22, minute=0,  day_of_week="1,3,5")},
    "full-backup":      {"task": "tasks.run_backup",           "schedule": crontab(hour=22, minute=30, day_of_week="0")},
}
```

- [x] **6.1** Paste schedule above into `schedule.py`, verify all task names match `tasks.py`
- [x] **6.2** Test Beat: verified all 19 beat entries import without errors
- [x] **6.3** All task functions verified callable via import check

---

## Phase 7 — FastAPI Dashboard

> Depends on: Phase 0 DB + shared utilities

- [x] **7.1 `app/main.py` — app setup**
  - FastAPI app with Jinja2 templates, StaticFiles
  - HTTP Basic Auth middleware using `DASHBOARD_USER` / `DASHBOARD_PASS` from env
  - Mount all routers below
  - Include lifespan: connect DB on startup

- [x] **7.2 `/` — Overview page**
  - Show: tasks run today (count), errors today, designs pending review, listings uploaded today
  - Pull from `TaskLog` table (last 24h) and `listings` table
  - Auto-refresh every 60s via `<meta http-equiv="refresh" content="60">`

- [x] **7.3 `/tasks` — Task control panel**
  - Table: task name, last run, status, duration, result summary
  - "Run now" button per task — calls `celery_app.send_task(name)` via POST
  - Pull from `TaskLog` table, latest entry per task name

- [x] **7.4 `/designs` — Human review queue**
  - Grid of designs where `status=approved` (CLIP passed, human not yet reviewed)
  - Show: niche keyword, CLIP score, raw and processed image side by side
  - Buttons: "Approve → Mockup" (set `status=approved`), "Reject" (set `status=rejected`)
  - POST `/designs/<id>/approve` and `/designs/<id>/reject` endpoints
  - Batch select + bulk approve/reject

- [x] **7.5 `/listings` — Listings table**
  - Paginated table: title, niche, status, Etsy link, views, favorites, revenue
  - Filter by status (pending / live / underperforming)
  - Click row to expand: show full description, tags, mockup image

- [x] **7.6 `/niches` — Niche rankings**
  - Table: keyword, final_score, trend_score, velocity, competition, designs count, listings count, status
  - Sort by final_score descending
  - Buttons: "Kill niche" (set `status=killed`), "Pause" (set `status=paused`)

- [x] **7.7 `/logs` — Log viewer**
  - Dropdown: select tool log file from `data/logs/`
  - Show last 200 lines, newest first
  - Auto-refresh every 30s

- [x] **7.8 `/report` — Weekly report**
  - List all `data/logs/report_*.md` files as links
  - Render selected report as HTML (parse markdown)

---

## Phase 8 — VPS Deployment

> Do this last, after all tools tested locally.

- [ ] **8.1 Provision VPS**
  - Hetzner CX21 (2 vCPU, 4GB RAM, Ubuntu 22.04) — €4.51/mo
  - SSH key auth only, disable password login
  - Open ports: 22 (SSH), 80, 443, 5555 (Flower — restrict to your IP)

- [ ] **8.2 Server setup**
  ```bash
  apt update && apt upgrade -y
  apt install -y docker.io docker-compose-plugin nginx certbot python3-certbot-nginx git
  usermod -aG docker $USER
  ```

- [ ] **8.3 Clone and configure**
  ```bash
  git clone <repo> /home/pod
  cd /home/pod
  cp .env.example .env   # fill in all keys
  mkdir -p data/designs/{raw,processed,mockups} data/logs
  ```

- [ ] **8.4 Nginx config**
  ```nginx
  # /etc/nginx/sites-available/pod
  server {
      listen 80;
      server_name <your-domain>;

      location / {
          proxy_pass http://127.0.0.1:8000;
          auth_basic "POD Dashboard";
          auth_basic_user_file /etc/nginx/.htpasswd;
      }

      location /flower {
          proxy_pass http://127.0.0.1:5555;
          auth_basic "Flower";
          auth_basic_user_file /etc/nginx/.htpasswd;
      }
  }
  ```
  - `htpasswd -c /etc/nginx/.htpasswd admin`
  - `certbot --nginx -d <your-domain>`

- [ ] **8.5 Start all containers**
  ```bash
  docker compose up -d
  docker compose ps   # all 5 containers: Up
  ```

- [ ] **8.6 `backup.sh`**
  ```bash
  #!/bin/bash
  DATE=$(date +%Y-%m-%d)
  sqlite3 data/pod.db ".backup data/backup_${DATE}.db"
  tar -czf /tmp/designs_${DATE}.tar.gz data/designs/
  # upload to S3/Backblaze
  aws s3 cp data/backup_${DATE}.db s3://$S3_BUCKET/backups/
  aws s3 cp /tmp/designs_${DATE}.tar.gz s3://$S3_BUCKET/backups/
  ```
  - `chmod +x backup.sh`
  - Add to cron: `0 22 * * 0 /home/pod/backup.sh >> data/logs/backup.log 2>&1`

- [ ] **8.7 Smoke test**
  - Visit dashboard URL — login works
  - Visit `/flower` — Celery workers visible
  - Manually trigger `run_trend_scraper` from `/tasks` page
  - Confirm `TaskLog` entry created with `status=done`
  - Confirm niches appear in `/niches` page

---

## Phase 9 — Testing Checklist

Run before marking any phase complete.

```bash
# run all tests
pytest tests/ -v --tb=short

# individual
pytest tests/test_trend_scraper.py
pytest tests/test_image_generator.py
pytest tests/test_copy_generator.py
pytest tests/test_etsy_uploader.py
pytest tests/test_analytics_puller.py
pytest tests/test_dashboard.py
```

- [x] **9.1** All unit tests pass (mocked APIs) — 66/66 passing
- [ ] **9.2** Integration test: run full chain end-to-end with 1 niche, 1 design, 1 listing (use Etsy sandbox)
- [ ] **9.3** Load test: trigger 20 concurrent image gen tasks — confirm no DB race conditions
- [ ] **9.4** Failure test: kill Redis mid-run — confirm tasks retry and recover
- [ ] **9.5** Backup test: run `backup.sh`, confirm files appear in S3

---

## Implementation Rules for Claude

1. **One step at a time.** Never implement two unchecked steps in the same response.
2. **No orphan code.** Every function must be imported and called somewhere.
3. **Always handle errors.** Every API call needs try/except. Every file operation needs existence check.
4. **Always log.** Every tool must log to `data/logs/<toolname>.log` and write a `TaskLog` row.
5. **Never hardcode secrets.** All API keys come from `config.py` which reads `.env`.
6. **Test before mark.** Do not mark a step `[x]` unless a test (even manual) confirms it works.
7. **Notify on failure.** Every Celery task wraps its body in try/except and calls `notify()` on exception.
8. **Keep functions small.** Each function does one thing. Max ~40 lines per function.
9. **Database writes are atomic.** Use `session.begin()` context manager — rollback on error.
10. **Ask before guessing.** If a step is ambiguous (e.g. which Printify blueprint ID to use), ask the human before implementing.

---

## Current Status

| Phase | Name | Status |
|-------|------|--------|
| 0 | Bootstrap | `[x] complete` |
| 1 | Trend Research | `[x] complete` |
| 2 | AI Design Pipeline | `[x] complete` |
| 3 | AI Copywriting | `[x] complete` |
| 4 | Upload & Automation | `[x] complete` |
| 5 | Analytics | `[x] complete` |
| 6 | Celery Beat Schedule | `[x] complete` |
| 7 | FastAPI Dashboard | `[x] complete` |
| 8 | VPS Deployment | `[ ] ready to deploy` |
| 9 | Testing | `[~] unit tests pass, integration pending` |

---

*Start with Phase 0, Step 0.1. Work top to bottom. Update this table as phases complete.*
