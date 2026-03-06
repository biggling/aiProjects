# Build Plan: autoGenVideo — AI Video Generation Automation SaaS

**Goal:** Auto-generate and publish 50+ short-form videos/day to TikTok, YouTube Shorts, Instagram Reels, Pinterest targeting SEA markets (Thailand, Vietnam, Indonesia)
**Reference Prompt:** `prompt_auto_gen_video.md`
**Business Reference:** `business_gencnx.md`
**Status:** Phase 1–8 Complete | Phase 9 (TikTok Shop) + Phase 10 (SaaS Productization) Pending

---

## Phase Overview

| Phase | Days | Focus | Milestone |
|---|---|---|---|
| Phase 1 | 1–7 | Foundation: scaffold, DB, config, FastAPI shell | Infra ready |
| Phase 2 | 8–14 | Jobs 1–2: Trend research + Script generation | Scripts auto-generating |
| Phase 3 | 15–21 | Jobs 3–4: Media assembly + Video rendering | MP4 output working |
| Phase 4 | 22–28 | Job 5: Multi-platform publishing | First auto-posts live |
| Phase 5 | 29–42 | Jobs 6–7: Analytics + Optimization loop | Data feedback loop |
| Phase 6 | 43–56 | Job 8: Viral trend monitoring | 30-min trend reaction |
| Phase 7 | 57–63 | Job 9: TikTok Shop product automation | Key differentiator live |
| Phase 8 | 64–70 | FastAPI REST + cost tracking + brand config | API-first SaaS ready |
| Phase 9 | 71–90 | Stripe billing + multi-tenant + Redis + production | $19/$49/$99 tiers live |

---

## Tech Stack (Validated March 2026)

| Layer | Tool | Notes |
|---|---|---|
| Language | Python 3.11+ | Async-first |
| Web Framework | FastAPI + Uvicorn | OpenAPI auto-docs |
| Scheduling | APScheduler (async) | cron + interval + event triggers |
| AI Script Gen | `anthropic` (`claude-sonnet-4-6`) | Best for structured JSON scripts |
| AI Video | Sora 2 API ($0.10/sec) → Veo 3.1 Fast ($0.15/sec) fallback | Cost-first: use asset_compose by default |
| AI Image Gen | OpenAI DALL-E 3 / Stability AI | Scene images |
| TTS (Cloud) | ElevenLabs API | Multilingual, natural voices |
| TTS (Self-hosted) | Kokoro / XTTS-v2 (Coqui) | Zero COGS; XTTS-v2 supports Thai/VI |
| Video Rendering | `python-ffmpeg` + `Movis` | **NOT** `ffmpeg-python` (unmaintained) |
| Image Processing | Pillow + OpenCV | Resize, overlay, color grading |
| Trend Data | `pytrends`, YouTube Data API v3, PRAW, `feedparser` | Cross-platform signals |
| TikTok API | `tiktok-api-client` (PyPI) | Official OAuth 2.0 |
| YouTube API | `google-api-python-client` | `videos.insert` auto-classifies as Shorts |
| Instagram API | Instagram Graph API via `httpx` | Business accounts only |
| Pinterest API | Pinterest API v5 via `httpx` | Idea Pins |
| Database | PostgreSQL (prod) + SQLite (dev), SQLAlchemy + Alembic | Multi-tenant |
| Caching / State | Redis | Rate limit, job state, queue |
| Reporting | pandas + Jinja2 | Performance reports |
| Notifications | `slack-sdk` + Telegram Bot API | Alerts |
| Config | `python-dotenv` | Secrets management |
| Payments | Stripe API | Subscription billing, usage metering |

---

## Phase 1: Foundation (Days 1–7) ✅

### 1.1 Project Scaffold

**Directory Structure:**
```
autoGenVideo/
├── .env                            # Never commit
├── .env.example                    # API key template
├── requirements.txt
├── config.py                       # .env loader, constants, paths
├── main.py                         # CLI: --init-db | --scheduler | --job N | --api
├── scheduler.py                    # APScheduler job registry
├── api/
│   ├── __init__.py
│   └── main.py                     # FastAPI app + REST endpoints
├── database/
│   ├── __init__.py
│   ├── models.py                   # SQLAlchemy ORM (6 tables + tiktok_shop_products)
│   ├── migrations/                 # Alembic migrations (prod)
│   └── init_db.py                  # Schema creation (idempotent)
├── jobs/
│   ├── job1_content_research.py
│   ├── job2_script_generation.py
│   ├── job3_media_assembly.py
│   ├── job4_video_rendering.py
│   ├── job5_publishing.py
│   ├── job6_analytics.py
│   ├── job7_optimization.py
│   ├── job8_trend_monitoring.py
│   └── job9_tiktok_shop.py         # KEY DIFFERENTIATOR — to build
├── utils/
│   ├── ai_utils.py                 # Claude + OpenAI wrappers
│   ├── tts_utils.py                # ElevenLabs + Kokoro/XTTS-v2 switcher
│   ├── video_utils.py              # python-ffmpeg + Movis rendering
│   ├── platform_api.py             # TikTok, YouTube, Instagram, Pinterest
│   ├── cost_tracker.py             # Per-user AI API cost logging — to build
│   └── notify.py                   # Slack + Telegram alerts
├── assets/
│   ├── fonts/
│   ├── music/                      # Royalty-free background tracks
│   └── templates/                  # Brand overlays, end screens, price badges
├── storage/                        # User video/asset storage (→ S3 in prod)
├── reports/
├── logs/
└── tests/
```

### 1.2 Required API Keys (`.env.example`)

```
# AI
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
ELEVENLABS_API_KEY=
STABILITY_API_KEY=

# Video Platforms
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=
YOUTUBE_API_KEY=
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ACCOUNT_ID=
PINTEREST_ACCESS_TOKEN=

# TikTok Shop
TIKTOK_SHOP_APP_KEY=
TIKTOK_SHOP_APP_SECRET=
TIKTOK_SHOP_ACCESS_TOKEN=

# Content APIs
PEXELS_API_KEY=
PIXABAY_API_KEY=
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=

# Infrastructure
REDIS_URL=redis://localhost:6379/0
DATABASE_URL=sqlite:///autoGenVideo.db
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Notifications
SLACK_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# App
MAX_VIDEOS_PER_DAY=50
VIDEO_RESOLUTION=1080x1920
VIDEO_FPS=30
VIDEO_BITRATE=8M
DEFAULT_LANGUAGE=th
DEFAULT_MARKET=TH
```

### 1.3 Database Schema (7 Tables)

| Table | Purpose |
|---|---|
| `users` | Multi-tenant user accounts (plan, Stripe ID) |
| `topics` | Trending content ideas (per user, per market) |
| `scripts` | Generated video scripts (A/B variants) |
| `videos` | Rendered MP4 files + actual API cost |
| `publications` | Platform post records (post IDs, URLs) |
| `analytics` | Platform performance metrics |
| `tiktok_shop_products` | TikTok Shop affiliate product automation |

**Full schema in `prompt_auto_gen_video.md` (PostgreSQL DDL)**

### 1.4 Dependencies (`requirements.txt`)

**Core:**
```
anthropic>=0.40.0
openai>=1.50.0
fastapi>=0.115.0
uvicorn>=0.32.0
apscheduler>=3.10.4
sqlalchemy>=2.0.36
alembic>=1.13.0
asyncpg>=0.30.0
python-dotenv>=1.0.1
httpx>=0.27.0
redis>=5.1.0
```

**Video (CORRECTED):**
```
python-ffmpeg>=2.0.0          # NOT ffmpeg-python (unmaintained since 2019)
movis>=0.4.0
Pillow>=11.0.0
opencv-python>=4.10.0
pydub>=0.25.1
elevenlabs>=1.9.0
```

**Scraping / Data:**
```
pytrends>=4.9.2
beautifulsoup4>=4.12.3
praw>=7.7.1
feedparser>=6.0.11
google-api-python-client>=2.150.0
```

**Platform / Billing:**
```
tiktok-api-client>=1.0.0
slack-sdk>=3.33.0
stripe>=11.0.0
tenacity>=9.0.0
pandas>=2.2.0
jinja2>=3.1.0
```

**System requirement:** `ffmpeg` installed via OS package manager (`apt install ffmpeg`)

---

## Phase 2: Jobs 1–2 — Research + Scripts (Days 8–14) ✅

### 2.1 Job 1: Content & Trend Research

**File:** `jobs/job1_content_research.py`
**Schedule:** Every 4 hours

**Data sources:**
1. Google Trends via `pytrends` (geo: TH, VN, ID) — rising queries
2. YouTube Trending — YouTube Data API v3 (region + category)
3. Reddit hot posts — PRAW (niche subreddits, configurable)
4. Google News RSS — `feedparser` (breaking news)
5. TikTok trending hashtags — HTML scraper (no official trending API)
6. **TikTok Shop** — Top-selling products via TikTok Shop Affiliate API

**Scoring formula:**
```
score = (trend_velocity × 0.5) + (engagement_signals × 0.3) + (freshness_bonus × 0.2)
```
- `trend_velocity`: % rise in last 4h vs. 24h baseline
- `engagement_signals`: YouTube view velocity, Reddit upvotes
- `freshness_bonus`: +0.3 if topic < 6h old

**Output:** Top 10 topics per user written to `topics` table (`status=pending`)

**Rate limits:**
- YouTube API: 10,000 quota units/day — 1 call per 4h
- pytrends: 5s between requests, rotate user-agents
- Reddit: PRAW handles automatically

### 2.2 Job 2: Script & Content Generation

**File:** `jobs/job2_script_generation.py`
**Schedule:** Triggered by Job 1 (or every 4h)

**Script output (JSON per video):**
```json
{
  "hook": "3-second attention grabber",
  "body": "Core educational/promotional content",
  "cta": "Like and follow for more!",
  "caption": "Platform caption (150 chars TikTok display)",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"],
  "voiceover_text": "Full voiceover script for TTS",
  "hook_variants": ["variant_b_hook", "variant_c_hook"]
}
```

**Claude API:**
- Model: `claude-sonnet-4-6`
- Temperature: 0.8 (creative)
- Language: TH | VI | ID | EN | multilingual
- Max tokens: 1024

**Validation:**
- Hook: ≤ 15 words
- 30s video: ~75 words voiceover; 60s: ~150 words
- Log estimated cost: `Sora_seconds × $0.10 + TTS_chars × $0.0001`

---

## Phase 3: Jobs 3–4 — Media + Rendering (Days 15–21) ✅

### 3.1 Job 3: Media Asset Generation

**File:** `jobs/job3_media_assembly.py`
**Schedule:** Triggered by Job 2

**Asset pipeline:**
1. Parse script into scene breakdown (1 image per scene segment)
2. Per scene: Pexels/Pixabay API first (free stock), DALL-E 3 fallback
3. Resize all assets to 1080×1920px (9:16 portrait)
4. Color grade via Pillow (contrast +10%, saturation +15%)
5. Generate text overlay for hook (large font, bottom-center)
6. Generate end screen (brand logo + CTA button)
7. Apply brand palette and font from user brand config

**Storage:** `/storage/{user_id}/{script_id}/assets/`

### 3.2 Job 4: Video Rendering

**File:** `jobs/job4_video_rendering.py`
**Schedule:** Triggered by Job 3

**Rendering modes:**
- **`asset_compose` (default):** `python-ffmpeg` + `Movis` — near-zero COGS, use for all Starter/Free tier
- **`ai_generate`:** Sora 2 API ($0.10/sec) or Veo 3.1 Fast ($0.15/sec) — Pro tier "hero" videos only

**`asset_compose` pipeline:**
```
1. Generate TTS voiceover (ElevenLabs → OpenAI TTS → Kokoro fallback)
2. Sync voiceover timing to scene timeline
3. Assemble image scenes with Ken Burns zoom/pan (Movis)
4. Add word-by-word caption overlay synced to voiceover timestamps
5. Mix background music (royalty-free, -20dB under voiceover)
6. Add brand watermark (corner, configurable opacity)
7. Add end screen: CTA card with follow/shop animation (last 3s)
8. Export: 1080×1920 MP4, H.264, 30fps, 8Mbps, max 60s
9. Log actual API cost to videos.api_cost_usd
```

**TTS priority:**
1. ElevenLabs (quality, multilingual, $0.0001/char)
2. OpenAI TTS (gpt-4o-mini-tts, 6 voices)
3. Kokoro / XTTS-v2 self-hosted (zero COGS, Thai/VI support)

**Performance target:** < 2 min render/60s video (CPU) | < 30s (GPU)

---

## Phase 4: Job 5 — Multi-Platform Publishing (Days 22–28) ✅

### 4.1 Job 5: Publishing

**File:** `jobs/job5_publishing.py`
**Schedule:** Every 2 hours (staggered per platform)

**Platform requirements:**

| Platform | API | Max Length | Caption |
|---|---|---|---|
| TikTok | `tiktok-api-client` (OAuth 2.0) | 60s | 2200 chars |
| YouTube Shorts | `google-api-python-client` `videos.insert` | 60s | 5000 chars |
| Instagram Reels | Instagram Graph API (Business account) | 60s | 2200 chars |
| Pinterest Idea Pins | Pinterest API v5 | 60s | 500 chars |

**Publishing flow:**
1. Read `videos` with `status=ready`
2. Select platform based on stagger schedule
3. Upload via platform API + set metadata
4. Record post URL + ID in `publications`
5. Update video `status=published`
6. Alert via Slack/Telegram

**Optimal posting times (local):**
```
TikTok (TH/VI): 19:00–22:00 daily; 12:00–14:00 Tue–Fri
YouTube Shorts: 15:00–18:00 Mon, Wed, Fri
Instagram Reels: 11:00, 17:00, 20:00 daily
Pinterest: 20:00–23:00 daily
```

**Rate limits:**
- TikTok: 100 posts/day/account
- YouTube: 6/day (unverified), unlimited (verified)
- Instagram: 25 API calls/hour
- Pinterest: 150 pins/day

---

## Phase 5: Jobs 6–7 — Analytics + Optimization (Days 29–42) ✅

### 5.1 Job 6: Analytics Tracking

**File:** `jobs/job6_analytics.py`
**Schedule:** Every 6 hours

**Metrics:** views, likes, comments, shares, watch_time_avg, engagement_rate, CTR

**KPI thresholds:**
- Viral: > 10,000 views in 24h → Slack/Telegram alert
- Good: engagement_rate > 5%
- Underperformer: < 200 views after 48h → flag for Job 7

**TikTok Shop ROI:** `revenue_per_video = affiliate_clicks × avg_commission`

### 5.2 Job 7: Content Optimization & Regeneration

**File:** `jobs/job7_optimization.py`
**Schedule:** Daily at 02:00 local market time

**Decision logic:**
```
Video after 48h:
  views < 200           → regenerate with new hook (Jobs 2→3→4→5)
  views 200–1000, ER<3% → update caption/hashtags only
  views > 1000          → generate 3 similar videos on same topic
  viral (>10k)          → replicate immediately + cross-post all platforms
```

**Hook improvement via Claude:**
```
Original hook underperformed ({views} views, 48h).
Top performers use: question hooks, bold claims, curiosity gaps.
Generate 3 improved hooks for "{topic}" targeting {market}.
Return JSON: {"hooks": ["h1", "h2", "h3"]}
```

---

## Phase 6: Job 8 — Viral Trend Monitoring (Days 43–56) ✅

### 6.1 Job 8: Real-Time Trend Detection

**File:** `jobs/job8_trend_monitoring.py`
**Schedule:** Every 30 minutes

**Data sources (fast/real-time):**
1. Google Trends real-time (`pytrends` `now 1-H` timeframe)
2. Reddit rising posts (PRAW hot filter, freshness < 2h)
3. RSS feeds: BBC, CNN, TechCrunch, regional SEA news
4. Google News trending (`feedparser`)

**Velocity threshold:**
```
velocity = (current_volume / 24h_ago_volume) - 1
```
- velocity > 2.0 (200% rise) → alert + auto-trigger Job 2

**Content-to-post target:** < 4 hours from trend detection to published video

---

## Phase 7: Job 9 — TikTok Shop Product Automation (Days 57–63) 🔲 TO BUILD

### 7.1 Job 9: TikTok Shop Product Automation (Key Differentiator)

**File:** `jobs/job9_tiktok_shop.py`
**Schedule:** Triggered on product add OR daily batch for catalog items

**Purpose:** Auto-generate product review/promo videos from TikTok Shop affiliate links. This is the primary differentiator vs. competitors (HeyGen, Synthesia, GenCNX).

**Inputs:**
- TikTok Shop product URL or affiliate product ID
- Target market/language: TH | VI | ID | EN
- Review style: `honest_review` | `unboxing` | `comparison` | `how_to_use`

**Outputs:**
- Product video MP4 in `/storage/{user_id}/{product_id}/final.mp4`
- Posted to TikTok with affiliate link in bio/caption
- Tracked in `tiktok_shop_products` table

**Pipeline tasks:**
1. Scrape product data via `httpx`: title, price, description, images, ratings, review count
2. Generate localized product review script via Claude (TH/VI/ID)
   - Template: `honest_review` (pros/cons/price), `unboxing` (reveal + reaction), etc.
3. Fetch/generate scene visuals: product images + lifestyle B-roll (Pexels)
4. Render video with Movis: price badge overlay, affiliate CTA ("Shop link in bio!")
5. Post to TikTok via `tiktok-api-client` with affiliate link in caption
6. Track clicks/conversions via TikTok Shop Affiliate API
7. Auto-regenerate high-converting products weekly with fresh angles

**Claude prompt template (TikTok Shop):**
```
You are a viral TikTok product review creator for {market} market (language: {language}).
Create a {duration}s {review_style} video script for this product:

Product: {product_name}
Price: {price}
Key features: {features}
Rating: {rating} ({review_count} reviews)
Affiliate URL: {affiliate_url}

Return JSON:
{
  "hook": "Attention-grabbing opener (3 seconds)",
  "body": "Product review content highlighting value",
  "cta": "Shop link in bio! [affiliate CTA]",
  "caption": "TikTok caption (150 chars) with shop hashtags",
  "hashtags": ["#TikTokShop", "#niche_tag", ...],
  "voiceover_text": "Full TTS script",
  "price_badge_text": "Only {price}!"
}
```

**Libraries:**
```
httpx, anthropic, tiktok-api-client, Pillow (price badge overlay), asyncpg
```

---

## Phase 8: FastAPI REST + Cost Tracking (Days 64–70) 🔲 PARTIAL

### 8.1 FastAPI REST Endpoints

**File:** `api/main.py`
**Auth:** Bearer token (API key per user)

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/v1/video/generate` | POST | Submit topic → full pipeline |
| `/api/v1/video/generate-from-url` | POST | Product URL → TikTok Shop video |
| `/api/v1/video/{id}/status` | GET | Generation status |
| `/api/v1/video/{id}/download` | GET | Download MP4 |
| `/api/v1/video/{id}/publish` | POST | Manual publish trigger |
| `/api/v1/analytics/summary` | GET | Dashboard stats |
| `/api/v1/analytics/roi` | GET | Revenue vs. cost breakdown |
| `/api/v1/topics/trending` | GET | Current trending topics |
| `/api/v1/script/generate` | POST | Script only (no video) |
| `/api/v1/jobs/status` | GET | Scheduler health check |
| `/api/v1/usage/cost` | GET | AI API cost tracker per user |
| `/api/v1/brand/config` | POST | Set brand voice, colors, logo |
| `/api/v1/shop/products` | GET | TikTok Shop product catalog |

### 8.2 Cost Tracking Utility

**File:** `utils/cost_tracker.py` — TO BUILD

**Purpose:** Log actual AI API spend per video, per user. Critical for margin monitoring.

**Cost tracking points:**
- Sora 2 / Veo 3.1: `duration_seconds × cost_per_second`
- ElevenLabs TTS: `char_count × $0.0001`
- DALL-E 3: `$0.04/image` (1024×1024 standard)
- Claude API: `input_tokens × $0.000003 + output_tokens × $0.000015`

**Functions needed:**
```python
log_video_cost(video_id, user_id, api, cost_usd)
get_user_monthly_cost(user_id, month)
get_cost_by_video(video_id)
check_user_budget_limit(user_id)   # enforce tier COGS caps
```

**COGS caps by tier:**
```
Free:    $0.50/user/mo  (5 videos × $0.10 Sora or ~5 asset_compose)
Starter: $3.00/user/mo  (84% GM target — asset_compose mode only)
Pro:     $8.00/user/mo  (84% GM — mixed asset_compose + selective Sora)
Agency:  custom         (70%+ GM target)
```

---

## Phase 9: SaaS Productization — Stripe + Multi-tenant + Redis (Days 71–90) 🔲 TO BUILD

### 9.1 Stripe Billing Integration

**Tiers:**

| Feature | Free | Starter ($19/mo) | Pro ($49/mo) | Agency ($99/mo) |
|---|---|---|---|---|
| Videos/month | 5 (watermarked) | 30 | 150 | Unlimited |
| Platforms | TikTok only | All 4 | All 4 | All 4 + custom |
| Languages/TTS | EN only | EN + TH | EN + TH + VI + ID | All |
| TikTok Shop auto-video | No | 10 products | 50 products | Unlimited |
| API access | No | No | 1,000 calls/mo | Unlimited |
| Analytics | Basic | Full | Full + AI insights | Full + white-label |
| A/B testing | No | No | Yes | Yes |
| Brand kit | No | 1 brand | 3 brands | Unlimited |

**Stripe setup:**
- Products: 4 tiers (Free, Starter, Pro, Agency)
- Usage metering: video generation events reported to Stripe
- Webhooks: `customer.subscription.updated`, `invoice.payment_failed`
- Enforce limits in `api/main.py` middleware: check `users.plan` + monthly video count

### 9.2 Redis Integration

**Use cases:**
- Rate limit management per user (job execution frequency)
- Job state caching (avoid duplicate job runs)
- Session/token caching
- Rendering queue depth tracking
- Pub/sub for job completion events (Job 3 done → trigger Job 4)

**Key patterns:**
```
rate_limit:{user_id}:{job_name}    TTL = job_interval
job_state:{job_id}                  Hash with status, progress
user_quota:{user_id}:videos        Counter, reset monthly
```

### 9.3 Multi-tenant PostgreSQL Migration

**Migration from SQLite to PostgreSQL:**
1. Alembic `env.py` configured for async PostgreSQL (asyncpg)
2. All tables include `user_id UUID` FK to `users`
3. Row-level isolation: all queries filter by `user_id`
4. Connection pool: `asyncpg` pool with 10–50 connections

**Production deployment checklist:**
- PostgreSQL 16+ with `pgcrypto` extension (for `gen_random_uuid()`)
- Redis 7.0+
- S3/R2 for `storage/` (replace local filesystem)
- Nginx reverse proxy for FastAPI
- Systemd service for scheduler

---

## Build Order (Recommended)

1. ✅ **Phase 1** — Scaffold + DB + Config + FastAPI shell
2. ✅ **Job 1** — Trend Research
3. ✅ **Job 2** — Script Generation (Claude API)
4. ✅ **Job 3** — Media Assembly (Pexels + DALL-E 3)
5. ✅ **Job 4** — Video Rendering (asset_compose mode: python-ffmpeg + Movis + TTS)
6. ✅ **Job 5** — Publishing (TikTok + YouTube)
7. ✅ **Job 6** — Analytics Tracking
8. ✅ **Job 7** — Optimization & Regeneration
9. ✅ **Job 8** — Viral Trend Monitoring
10. 🔲 **Job 9** — TikTok Shop Product Automation
11. 🔲 **cost_tracker.py** — AI API cost logging utility
12. 🔲 **FastAPI** — Add `/generate-from-url`, `/usage/cost`, `/brand/config`, `/shop/products`
13. 🔲 **Stripe** — Billing tiers, usage metering, webhook handler
14. 🔲 **Redis** — Rate limiting, job state, quota enforcement
15. 🔲 **PostgreSQL migration** — Alembic, asyncpg, multi-tenant row-level isolation

---

## Dependencies Between Jobs

```
Job 1 (Research) ──► Job 2 (Scripts) ──► Job 3 (Media) ──► Job 4 (Rendering) ──► Job 5 (Publish)
                                                                                         │
Job 8 (Trend Monitor) ──► [auto-trigger Job 2 on velocity spike]                        │
                                                                                         ▼
Job 9 (TikTok Shop) ──► [own pipeline: scrape → script → render → post]          Job 6 (Analytics)
                                                                                         │
                                                                                         ▼
                                                                                   Job 7 (Optimize)
                                                                                   [trigger Job 2→3→4→5]
```

Database is the integration layer. No direct function calls between jobs — fully decoupled.

---

## Risk & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| TikTok API restrictions | No auto-posting | Playwright browser automation fallback |
| Sora 2 / DALL-E cost overrun | Negative margin | Default `asset_compose` mode; Sora only for Pro "hero" videos |
| Instagram Graph API rate limits | Post failures | Queue + exponential backoff (tenacity) |
| TikTok Shop affiliate scraping breaks | Job 9 fails | Fallback to manual product data entry via API |
| Video rendering slow | Pipeline bottleneck | GPU acceleration flag; pre-generate assets async |
| Platform TOS violation | Account ban | Stay within official API limits; no automation flagging |
| Stripe webhook missed | Subscription not updated | Idempotent handlers + reconciliation cron |
| Redis failure | Rate limits bypass | Graceful degradation: fall back to DB-based rate counting |

---

## Success Metrics

| Metric | Week 2 | Week 4 | Week 8 | Week 12 |
|---|---|---|---|---|
| Videos generated/day | 5 | 20 | 50 | 100+ |
| Platforms live | 1 (YouTube) | 3 | 4 | 4 + API |
| Avg views/video | — | 500 | 2,000 | 10,000+ |
| Viral videos (>10k) | 0 | 1 | 5 | 20+ |
| TikTok Shop products auto-posted | — | — | 20 | 100+ |
| Paying SaaS users | — | — | 5 | 25+ |
| Monthly SaaS revenue | — | — | $100 | $500+ |

---

## Status Log

| Date | Phase | Status | Notes |
|---|---|---|---|
| 2026-03-06 | Planning | ✅ Complete | plan_build_auto_gen_video.md created + updated |
| 2026-03-06 | Phase 1: Scaffold | ✅ Complete | config.py, requirements.txt, .env.example, directory structure |
| 2026-03-06 | Phase 1: DB Models | ✅ Complete | models.py (5 tables), init_db.py — missing tiktok_shop_products |
| 2026-03-06 | Phase 1: Utils | ✅ Complete | ai_utils, tts_utils, video_utils, platform_api, notify |
| 2026-03-06 | Job 1: Research | ✅ Complete | pytrends + YouTube + Reddit + RSS feeds |
| 2026-03-06 | Job 2: Scripts | ✅ Complete | Claude API (claude-sonnet-4-6) script generation |
| 2026-03-06 | Job 3: Media | ✅ Complete | Pexels + DALL-E 3 scene image generation |
| 2026-03-06 | Job 4: Rendering | ✅ Complete | MoviePy + TTS — NOTE: needs migration to python-ffmpeg + Movis |
| 2026-03-06 | Job 5: Publishing | ✅ Complete | YouTube + TikTok API publishing |
| 2026-03-06 | Job 6: Analytics | ✅ Complete | Platform stats collection + daily report |
| 2026-03-06 | Job 7: Optimization | ✅ Complete | Underperform remake + viral replication |
| 2026-03-06 | Job 8: Trend Monitor | ✅ Complete | 30-min Google Trends + RSS polling |
| 2026-03-06 | FastAPI (partial) | ✅ Complete | 6 REST endpoints + API key auth |
| 2026-03-06 | Scheduler | ✅ Complete | APScheduler + main.py CLI |
| — | Job 9: TikTok Shop | 🔲 Pending | Key differentiator — product URL → auto video → post |
| — | cost_tracker.py | 🔲 Pending | Per-user AI API cost logging utility |
| — | requirements.txt fix | 🔲 Pending | Replace ffmpeg-python with python-ffmpeg; add movis, redis, stripe |
| — | Stripe billing | 🔲 Pending | $19/$49/$99 tiers + webhook handler |
| — | Redis integration | 🔲 Pending | Rate limits, job state, quota enforcement |
| — | PostgreSQL migration | 🔲 Pending | Alembic + asyncpg + multi-tenant isolation |

## Known Technical Debt

1. **`requirements.txt`** — uses `ffmpeg-python` (unmaintained since 2019). Must replace with `python-ffmpeg>=2.0.0` + add `movis>=0.4.0`
2. **Job 4** — built with MoviePy, should migrate to `python-ffmpeg` + `Movis` per tech stack spec
3. **`database/models.py`** — missing `tiktok_shop_products` table
4. **No cost tracking** — `utils/cost_tracker.py` not yet built; `videos.api_cost_usd` not being populated
5. **No multi-tenant isolation** — current DB schema lacks `user_id` FK enforcement in all tables
6. **No Redis** — job state management is in-memory only; loses state on restart

## Next Steps for Current Build Session

1. `pip install python-ffmpeg movis redis stripe tiktok-api-client` (update requirements.txt)
2. Build `jobs/job9_tiktok_shop.py` (TikTok Shop product automation)
3. Build `utils/cost_tracker.py` (AI API cost logging)
4. Add `tiktok_shop_products` table to `database/models.py` + run migration
5. Extend `api/main.py` with remaining endpoints (`/generate-from-url`, `/usage/cost`, `/shop/products`)
6. Add Redis rate limiting to job scheduler
7. Add Stripe billing integration
8. Test full pipeline: `python main.py --init-db` → `--job 1` → `--job 2` → `--job 9`
