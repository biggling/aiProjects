# TikTok Affiliate & Shop Automation — Implementation Plan

> This document is the authoritative build guide for Claude.
> Work through each phase sequentially. Complete all tasks in a phase before moving to the next.
> Mark each task `[x]` when done.

---

## Phase -1: Deep Market Research & Target Customer (DO BEFORE RESUMING BUILD)

**Goal:** Validate TikTok Shop affiliate model with real data and identify exact audience/product sweet spot.

### Market Sizing & Validation
- [ ] Research TikTok Shop affiliate program in Thailand:
  - Total affiliate creators in Thailand (TikTok Shop Creator Hub data)
  - Average commission rates by category (beauty, gadgets, fashion)
  - Top 10 TikTok Shop affiliate creators in Thailand — avg monthly earnings
- [ ] Analyze actual TikTok Shop bestsellers in Thailand:
  - Top 50 products by affiliate sales volume — note category, price, commission
  - Which products have >10% commission AND >1000 daily sales?
- [ ] Research AI-generated TikTok content performance:
  - Do AI voiceover videos perform as well as human-voice videos?
  - What's the avg view count for AI-generated product review content?
  - Has TikTok cracked down on AI-generated content in 2026?
- [ ] Calculate unit economics per video:
  - Cost: AI video gen API ($X) + voiceover ($X) + compute ($X) per video
  - Revenue: avg views × CTR × conversion rate × avg commission
  - At what volume does this become profitable?
- [ ] Research TikTok algorithm changes in 2026: any penalties for automated posting?

### Laser-Targeted Audience Persona
- [ ] **Primary audience: "Shopaholic Siri"** — Thai female, 18-30:
  - Shopping behavior: daily TikTok scroller, impulse buyer
  - Categories she buys: beauty/skincare, fashion accessories, home gadgets
  - Price range: ฿100-฿1,000 ($3-$30) per impulse purchase
  - Content that makes her buy: demo videos, before/after, "TikTok made me buy it"
  - Language: Thai only — content MUST be in Thai
  - Peak active hours: 12:00-14:00 (lunch) and 19:00-23:00 (evening)
- [ ] **Secondary audience: "Gadget Guy Gorn"** — Thai male, 20-35:
  - Buys: tech gadgets, gaming accessories, fitness gear
  - Higher price tolerance: ฿500-฿3,000
  - Content that works: unboxing, comparison, "ของเจ๋งจาก TikTok Shop"
- [ ] Research which content angles get highest conversion (not just views):
  - Demo/review vs lifestyle vs problem-solution vs humor
  - Does "honest review" outperform "hype" in conversion?
- [ ] Study top 5 TikTok Shop affiliate creators in Thailand — note their exact formula

### Competitor Deep-Dive
- [ ] Identify automated/AI TikTok Shop affiliate accounts — are they working?
- [ ] Analyze top manual affiliate creators: posting frequency, avg views, engagement rate
- [ ] Research what tools Thai affiliate creators use (CapCut templates, editing styles)
- [ ] Check TikTok Creator Marketplace for commission benchmarks in Thailand

### Research Deliverables
- [ ] Unit economics model: cost per video vs expected revenue per video
- [ ] Audience persona cards with buying triggers and content preferences
- [ ] Top 20 product × category opportunities ranked by commission × volume × content ease
- [ ] Go/no-go: is automated TikTok affiliate viable at current API costs?

---

## Project overview

Build a fully automated Python-based system that:
1. Researches trending products and content angles daily
2. Generates scripts, voiceovers, and AI video clips automatically
3. Edits, captions, and publishes 2 TikTok videos per day
4. Cross-posts to Instagram Reels and YouTube Shorts
5. Tracks performance and surfaces winners for human review

**Target output:** 10 published videos/week with ~90 min of human input total.

---

## Tech stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Task queue | Celery + Redis |
| API framework | FastAPI |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Video editing | FFmpeg |
| Speech-to-text | OpenAI Whisper |
| LLM | OpenAI GPT-4o or Claude claude-sonnet-4-6 |
| Voiceover | ElevenLabs API |
| Video generation | Kling AI API or Runway Gen-4 API |
| Scheduling | APScheduler |
| Config | python-dotenv + YAML |
| **Dashboard frontend** | **React 18 + Vite** |
| **Dashboard UI kit** | **shadcn/ui + Tailwind CSS** |
| **Dashboard charts** | **Recharts** |
| **Dashboard state** | **TanStack Query (React Query)** |
| **Dashboard routing** | **React Router v6** |
| **Dashboard realtime** | **WebSocket (FastAPI native)** |

---

## Repository structure

```
tiktok-automation/
├── plan.md                   ← this file
├── README.md
├── .env.example
├── config/
│   ├── settings.yaml         ← global config (slots, limits, paths)
│   └── products.yaml         ← human-managed product list
├── data/
│   ├── db/                   ← SQLite files (dev)
│   ├── assets/               ← raw AI-generated video + audio
│   ├── output/               ← final edited videos ready to publish
│   └── analytics/            ← pulled metrics JSONs
├── modules/
│   ├── 01_research/
│   ├── 02_scriptgen/
│   ├── 03_voiceover/
│   ├── 04_videogen/
│   ├── 05_editor/
│   ├── 06_publisher/
│   └── 07_analytics/
├── scheduler/
│   └── jobs.py               ← APScheduler job definitions
├── api/
│   ├── main.py               ← FastAPI backend + WebSocket server
│   ├── routers/              ← route modules per domain
│   │   ├── videos.py
│   │   ├── brief.py
│   │   ├── analytics.py
│   │   ├── products.py
│   │   └── schedule.py
│   └── ws.py                 ← WebSocket connection manager
├── dashboard/                ← React frontend (Vite)
│   ├── index.html
│   ├── vite.config.ts
│   ├── tailwind.config.ts
│   ├── package.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/              ← typed API client (axios + React Query)
│       ├── components/       ← shared UI components
│       │   ├── VideoPlayer.tsx
│       │   ├── StatusBadge.tsx
│       │   ├── JobTimeline.tsx
│       │   └── MetricCard.tsx
│       ├── pages/
│       │   ├── Dashboard.tsx       ← home: today's status overview
│       │   ├── QueueReview.tsx     ← video QC approval page
│       │   ├── ContentBrief.tsx    ← monday brief review + product approval
│       │   ├── Analytics.tsx       ← weekly performance charts
│       │   ├── Products.tsx        ← product config management
│       │   └── Schedule.tsx        ← automation job log + status
│       └── hooks/            ← custom React hooks
├── tests/
└── requirements.txt
```

---

## Phase 0 — Project bootstrap

**Goal:** Repo, env, and dependencies ready. All API keys confirmed working.

### Tasks

- [x] Create the repository structure above using `mkdir -p` and placeholder `__init__.py` files
- [x] Create `requirements.txt` with all dependencies listed in the tech stack
- [x] Create `.env.example` with all required env var keys (no values):
  ```
  OPENAI_API_KEY=
  ELEVENLABS_API_KEY=
  ELEVENLABS_VOICE_ID=
  KLING_API_KEY=
  RUNWAY_API_KEY=
  TIKTOK_ACCESS_TOKEN=
  TIKTOK_OPEN_ID=
  INSTAGRAM_ACCESS_TOKEN=
  YOUTUBE_CLIENT_SECRET=
  REDIS_URL=redis://localhost:6379/0
  DATABASE_URL=sqlite:///data/db/app.db
  API_KEY=
  DASHBOARD_PORT=5173
  VITE_API_BASE_URL=http://localhost:8000
  VITE_WS_URL=ws://localhost:8000/ws
  ```
- [x] Create `config/settings.yaml` with:
  - publish slots: `["12:00", "18:00"]` (Asia/Bangkok timezone)
  - max videos per day: 2
  - video duration target: 30–45 seconds
  - output resolution: 1080x1920
  - language: Thai (primary), English (captions)
- [x] Create `config/products.yaml` schema:
  ```yaml
  products:
    - id: prod_001
      name: ""
      tiktok_shop_url: ""
      commission_rate: 0.0
      affiliate_link: ""
      utm_source: tiktok
      utm_campaign: ""
      approved: false
  ```
- [x] Write a `scripts/verify_env.py` that imports each API client and confirms authentication for every key
- [ ] Run `verify_env.py` and confirm all APIs respond — fix any auth errors before proceeding

### Deliverable
`python scripts/verify_env.py` exits with `All APIs OK`.

---

## Phase 1 — Research module (`modules/01_research/`)

**Goal:** Automated daily trend + product data collection stored to DB.

### Files to create
- `scraper.py` — main entry point
- `tiktok_trends.py` — TikTok trending sounds and hashtags
- `shop_products.py` — TikTok Shop bestseller rankings
- `competitor.py` — video hook extraction from top performers
- `models.py` — SQLAlchemy models: `Trend`, `Product`, `CompetitorHook`
- `db.py` — database session and migration helpers

### Tasks

- [x] Create SQLAlchemy models:
  - `Trend(id, date, sound_name, hashtag, use_count, scraped_at)`
  - `Product(id, name, category, price, commission_rate, rank, scraped_at)`
  - `CompetitorHook(id, video_id, hook_text, view_count, scraped_at)`
- [x] Implement `tiktok_trends.py`:
  - Use TikTok Research API (or unofficial scraper fallback) to fetch top 20 trending sounds and hashtags
  - Store results to `Trend` table
  - Log count of new records found
- [x] Implement `shop_products.py`:
  - Fetch TikTok Shop affiliate bestsellers via the affiliate open platform API
  - Filter by commission rate >= 10%
  - Store to `Product` table
- [x] Implement `competitor.py`:
  - Accept a list of hashtags, fetch top 10 videos per hashtag
  - Use GPT-4o to extract the hook (first 3 seconds of caption/title)
  - Store to `CompetitorHook` table
- [x] Implement `scraper.py` as the orchestrator:
  - Calls all three scrapers in sequence
  - Handles errors gracefully (log and continue, do not crash)
  - Returns a summary dict: `{trends: N, products: N, hooks: N}`
- [x] Write `tests/test_research.py` with at least one test per scraper using mocked API responses

### Deliverable
`python -m modules.01_research.scraper` runs without error and inserts rows into the DB.

---

## Phase 2 — Content strategy engine (`modules/01_research/strategy.py`)

**Goal:** AI scoring model that produces a ranked daily content brief from DB data.

### Tasks

- [x] Create `strategy.py` with a `generate_brief()` function that:
  1. Loads today's trends, top-ranked products, and top competitor hooks from DB
  2. Builds a structured prompt for GPT-4o containing all three data sources
  3. Asks the model to output a JSON array of 5 content ideas, each with:
     ```json
     {
       "rank": 1,
       "product_id": "prod_001",
       "product_name": "",
       "angle": "",
       "hook_idea": "",
       "trending_sound": "",
       "hashtags": [],
       "estimated_difficulty": "low|medium|high"
     }
     ```
  4. Validates and parses the JSON response
  5. Saves the brief to `data/analytics/brief_YYYY-MM-DD.json`
- [x] Create `models.py` entry: `ContentBrief(id, date, ideas_json, human_approved, approved_at)`
- [x] Add a CLI flag `--print` to output the brief to terminal for human review
- [ ] Write a unit test with a mocked GPT response

### Human checkpoint
After this phase, the Monday 07:00 review slot works:
```bash
python -m modules.01_research.strategy --print
```
Human reads brief, edits `config/products.yaml` to set `approved: true` on confirmed products.

### Deliverable
`brief_YYYY-MM-DD.json` file generated with 5 ranked ideas.

---

## Phase 3 — Script generator (`modules/02_scriptgen/`)

**Goal:** Produce a full video script for each approved content idea.

### Files to create
- `generator.py`
- `prompts.py` — all system and user prompt templates
- `models.py` — `Script(id, brief_id, product_id, hook, body, cta, caption, hashtags, created_at)`

### Tasks

- [x] Create prompt templates in `prompts.py`:
  - System prompt: sets tone (energetic, authentic, TikTok-native Thai creator)
  - User prompt: injects product name, angle, hook idea, trending sound, target duration
  - Output format: structured JSON with `hook`, `body`, `cta`, `caption`, `hashtags`
- [x] Implement `generator.py`:
  - Reads approved ideas from the latest brief
  - Calls GPT-4o once per idea with the prompt template
  - Parses and validates JSON output
  - Saves each script to DB and to `data/assets/scripts/script_{id}.json`
- [x] Add word count and estimated duration check (target: 80–120 words for 30–45 sec)
  - If too long: ask GPT to trim
  - If too short: ask GPT to expand
- [ ] Write tests with mocked GPT responses

### Deliverable
5 `script_{id}.json` files in `data/assets/scripts/` ready for voiceover.

---

## Phase 4 — Voiceover pipeline (`modules/03_voiceover/`)

**Goal:** Batch-render MP3 voiceovers from scripts using ElevenLabs.

### Files to create
- `renderer.py`
- `models.py` — `Voiceover(id, script_id, file_path, duration_sec, created_at)`

### Tasks

- [x] Implement `renderer.py`:
  - Loads all scripts that have no matching `Voiceover` record
  - For each script, concatenates `hook + " " + body + " " + cta` into one string
  - Calls ElevenLabs `text_to_speech` endpoint with configured `ELEVENLABS_VOICE_ID`
  - Settings: `stability=0.4`, `similarity_boost=0.8`, `style=0.3` (energetic tone)
  - Saves MP3 to `data/assets/audio/voice_{script_id}.mp3`
  - Records duration using `mutagen` or `librosa`
  - Saves `Voiceover` record to DB
- [x] Add retry logic: 3 attempts with 5-second backoff on API failure
- [ ] Write test with mocked ElevenLabs response

### Deliverable
5 `voice_{id}.mp3` files in `data/assets/audio/`.

---

## Phase 5 — Video generation orchestrator (`modules/04_videogen/`)

**Goal:** Generate AI B-roll footage for each script using Kling or Runway.

### Files to create
- `orchestrator.py`
- `kling.py` — Kling AI API client
- `runway.py` — Runway Gen-4 API client (fallback)
- `prompt_builder.py` — converts script body into video generation prompts
- `models.py` — `VideoClip(id, script_id, provider, file_path, duration_sec, status, created_at)`

### Tasks

- [x] Implement `prompt_builder.py`:
  - Takes script body text
  - Uses GPT-4o to produce a short (15-word max) visual scene description suitable for video gen
  - Outputs: `{"scene": "...", "style": "realistic product demo", "aspect_ratio": "9:16"}`
- [x] Implement `kling.py`:
  - `generate(prompt, duration=5)` → submits job, polls until complete, returns file URL
  - Download MP4 to `data/assets/clips/`
- [x] Implement `runway.py` as fallback with same interface
- [x] Implement `orchestrator.py`:
  - For each script with no `VideoClip` record
  - Build visual prompt
  - Try Kling first, fall back to Runway on failure
  - May need multiple clips per video (one per script section)
  - Save all clips and DB records
- [ ] Use Celery tasks for async generation — video gen can take 5–60 min
- [ ] Write tests with mocked API clients

### Deliverable
Raw MP4 clips in `data/assets/clips/` for each script.

---

## Phase 6 — Auto-editor (`modules/05_editor/`)

**Goal:** Assemble final 9:16 TikTok-ready MP4 from clips + voice + captions.

### Files to create
- `editor.py`
- `caption_generator.py` — Whisper transcription → styled subtitle file
- `thumbnail.py` — auto cover frame extractor
- `models.py` — `EditedVideo(id, script_id, file_path, thumbnail_path, duration_sec, created_at)`

### Tasks

- [x] Implement `caption_generator.py`:
  - Runs `openai.Audio.transcribe()` (Whisper) on the voiceover MP3
  - Produces an SRT file with word-level timestamps
  - Converts SRT to ASS format with styled fonts (large, bold, center, white with black outline)
  - Saves to `data/assets/captions/captions_{script_id}.ass`
- [x] Implement `editor.py` using FFmpeg subprocess calls:
  1. Resize/pad all video clips to 1080x1920
  2. Concatenate clips to match voiceover duration (loop or trim as needed)
  3. Mix voiceover audio over video (background music optional at -20dB)
  4. Burn captions using `subtitles` filter
  5. Add a 0.3-second fade-in at the start
  6. Output: `data/output/video_{script_id}.mp4` (H.264, AAC, max 50MB)
- [x] Implement `thumbnail.py`:
  - Extract frame at 1.5 seconds (past the hook)
  - Use Pillow to overlay product name text (white bold, bottom third)
  - Save as `data/output/thumb_{script_id}.jpg`
- [x] Validate output file: must be under 60 seconds and under 100MB
- [ ] Write integration test using a short sample clip and audio file

### Human checkpoint
After editing, the QC review slot (11:00 daily) uses:
```bash
python -m api.main  # launches dashboard at localhost:8000
```
Human watches videos in the dashboard, clicks Approve or Reject with optional note.

### Deliverable
Final `video_{id}.mp4` and `thumb_{id}.jpg` in `data/output/`.

---

## Phase 7 — Publisher (`modules/06_publisher/`)

**Goal:** Publish approved videos to TikTok at scheduled times with affiliate links attached.

### Files to create
- `tiktok.py` — TikTok Content Posting API client
- `instagram.py` — Instagram Graph API client
- `youtube.py` — YouTube Data API v3 client
- `link_tagger.py` — UTM and affiliate link formatter
- `scheduler_jobs.py` — APScheduler publish jobs
- `models.py` — `PublishedVideo(id, edited_video_id, platform, post_id, published_at, status)`

### Tasks

- [x] Implement `link_tagger.py`:
  - Takes base affiliate URL from `config/products.yaml`
  - Appends UTM params: `utm_source`, `utm_medium=video`, `utm_campaign`, `utm_content=video_{id}`
  - Returns formatted link string for caption insertion
- [x] Implement `tiktok.py`:
  - `upload_video(file_path, caption, cover_path)` using TikTok Content Posting API v2
  - Caption includes: script caption + hashtags + affiliate link (if allowed in caption) or bio link CTA
  - Handles chunked upload for files > 10MB
  - Returns `post_id`
- [x] Implement `instagram.py`:
  - Reformat video to 1080x1920 if not already (should already be correct)
  - Post as Instagram Reel via Graph API
  - Caption adapted from TikTok caption (remove TikTok-specific hashtags)
- [x] Implement `youtube.py`:
  - Upload as YouTube Short (≤60 sec, vertical)
  - Title = hook text, description = full caption + affiliate link
  - Set category, tags from hashtags
- [x] Implement `scheduler_jobs.py`:
  - Register two daily APScheduler jobs: `publish_slot_1` at 12:00 and `publish_slot_2` at 18:00 (Asia/Bangkok)
  - Each job: finds next approved, unpublished video → publishes to TikTok → queues cross-post
  - Cross-post to Instagram and YouTube fires 30 minutes after TikTok publish
- [ ] Write tests with mocked API clients and a fake video file

### Deliverable
Video published to TikTok with correct caption and affiliate link. `PublishedVideo` record created.

---

## Phase 8 — Analytics (`modules/07_analytics/`)

**Goal:** Pull per-video performance metrics daily and surface winners.

### Files to create
- `puller.py` — nightly metrics collection
- `scorer.py` — ranks videos and flags winners
- `report.py` — generates weekly summary for human review
- `models.py` — `VideoMetric(id, published_video_id, pulled_at, views, watch_time_avg, likes, shares, comments, ctr, gmv)`

### Tasks

- [x] Implement `puller.py`:
  - Runs nightly at 21:00
  - For each `PublishedVideo` published in the last 14 days
  - Calls TikTok Analytics API for: `video_views`, `average_watch_time`, `likes`, `shares`, `profile_visits`
  - Calls TikTok Shop affiliate API for GMV and order count attributed to the video
  - Saves to `VideoMetric` table
- [x] Implement `scorer.py`:
  - Composite score = `(views × 0.3) + (watch_time_pct × 0.3) + (ctr × 0.2) + (gmv × 0.2)`
  - Flags videos in top 20% as `winner=True`
  - For winners: generates a remix brief (extracts hook style, product, and angle for reuse)
- [x] Implement `report.py`:
  - Produces `data/analytics/weekly_report_YYYY-WW.json` and prints a human-readable summary
  - Contents: top 3 videos, total GMV, total views, avg CTR, best-performing product, worst hook
- [ ] Wire winners into content strategy: `scorer.py` writes remix ideas back into `ContentBrief` for next Monday

### Human checkpoint
Friday 15:00 review:
```bash
python -m modules.07_analytics.report --week current
```
Friday 21:00 winner approval:
```bash
python -m modules.07_analytics.scorer --approve-interactive
```
Human sees top 3, types `y/n` per winner to approve remix for next week.

### Deliverable
Weekly report JSON + terminal summary. Remix ideas queued for Monday brief.

---

## Phase 9 — Scheduler wiring (`scheduler/`)

**Goal:** All modules run automatically on schedule via APScheduler backed by Redis.

### Tasks

- [x] Create `scheduler/jobs.py` registering all cron jobs:

  | Time (BKK) | Job | Module |
  |---|---|---|
  | 06:00 daily | `run_research` | `01_research.scraper` |
  | 07:00 daily | `run_strategy` | `01_research.strategy` |
  | 07:30 daily | `run_scriptgen` | `02_scriptgen.generator` |
  | 08:00 daily | `run_voiceover` | `03_voiceover.renderer` |
  | 09:00 daily | `run_videogen` | `04_videogen.orchestrator` |
  | 10:30 daily | `run_editor` | `05_editor.editor` |
  | 12:00 daily | `publish_slot_1` | `06_publisher.tiktok` |
  | 15:30 daily | `run_crosspost` | `06_publisher.instagram + youtube` |
  | 18:00 daily | `publish_slot_2` | `06_publisher.tiktok` |
  | 21:00 daily | `run_analytics` | `07_analytics.puller` |
  | Friday 21:00 | `run_weekly_score` | `07_analytics.scorer` |

- [x] Each job: logs start/end time, catches all exceptions (log + alert, never crash scheduler)
- [x] Add a `--dry-run` flag to all jobs that executes all logic except actual API publish calls
- [x] Create `scheduler/main.py` as the entrypoint: `python -m scheduler.main`

### Deliverable
`python -m scheduler.main` runs without error. All jobs fire at correct times in dry-run mode.

---

## Phase 10 — Backend API (`api/`)

**Goal:** Clean FastAPI backend with typed routes, WebSocket support, and static file serving for the React dashboard.

### Files to create
- `api/main.py` — app factory, mounts routers, serves built dashboard static files
- `api/ws.py` — WebSocket connection manager for real-time job progress
- `api/routers/videos.py` — video queue and approval endpoints
- `api/routers/brief.py` — content brief read + product approval endpoints
- `api/routers/analytics.py` — metrics and weekly report endpoints
- `api/routers/products.py` — product CRUD (reads/writes `config/products.yaml`)
- `api/routers/schedule.py` — job status and manual trigger endpoints
- `api/deps.py` — shared dependencies (DB session, auth guard)

### API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/videos/pending` | List videos awaiting QC |
| GET | `/api/videos/{id}/stream` | Stream MP4 for in-browser playback |
| GET | `/api/videos/{id}/thumbnail` | Serve thumbnail JPEG |
| POST | `/api/videos/{id}/approve` | Approve video, queue for publish |
| POST | `/api/videos/{id}/reject` | Reject with `{ reason: string }` |
| GET | `/api/brief/today` | Today's content brief JSON |
| POST | `/api/brief/approve` | Approve selected ideas `{ idea_ids: [] }` |
| GET | `/api/analytics/weekly` | Weekly summary + top videos |
| GET | `/api/analytics/video/{id}` | Per-video metrics history |
| GET | `/api/products` | List all products |
| POST | `/api/products` | Add new product |
| PUT | `/api/products/{id}` | Update product (link, commission, approved) |
| DELETE | `/api/products/{id}` | Remove product |
| GET | `/api/schedule/today` | Today's job statuses |
| POST | `/api/schedule/run/{job_name}` | Manually trigger a job |
| WS | `/ws` | Real-time push: job progress, new videos ready |

### Tasks

- [x] Create `api/deps.py`:
  - `get_db()` — yields SQLAlchemy session
  - `verify_api_key()` — reads `Authorization: Bearer` header, compares to `API_KEY` env var
- [x] Create `api/ws.py` WebSocket manager:
  - `ConnectionManager` class with `connect()`, `disconnect()`, `broadcast(message)`
  - Broadcast events: `job_started`, `job_done`, `job_failed`, `video_ready`, `published`
  - Each event payload: `{ event: string, data: object, timestamp: string }`
- [x] Create all five routers with full request/response Pydantic models
- [x] In `api/main.py`:
  - Mount all routers under `/api` prefix
  - Serve built React dashboard from `dashboard/dist/` at `/`
  - Add CORS middleware allowing `localhost:5173` in development
  - Add WebSocket endpoint at `/ws`
- [ ] Write tests for each router using FastAPI `TestClient` and mocked DB

### Deliverable
`uvicorn api.main:app --reload` starts. All `/api/*` routes return correct responses. WebSocket connects and receives a test broadcast.

---

## Phase 10b — Web dashboard (`dashboard/`)

**Goal:** React SPA with 5 pages covering every human touchpoint. Connects to the FastAPI backend. Runs at `localhost:5173` in dev, served from `dashboard/dist/` in production.

### Setup tasks

- [x] Scaffold with `npm create vite@latest dashboard -- --template react-ts`
- [ ] Install dependencies:
  ```bash
  npm install @tanstack/react-query axios react-router-dom recharts
  npx shadcn-ui@latest init
  npx shadcn-ui@latest add card badge button dialog table tabs toast
  ```
- [x] Configure `vite.config.ts` proxy: `/api` → `http://localhost:8000` and `/ws` → `ws://localhost:8000`
- [x] Create `src/api/client.ts`: axios instance with `Authorization: Bearer {API_KEY}` header from env
- [x] Create `src/api/hooks.ts`: React Query hooks for every endpoint (`useVideoPending`, `useTodayBrief`, `useWeeklyAnalytics`, etc.)
- [x] Create `src/hooks/useWebSocket.ts`: connects to `/ws`, parses events, updates React Query cache on `video_ready` and `published` events

### Page: Dashboard (`src/pages/Dashboard.tsx`)

The home page — shows a live snapshot of today's pipeline.

- [x] Top row — 4 metric cards:
  - Videos in queue (pending QC)
  - Videos approved today
  - Videos published today
  - Today's estimated GMV (from last analytics pull)
- [x] Pipeline status timeline — vertical list of today's automation jobs:
  - Each job: name, scheduled time, status badge (`pending` / `running` / `done` / `failed`), duration
  - Status updates live via WebSocket
  - Failed jobs show error message inline with a "retry" button that calls `POST /api/schedule/run/{job}`
- [x] "Next action required" card — prominent, always visible:
  - Shows the next human checkpoint (e.g. "QC review ready — 5 videos waiting")
  - Button navigates to the relevant page
- [ ] Recent publishes list (partial — needs dedicated endpoint) — last 5 published videos with platform badges and view counts

### Page: QC review (`src/pages/QueueReview.tsx`)

The daily 11:00 human slot — approve or reject assembled videos.

- [x] Video list on the left (scrollable):
  - Thumbnail, product name, script hook preview, status badge
  - Click to load into the player
- [x] Video player panel on the right:
  - Native HTML5 `<video>` element, autoplay on select, 9:16 aspect ratio
  - Script details below: hook, body, CTA, caption, hashtags
  - Two action buttons: green "Approve" and red "Reject"
  - Reject opens a small dialog with a text field for rejection reason
- [x] Keyboard shortcuts: `a` = approve, `r` = reject, `→` = next video
- [x] Progress indicator: "3 / 5 reviewed" at the top
- [x] After all reviewed: confirmation banner "All done — next publish at 12:00"

### Page: Content brief (`src/pages/ContentBrief.tsx`)

The Monday 07:00 human slot — review and approve this week's content plan.

- [ ] Date selector at top (defaults to today's brief)
- [x] 5 idea cards in a ranked list, each showing:
  - Rank badge, product name, angle, hook idea, trending sound, hashtags
  - Difficulty badge (`low` / `medium` / `high`)
  - Toggle switch: "Include this idea"
- [x] Product approval panel below the ideas:
  - Table of products from `config/products.yaml`
  - Columns: name, category, commission rate, affiliate link, approved toggle
  - Inline edit for affiliate link field
  - "Save products" button calls `PUT /api/products/{id}` for each changed row
- [x] "Confirm brief" button at bottom — calls `POST /api/brief/approve` with selected idea IDs

### Page: Analytics (`src/pages/Analytics.tsx`)

The Friday 15:00 review slot — weekly performance at a glance.

- [ ] Week selector (defaults to current week)
- [x] Summary row — 5 metric cards:
  - Total views, Total GMV, Avg CTR, Best-performing product, Videos published
- [x] Views over time — `Recharts` `AreaChart` — one line per platform (TikTok, Reels, Shorts)
- [x] GMV per video — `BarChart` — top 10 videos sorted by GMV, bars coloured by product
- [ ] Hook performance table:
  - Columns: hook text, avg watch time %, CTR, GMV, winner badge
  - Sortable by any column
  - Winner rows highlighted in green
- [ ] Winner approval panel:
  - Cards for top 3 videos flagged as winners
  - Each card: thumbnail, hook, metrics summary, "Approve remix" button
  - Approve remix calls `POST /api/analytics/video/{id}/approve-remix`

### Page: Products (`src/pages/Products.tsx`)

Manage affiliate products — used during the Monday 08:00 slot.

- [x] Product table with inline editing:
  - Columns: name, TikTok Shop URL, commission %, affiliate link, UTM campaign, approved
  - Every cell editable inline (click to edit)
  - Auto-save on blur
- [x] "Add product" button — opens a dialog form with all fields
- [x] "Delete" action per row with confirmation dialog
- [x] Commission rate displayed with colour coding: green ≥ 15%, amber 10–14%, red < 10%
- [ ] Validation: affiliate link must be a valid URL, commission must be 0–100

### Page: Schedule (`src/pages/Schedule.tsx`)

View automation job history and manually trigger jobs.

- [x] Today's schedule table:
  - Columns: job name, module, scheduled time, last run time, status, duration, actions
  - Status badge: `pending` / `running` / `done` / `failed` — live via WebSocket
  - "Run now" button per job (calls `POST /api/schedule/run/{job_name}`)
  - "Run now" disabled while job is running
- [ ] Job log panel:
  - Click any job to see its last 100 log lines
  - Auto-scrolls to bottom
  - Log lines colour-coded: INFO = default, WARNING = amber, ERROR = red
- [ ] 7-day job history calendar:
  - Grid: days as columns, jobs as rows
  - Each cell: coloured dot (green = success, red = failed, gray = did not run)

### Build and integration tasks

- [x] Add `npm run build` to output `dashboard/dist/`
- [x] Configure FastAPI to serve `dashboard/dist/index.html` for all non-API routes (SPA fallback)
- [x] Add `dashboard/dist/` to `.gitignore`
- [x] Write a `scripts/dev.sh` that starts FastAPI + Vite dev server concurrently:
  ```bash
  concurrently "uvicorn api.main:app --reload" "cd dashboard && npm run dev"
  ```
- [x] Write `dashboard/src/components/VideoPlayer.tsx`:
  - Accepts `videoId` prop
  - Fetches stream URL from `/api/videos/{id}/stream`
  - Native `<video>` with controls, poster from `/api/videos/{id}/thumbnail`
  - Handles loading and error states
- [x] Write `dashboard/src/components/JobTimeline.tsx`:
  - Accepts array of job status objects
  - Renders vertical stepper with time, name, status, duration
  - WebSocket hook updates statuses in real time

### Deliverable
`npm run dev` in `dashboard/` loads the app at `localhost:5173`. All 5 pages render with real data from the FastAPI backend. WebSocket connection shows live job status updates.

---

## Phase 11 — Testing & hardening

### Tasks

- [ ] Write end-to-end smoke test: research → script → voice → edit → publish (dry-run)
- [ ] Add dead-letter queue: failed Celery tasks retry 3× then move to `failed_jobs` table
- [ ] Add disk space guard: if `data/` > 10GB, archive clips older than 7 days to a `/archive/` folder
- [ ] Add cost tracker: log API credit usage per run (ElevenLabs chars, Kling credits, OpenAI tokens)
- [x] Write `scripts/daily_health_check.py` — runs all API auth checks, reports any failures by printing to console
- [ ] Document all env vars in `README.md` with setup instructions

### Deliverable
Full pipeline runs in dry-run mode without error. Health check passes.

---

## Human touchpoints summary

| Slot | Action | Dashboard page | Time |
|---|---|---|---|
| Mon 07:00 | Read AI brief, toggle ideas on/off, confirm plan | Content Brief | 20 min |
| Mon 08:00 | Paste affiliate links, set approved toggle per product | Products | 15 min |
| Tue–Fri 11:00 | Watch 5 videos, approve or reject each | QC Review | 15–20 min |
| Fri 15:00 | Review weekly charts, check GMV + top hooks | Analytics | 20 min |
| Fri 21:00 | Approve winners for remix from the winner panel | Analytics | 10 min |
| Sat 11:00 | Light QC scan of weekend batch | QC Review | 10 min |

**Total: ~90 min/week. All actions done in the browser — no terminal required after setup.**

---

## Implementation order for Claude

Work strictly in this order. Do not start a phase until the previous phase's deliverable is confirmed.

```
Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 →
Phase 5 → Phase 6 → Phase 7 → Phase 8 → Phase 9 →
Phase 10 (API) → Phase 10b (Dashboard) → Phase 11
```

When implementing each phase:
1. Create all files and folder structure first
2. Write the models/DB layer before business logic
3. Write the core logic
4. Write tests
5. Run and confirm the deliverable
6. Check off all tasks in this plan before moving on

---

## Notes for Claude

- Always use `python-dotenv` to load `.env` — never hardcode credentials
- All file paths must use `pathlib.Path` — no raw string paths
- All API calls must have timeout (30s default) and retry (3× with exponential backoff)
- Use `loguru` for all logging — structured JSON logs to `data/logs/`
- Database migrations via `alembic` — never alter tables manually
- Video files are large — always check disk space before writing new assets
- TikTok API rate limits: respect `x-ratelimit-remaining` headers, back off when < 10
- When in doubt on an API — check the official docs URL in `README.md` before guessing parameters

**Dashboard-specific notes:**
- All API responses must have matching Pydantic response models — no raw dicts returned from routes
- The React dashboard is a pure SPA — all routing is client-side via React Router, FastAPI only handles `/api/*` and the SPA fallback
- Never block the FastAPI event loop — use `asyncio.to_thread()` for any synchronous DB or file operations inside async route handlers
- Video streaming must use `StreamingResponse` with `Range` header support so the browser video player can seek
- WebSocket events are append-only — never send state, always send events; the frontend maintains its own state via React Query
- Dashboard components must handle loading, empty, and error states explicitly — no unhandled promise rejections
- Use `shadcn/ui` components as the base for all UI — do not write raw Tailwind utility classes for layout that shadcn already provides
- All dashboard pages must work on mobile width (375px min) — the QC review page is the most used and must be usable on a phone
