# Prompt: Design High-Level Python Automation for AI Video Generation Business
**Research Date:** 2026-03-06 | **Market Data:** Current (web-validated)

---

## Business Context & Market Intelligence

### Market Opportunity (Validated March 2026)
- **SEA TikTok Users:** 460M+ (Indonesia 160M, Vietnam 70M, Thailand 50M)
- **TikTok Shop GMV H1 2025:** Thailand $4.6B, Indonesia $6B, Vietnam $3.4B
- **ASEAN Digital Economy:** $300B+ in 2025; AI projected to handle 80% of routine marketing tasks by 2026
- **20M+ content creators** in SEA; influencer marketing drives 20% of online sales
- **Critical Gap:** Native Thai/Vietnamese/Indonesian AI content generation is massively underserved

### Competitor Pricing Map (March 2026)
| Platform | Free | Entry Paid | Mid | High |
|---|---|---|---|---|
| HeyGen | $0 (3 vids, watermark) | $29/mo (200 credits) | $99/mo | $149/mo |
| Synthesia | $0 (36 min/yr) | $29/mo (10 min) | $89/mo | Enterprise |
| Invideo AI | $0 (10 min/wk, watermark) | $28/mo (50 min) | $50/mo | $100/mo |
| Runway Gen-4 | $0 (125 credits) | $15/mo (625 credits) | $35/mo | $95/mo |
| Pika Labs | $0 (150 credits) | $8/mo | $28/mo | $76/mo |
| Kling AI | $0 | $7-10/mo | $37/mo | $92/mo |
| **Our Target** | $0 (3 vids, watermark) | **$19/mo** | **$49/mo** | **$99/mo** |

**Pricing insight:** Kling undercuts market at $7-10/mo. Our entry at $19/mo must justify with SEA localization + auto-posting pipeline.

### AI Video API Cost Reality (Critical for Margins)
| Model | Cost/Second | 10-sec clip | 60-sec clip |
|---|---|---|---|
| OpenAI Sora 2 | $0.10/sec | **$1.00** | $6.00 |
| Google Veo 3.1 Fast | $0.15/sec | $1.50 | $9.00 |
| Google Veo 3.1 Standard | $0.40/sec | $4.00 | $24.00 |
| Google Veo 3.0 Full | $0.75/sec | $7.50 | $45.00 |

**Gross margin warning:** AI SaaS averages ~52% GM (vs. 80-90% traditional SaaS). At $19/mo entry with 30 videos/mo cap using Sora 2 ($1/clip × 30 = $30 COGS) → **negative margin**. Must batch-optimize, use Veo Fast for drafts, only render final quality on approved scripts.

### Platform Performance Benchmarks (2026)
| Platform | Avg Engagement Rate | RPM (SEA creators) | Advertiser CPM |
|---|---|---|---|
| YouTube Shorts | 3.4–5.91% | $0.003–$0.015/1K | $3–$7 |
| TikTok | 2.5–4.64% | $0.40–$1.00/1K (Creator Rewards) | $1–$4 |
| Instagram Reels | 0.48–1.48% | $0.01–$0.05/1K | $5–$10 |
| Pinterest Idea Pins | 1–3% | — | $2–$5 |

**Revenue reality:** Creator RPM in SEA is too low for a channel-only model. Primary monetization must be **the tool itself** + TikTok Shop affiliate commissions, not ad revenue.

---

## Core Model

**Input:** URL / text topic / product URL / niche keyword / TikTok Shop product
**Process:** Trend research → AI script (Claude) → TTS voiceover → visual assets → video render → auto-post → analytics → optimize
**Output:** Auto-published short-form videos on TikTok, YouTube Shorts, Instagram Reels, Pinterest
**Revenue Streams:**
1. SaaS subscriptions (Freemium → $19 → $49 → $99/mo)
2. TikTok Shop affiliate auto-video (per-video commission sharing)
3. White-label agency licenses ($500–$2,000/mo)
4. API access for developers ($0.05/video call, volume tiers)

**Target Market (Priority Order):**
1. **TikTok Shop sellers** (Thailand, Vietnam, Indonesia) — product review auto-videos
2. **Content creators** (Thai/Vietnamese YouTubers, TikTokers) — topic automation
3. **Digital agencies** (batch video production for clients)
4. **E-commerce brands** (product ad videos, multilingual)

**Key Differentiators vs. GenCNX / Competitors:**
- Full pipeline: generate → schedule → **auto-post** → track → optimize (GenCNX lacks auto-posting)
- SEA-native multilingual TTS (Thai, Vietnamese, Bahasa Indonesia, English)
- TikTok Shop product URL → auto video (massive SEA e-commerce opportunity)
- API-first for developer ecosystem
- Transparent cost preview before generation (HeyGen added this Feb 2026 as a feature — we launch with it)
- SEO blog/tutorials for organic acquisition (GenCNX has zero SEO)

---

## Prompt for AI Design Session

```
Design a high-level Python automation system for an AI Video Generation SaaS
targeting Southeast Asia content creators and TikTok Shop sellers.

The system must cover the full pipeline from trend research to multi-platform
auto-publishing and performance-driven content optimization with minimal manual
intervention.

Business constraints:
- Primary market: Thailand, Vietnam, Indonesia (Thai, Vietnamese, Bahasa UI/TTS)
- Target: TikTok Shop sellers who need product review videos automatically
- Revenue: SaaS $19/$49/$99/mo tiers + white-label + API
- COGS target: <40% of subscription revenue (use Sora 2 API at $0.10/sec as baseline)
- Target: 50+ videos/day per paying customer at Pro tier

Break the design into clearly separated automated job modules, each independently
schedulable (APScheduler/cron). Each module must define:
- Purpose and business value
- Inputs / Outputs / Data flows
- Python libraries (2025-2026 validated)
- Scheduling cadence and trigger logic
- Error handling and retry strategy

Target platforms: TikTok, YouTube Shorts, Instagram Reels, Pinterest Idea Pins
Content types: TikTok Shop product promos, educational explainers, trend-based clips
Video length: 15–60 seconds short-form

Technical constraints:
- Python 3.11+
- Async-first (asyncio, httpx)
- PostgreSQL in production, SQLite for local dev
- Secrets: .env / python-dotenv
- Modular: each job runs standalone
- API-first: FastAPI REST endpoints for external access
- Multi-tenant: each user/account has isolated job queue
- Cost tracking: log actual AI API spend per video, per user
```

---

## Validated Tech Stack (March 2026)

| Layer | Tool | Reason |
|---|---|---|
| Language | Python 3.11+ | Ecosystem, async support |
| Web Framework | FastAPI + Uvicorn | Async, OpenAPI auto-docs |
| Scheduling | APScheduler (async) | Cron + interval + trigger modes |
| AI Script Gen | Anthropic Claude API (`claude-sonnet-4-6`) | Best instruction-following for structured scripts |
| AI Video | Sora 2 API ($0.10/sec) → Veo 3.1 Fast ($0.15/sec) fallback | Cost-effective; Sora 2 most affordable at scale |
| AI Image Gen | OpenAI DALL-E 3 / Stable Diffusion 3 API | Scene images for non-video-gen clips |
| TTS (Cloud) | ElevenLabs API | Best quality; multilingual |
| TTS (Self-hosted) | Kokoro (open-source) or XTTS-v2 (Coqui) | Cost saving for high-volume; XTTS-v2 supports Thai/VI |
| Video Rendering | `python-ffmpeg` + `Movis` | MoviePy replacement; `python-ffmpeg` actively maintained; Movis for compositing |
| Image Processing | Pillow + OpenCV | Resize, overlay, color grading |
| Trend Data | `pytrends`, YouTube Data API v3, PRAW, feedparser | Cross-platform trend signals |
| TikTok API | `tiktok-api-client` (PyPI, Apr 2025) | Official TikTok Open API, OAuth 2.0 |
| YouTube API | `google-api-python-client` | Standard; `videos.insert` auto-classifies as Shorts |
| Instagram API | Instagram Graph API via `requests` | Business accounts only |
| Pinterest API | Pinterest API v5 via `requests` | Idea Pins |
| Database | PostgreSQL (prod) + SQLAlchemy + Alembic | Multi-tenant, migrations |
| Caching | Redis | Rate limit management, job state |
| Reporting | pandas + Jinja2 | Performance reports |
| Notifications | slack-sdk + Telegram Bot API | Alerts |
| Config | python-dotenv | Secrets management |
| Payments | Stripe API | Subscription billing, usage metering |

**Note:** `ffmpeg-python` is unmaintained (last commit ~2019). Use `python-ffmpeg` instead.

---

## High-Level System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                     AUTO GEN VIDEO SAAS PIPELINE                        │
│                                                                          │
│  [Job 1]         [Job 2]          [Job 3]          [Job 4]              │
│  Trend &         Script &         Media Asset       Video               │
│  Product  ────► Content    ────► Generation  ────► Rendering            │
│  Research        Generation                                              │
│                                                                          │
│  [Job 5]         [Job 6]          [Job 7]          [Job 8]              │
│  Multi-platform  Analytics &      Content          Real-time Trend      │
│  Publishing ───► Tracking   ────► Optimization ◄── Monitoring           │
│                                                                          │
│  [Job 9: TikTok Shop]                                                   │
│  Product URL → Script → Video → Post → Track Affiliate Clicks           │
└────────────────────────────────────────────────────────────────────────┘
                              │
                    [FastAPI Server]
                  REST API + Web Dashboard
                              │
                    [Multi-tenant DB]
               PostgreSQL (per-user job queues)
```

---

## Automated Job Modules

---

### Job 1: Content & Trend Research
**Purpose:** Identify trending topics, hashtags, and TikTok Shop product opportunities per niche

**Schedule:** Every 4 hours

**Inputs:**
- User-configured seed niches (e.g., "beauty", "tech", "food")
- Target platforms (TikTok, YouTube, Instagram)
- Language/market: TH | VI | ID | EN
- TikTok Shop product categories (for shop-seller users)

**Outputs:**
- `topics` table: `(id, user_id, topic, platform, trend_score, hashtags, source, market, discovered_at, status)`
- Top 10 scored topics queued for Job 2

**Tasks:**
- Fetch YouTube trending via YouTube Data API v3 (`videoCategoryId` filter)
- Fetch Google Trends rising topics via `pytrends` (geo: TH, VN, ID)
- Fetch Reddit hot posts for niche subreddits via `praw`
- Parse Google News RSS for trending topics via `feedparser`
- TikTok trending hashtags (scraper — no official trending API exists)
- **TikTok Shop:** Fetch top-selling products in category via TikTok Shop Affiliate API
- Score: `(trend_velocity × engagement_potential) / content_saturation`
- Filter: score > threshold AND not produced for this user in last 7 days

**Libraries:**
```
pytrends, httpx, beautifulsoup4, praw, google-api-python-client, feedparser, sqlite3/asyncpg
```

---

### Job 2: Script & Content Generation
**Purpose:** Generate video scripts, hooks, CTAs, captions, and A/B variants using Claude AI

**Schedule:** Triggered by Job 1 output or manual API call

**Inputs:**
- Topic from `topics` table
- Content type: `product_promo` | `educational` | `trending_clip` | `tiktok_shop_review`
- Duration: 15s | 30s | 60s
- Language: TH | VI | ID | EN | multilingual
- Brand voice (user config: casual | professional | energetic)
- Product data (if TikTok Shop mode: title, price, features, image URL)

**Outputs:**
- `scripts` table: `(id, user_id, topic_id, hook, body, cta, caption, hashtags, voiceover_text, language, duration_target, variant, estimated_cost, status)`
- 3 hook variants per script (for A/B testing)

**Tasks:**
- Generate hook (first 3 seconds — question, bold claim, or curiosity gap)
- Generate body script (educational/promotional content)
- Generate CTA (like, follow, comment, visit shop link)
- Generate platform-optimized caption (150 chars + 5 trending hashtags)
- Generate 3 hook variants (A/B test material)
- Translate to target language via Claude if multilingual
- Validate: word count vs. target duration (avg 2.5 words/sec for voiceover)
- Log estimated cost (Sora 2 seconds × $0.10 + TTS chars × $0.0001)

**Claude Prompt Template:**
```
You are a viral short-form video script writer for {market} market (language: {language}).
Create a {duration}s script for {platform} about "{topic}".

Context: {content_type}
{product_context if product_context else ""}
Brand voice: {brand_voice}

Return JSON:
{{
  "hook": "First 3 seconds — attention grabber",
  "body": "Core content (educational/product value)",
  "cta": "Call to action (engage/shop)",
  "caption": "Platform caption (150 chars max)",
  "hashtags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "voiceover_text": "Full script for TTS (hook + body + cta)",
  "hook_variants": ["variant_b", "variant_c"]
}}
```

**Libraries:**
```
anthropic (claude-sonnet-4-6), httpx, asyncpg
```

---

### Job 3: Media Asset Generation
**Purpose:** Generate or fetch visual assets — scene images, product shots, B-roll

**Schedule:** Triggered by Job 2 completion

**Inputs:**
- Script from `scripts` table
- Product images (from TikTok Shop product URL or user upload)
- Visual style: `minimalist` | `vibrant` | `corporate` | `trendy` | `thai_aesthetic`
- Brand config (colors, fonts, logo)

**Outputs:**
- `assets` table: `(id, script_id, user_id, type, file_path, source, created_at)`
- Scene images in `/storage/{user_id}/{script_id}/assets/`

**Tasks:**
- Generate scene images via DALL-E 3 or Stability AI (1 per scene segment)
- Fetch royalty-free B-roll from Pexels/Pixabay API for lifestyle/background
- Download product images from TikTok Shop product URLs
- Apply image transforms via Pillow: resize to 1080×1920 (9:16), color grade, crop
- Generate text overlay graphics: hook text card, lower thirds, price badges
- Apply brand palette and font from user brand config
- Generate thumbnail: key scene frame + text overlay + brand logo
- Validate: all assets are 1080×1920px (portrait) or 1920×1080px (landscape)

**Libraries:**
```
openai (DALL-E 3), httpx (Pexels/Pixabay/Stability AI), Pillow, opencv-python, asyncpg
```

---

### Job 4: Video Rendering
**Purpose:** Combine voiceover, assets, captions, music into final MP4

**Schedule:** Triggered by Job 3 completion

**Inputs:**
- Scene images/clips from `assets` table
- Voiceover text from `scripts` table
- Music mood: `energetic` | `calm` | `corporate` | `trendy`
- Caption style config (color, font, position, word-highlight mode)
- Video generation mode: `asset_compose` (Pillow+FFmpeg) | `ai_generate` (Sora 2/Veo)

**Outputs:**
- Final MP4 in `/storage/{user_id}/{script_id}/final.mp4`
- `videos` table: `(id, script_id, user_id, file_path, thumbnail_path, duration, resolution, api_cost_usd, status, created_at)`

**Tasks:**
- Generate TTS voiceover (ElevenLabs for quality, or Kokoro/XTTS-v2 for cost saving)
  - ElevenLabs: multilingual, $0.0001/char
  - Kokoro (self-hosted): 96x real-time, zero COGS for voice
  - XTTS-v2 (self-hosted): supports Thai, Vietnamese
- Sync voiceover timing to scene timeline
- **If ai_generate mode:** Submit to Sora 2 API ($0.10/sec) or Veo 3.1 Fast ($0.15/sec)
- **If asset_compose mode:** Build with `python-ffmpeg` + `Movis`:
  - Assemble image scenes with Ken Burns zoom/pan
  - Add word-by-word caption overlay (synced to voiceover timestamps)
  - Mix background music (royalty-free, -20dB under voiceover)
  - Add brand watermark (corner, configurable opacity)
  - Add end screen: CTA card with follow/shop animation
- Export: 1080×1920px MP4, H.264, 30fps, 8Mbps, max 60s
- Log actual API cost to `videos.api_cost_usd`

**Libraries:**
```
python-ffmpeg, movis, elevenlabs, openai (TTS), pydub, asyncpg
```
*(Note: use `python-ffmpeg`, NOT the unmaintained `ffmpeg-python` package)*

---

### Job 5: Multi-Platform Publishing
**Purpose:** Auto-publish videos to TikTok, YouTube Shorts, Instagram Reels, Pinterest

**Schedule:** Every 2 hours (staggered by optimal posting time per platform and market)

**Inputs:**
- Completed videos (`status=ready`) from `videos` table
- Platform metadata: title, description, tags, thumbnail
- User posting schedule config

**Outputs:**
- `publications` table: `(id, video_id, user_id, platform, post_id, url, posted_at, status)`

**Tasks:**
- **TikTok:** `tiktok-api-client` (official OAuth 2.0) — video upload + caption + hashtags
- **YouTube Shorts:** `google-api-python-client` `videos.insert` (vertical = auto-Shorts)
- **Instagram Reels:** Instagram Graph API — requires Business account, video + caption
- **Pinterest:** Pinterest API v5 — Idea Pin (video + title + board)
- Stagger posts: 30–90 min apart across platforms (avoid spam detection)
- Respect platform best times per market timezone (TH=ICT, VN=ICT, ID=WIB)
- Save post URLs + platform IDs
- Alert via Slack/Telegram on successful post or failure

**Optimal Posting Times (Local Time):**
```
TikTok (Thailand/Vietnam): 19:00–22:00 (daily); 12:00–14:00 (Tue–Fri)
YouTube Shorts: 15:00–18:00 (Mon, Wed, Fri)
Instagram Reels: 11:00, 17:00, 20:00 (daily)
Pinterest: 20:00–23:00 (daily)
```

**Libraries:**
```
tiktok-api-client (PyPI), google-api-python-client, httpx (IG/Pinterest), slack-sdk, redis
```

---

### Job 6: Analytics & Performance Tracking
**Purpose:** Collect platform metrics and flag top/bottom performers

**Schedule:** Every 6 hours

**Inputs:**
- Published post IDs from `publications` table
- Platform analytics APIs

**Outputs:**
- `analytics` table: `(id, pub_id, user_id, platform, views, likes, comments, shares, watch_time_avg, engagement_rate, ctr, collected_at)`
- Daily performance email/Slack summary per user

**Tasks:**
- Fetch TikTok video analytics via TikTok Analytics API
- Fetch YouTube video stats via YouTube Analytics API
- Fetch Instagram Reels metrics via Instagram Graph API
- Calculate: `engagement_rate = (likes + comments + shares) / views`
- Flag top performers: `engagement_rate > platform_avg × 1.5`
- Flag underperformers: `< 200 views after 48h`
- Track ROI: `revenue_per_video = affiliate_clicks × avg_commission` (TikTok Shop users)
- Send daily digest: total views, total engagement, top video, worst video, total cost vs. revenue
- Viral alert (Slack/Telegram): `> 10,000 views` within 24h

**Libraries:**
```
httpx, google-api-python-client, pandas, asyncpg, slack-sdk
```

---

### Job 7: Content Optimization & Regeneration
**Purpose:** Auto-remake underperforming videos with improved hooks and pacing

**Schedule:** Daily at 02:00 (local market time)

**Inputs:**
- Underperformer flags from `analytics` table
- Top 10 performer patterns (hooks, captions, duration)
- User regeneration budget config

**Outputs:**
- New script variants in `scripts` table (`variant=remake`)
- Remake videos queued for Jobs 2→3→4→5

**Tasks:**
- Identify videos: `< 200 views after 48h` → flag for remake
- Analyze top 10 performers: extract common hook patterns, duration, caption style
- Generate improved hooks via Claude:
  ```
  Original hook "{hook}" underperformed ({views} views in 48h).
  Top performers use: question hooks, bold claims, curiosity gaps.
  Generate 3 improved hooks for topic "{topic}" targeting {market} audience.
  Return JSON: {{"hooks": ["h1", "h2", "h3"]}}
  ```
- A/B test: post remake on different platform than original
- Track remake vs. original performance
- Auto-archive if no remake improves within 72h

**Libraries:**
```
anthropic, asyncpg, pandas
```

---

### Job 8: Real-Time Trend Monitoring
**Purpose:** Detect emerging trends for 2–4 hour rapid response

**Schedule:** Every 30 minutes

**Inputs:**
- User-configured monitored hashtags and niches
- Platform trending feeds (TikTok, Google, News)

**Outputs:**
- `trending_alerts` table: `(id, user_id, topic, platform, velocity, detected_at, actioned)`
- Push notification for velocity > 200% rise/hour

**Tasks:**
- Poll Google Trends via `pytrends` for spike detection
- Poll Google News trending via `feedparser` (RSS)
- Poll TikTok trending hashtags (scraper/unofficial signal)
- Calculate: `velocity = (current_volume / 24h_ago_volume) - 1`
- Alert if velocity > 2.0 (200% rise) within 1 hour
- Auto-trigger Job 2 script generation for actionable high-velocity trends
- Distinguish: `viral_spike` (act now) vs. `evergreen_rising` (plan content)

**Libraries:**
```
pytrends, feedparser, httpx, redis, slack-sdk, asyncpg
```

---

### Job 9: TikTok Shop Product Automation (Key Differentiator)
**Purpose:** Auto-generate product review/promo videos from TikTok Shop affiliate links

**Schedule:** Triggered on product add OR daily batch for catalog items

**Inputs:**
- TikTok Shop product URL or affiliate product ID
- Target market/language: TH | VI | ID | EN
- Review style: `honest_review` | `unboxing` | `comparison` | `how_to_use`

**Outputs:**
- Product video in `/storage/{user_id}/{product_id}/final.mp4`
- Posted to TikTok with affiliate link in bio/caption
- `tiktok_shop_products` table: `(id, user_id, product_id, product_name, price, affiliate_url, video_id, clicks, conversions, commission_earned)`

**Tasks:**
- Scrape product data: title, price, description, images, ratings, review count
- Generate product review script via Claude (localized to TH/VI/ID)
- Fetch/generate scene visuals (product images + lifestyle B-roll)
- Render video with price badge overlay, affiliate CTA ("Shop link in bio!")
- Post to TikTok with affiliate link in caption or bio
- Track clicks/conversions via TikTok Shop Affiliate API
- Auto-regenerate high-converting products weekly with fresh angles

**Libraries:**
```
httpx (product scrape), anthropic, tiktok-api-client, asyncpg
```

---

## FastAPI REST Endpoints

**File:** `api/main.py`
**Auth:** Bearer token (API key per user)

```
POST /api/v1/video/generate              # Submit topic → full pipeline
POST /api/v1/video/generate-from-url     # Product URL → TikTok Shop video
GET  /api/v1/video/{id}/status           # Generation status
GET  /api/v1/video/{id}/download         # Download MP4
POST /api/v1/video/{id}/publish          # Manual publish trigger
GET  /api/v1/analytics/summary           # Dashboard stats
GET  /api/v1/analytics/roi               # Revenue vs. cost breakdown
GET  /api/v1/topics/trending             # Current trending topics
POST /api/v1/script/generate             # Script only (no video)
GET  /api/v1/jobs/status                 # Scheduler health check
GET  /api/v1/usage/cost                  # AI API cost tracker per user
POST /api/v1/brand/config                # Set brand voice, colors, logo
GET  /api/v1/shop/products               # TikTok Shop product catalog
```

---

## Database Schema (PostgreSQL)

```sql
-- Multi-tenant: every table has user_id
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    plan TEXT DEFAULT 'free',       -- free | starter | pro | enterprise
    stripe_customer_id TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE topics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    topic TEXT NOT NULL,
    platform TEXT,
    market TEXT DEFAULT 'TH',       -- TH | VI | ID | EN
    trend_score REAL,
    hashtags JSONB,
    source TEXT,
    status TEXT DEFAULT 'pending',  -- pending | scripted | archived
    discovered_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE scripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    topic_id UUID REFERENCES topics(id),
    hook TEXT, body TEXT, cta TEXT,
    caption TEXT, hashtags JSONB,
    voiceover_text TEXT,
    language TEXT DEFAULT 'th',
    duration_target INTEGER,        -- seconds
    variant TEXT DEFAULT 'a',       -- a | b | c | remake
    estimated_cost_usd NUMERIC(8,4),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    script_id UUID REFERENCES scripts(id),
    file_path TEXT,
    thumbnail_path TEXT,
    duration REAL,
    resolution TEXT DEFAULT '1080x1920',
    api_cost_usd NUMERIC(8,4),      -- actual Sora/Veo/ElevenLabs cost
    status TEXT DEFAULT 'rendering',-- rendering | ready | published | archived
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE publications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    video_id UUID REFERENCES videos(id),
    platform TEXT,                  -- tiktok | youtube | instagram | pinterest
    post_id TEXT,
    url TEXT,
    posted_at TIMESTAMP,
    status TEXT DEFAULT 'pending'   -- pending | posted | failed
);

CREATE TABLE analytics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pub_id UUID REFERENCES publications(id),
    user_id UUID REFERENCES users(id),
    platform TEXT,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    watch_time_avg REAL,
    engagement_rate REAL,
    ctr REAL,
    collected_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE tiktok_shop_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    product_id TEXT,
    product_name TEXT,
    price NUMERIC(10,2),
    affiliate_url TEXT,
    video_id UUID REFERENCES videos(id),
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    commission_earned NUMERIC(10,2) DEFAULT 0
);
```

---

## Project File Structure

```
autoGenVideo/
├── .env
├── .env.example
├── requirements.txt
├── config.py
├── main.py                           # CLI + orchestrator entry
├── scheduler.py                      # APScheduler async job registry
├── api/
│   ├── __init__.py
│   ├── main.py                       # FastAPI app
│   ├── routes/
│   │   ├── videos.py
│   │   ├── analytics.py
│   │   ├── topics.py
│   │   └── shop.py
│   └── auth.py                       # API key auth middleware
├── database/
│   ├── __init__.py
│   ├── models.py                     # SQLAlchemy ORM (async)
│   ├── migrations/                   # Alembic migrations
│   └── init_db.py
├── jobs/
│   ├── job1_trend_research.py
│   ├── job2_script_generation.py
│   ├── job3_media_assets.py
│   ├── job4_video_rendering.py
│   ├── job5_publishing.py
│   ├── job6_analytics.py
│   ├── job7_optimization.py
│   ├── job8_trend_monitoring.py
│   └── job9_tiktok_shop.py           # Key differentiator
├── utils/
│   ├── ai_utils.py                   # Claude API wrapper
│   ├── tts_utils.py                  # ElevenLabs + Kokoro/XTTS-v2 switcher
│   ├── video_utils.py                # python-ffmpeg + Movis rendering
│   ├── platform_api.py               # TikTok, YouTube, Instagram, Pinterest
│   ├── cost_tracker.py               # Per-user API cost logging
│   └── notify.py                     # Slack + Telegram alerts
├── assets/
│   ├── fonts/
│   ├── music/                        # Royalty-free background tracks
│   └── templates/                    # Brand overlays, end screens, price badges
├── storage/                          # User video/asset storage (→ S3 in prod)
├── reports/
├── logs/
└── tests/
```

---

## Business Model & Pricing Tiers

| Feature | Free | Starter ($19/mo) | Pro ($49/mo) | Agency ($99/mo) |
|---|---|---|---|---|
| Videos/month | 5 (watermarked) | 30 | 150 | Unlimited |
| Platforms | TikTok only | All 4 | All 4 | All 4 + custom |
| Languages/TTS | EN only | EN + TH | EN + TH + VI + ID | All |
| TikTok Shop auto-video | No | 10 products | 50 products | Unlimited |
| API access | No | No | 1,000 calls/mo | Unlimited |
| Analytics | Basic | Full | Full + AI insights | Full + white-label |
| A/B testing | No | No | Yes | Yes |
| Brand kit (logo, colors) | No | 1 brand | 3 brands | Unlimited |
| Support | Community | Email | Priority | SLA + CSM |

**COGS target per tier:**
- Free: $0.50/user/mo (5 × $0.10 Sora 2 clips)
- Starter $19/mo: $3.00 COGS → **84% GM** (use asset_compose mode, not Sora)
- Pro $49/mo: $8.00 COGS → **84% GM** (mix asset_compose + Sora selectively)
- Agency $99/mo: custom COGS → **70%+ GM** target

**Strategy:** Default to `asset_compose` mode (FFmpeg + images = near-zero COGS). Only use Sora 2 API for "hero" videos or when user explicitly requests AI-generated video. This preserves margins.

---

## 90-Day Milestone Plan

| Days | Focus | Goal |
|---|---|---|
| 1–7 | Scaffold: DB, config, FastAPI shell, auth | Infrastructure + API skeleton ready |
| 8–14 | Job 1 + 2: Trend research + Script generation (TH/EN) | Auto-scripts generating from trending topics |
| 15–21 | Job 3 + 4: Asset gen + Video rendering (asset_compose mode) | Videos rendering locally without Sora API |
| 22–28 | Job 5: TikTok + YouTube auto-publishing | First auto-posts live |
| 29–35 | Job 9: TikTok Shop product URL → video → post | Core differentiator live |
| 36–42 | Job 6 + 7: Analytics + optimization loop | Data-driven content remakes |
| 43–56 | Job 8: Real-time trend monitoring | 30-min viral response pipeline |
| 57–70 | Stripe billing integration, multi-tenant, usage limits | SaaS-ready: Free/Starter/Pro tiers |
| 71–90 | Sora 2 / Veo 3.1 AI video integration, white-label, scale | 50+ videos/day per Pro user |

---

## References & Data Sources

- [HeyGen Pricing 2026](https://aiblogfirst.com/heygen-pricing/)
- [Invideo AI Pricing](https://invideo.io/pricing/)
- [Runway Pricing](https://runwayml.com/pricing)
- [Pika Labs Pricing](https://pika.art/pricing)
- [Kling AI Pricing](https://aitoolanalysis.com/kling-ai-pricing/)
- [Google Veo 3.1 Pricing](https://developers.googleblog.com/veo-3-and-veo-3-fast-new-pricing-new-configurations-and-better-resolution)
- [OpenAI Sora 2 Pricing](https://costgoat.com/pricing/sora)
- [TikTok SEA Stats](https://newsroom.tiktok.com/tiktok-surpasses-460-million-users-in-southeast-asia-inks-partnership-with-vietnams-ministry-of-culture-sports-and-tourism)
- [TikTok Shop GMV 2025](https://resourcera.com/data/social/tiktok-shop-statistics/)
- [BCG SEA AI Report](https://web-assets.bcg.com/2d/5a/2b923a054e2b9423e61e77f442f7/unlocking-southeast-asias-ai-potential-vf-20250407.pdf)
- [SocialInsider Benchmarks 2026](https://www.socialinsider.io/social-media-benchmarks)
- [TikTok Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started)
- [BentoML Open Source TTS](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)
- [IMG.LY Python Video SDKs](https://img.ly/blog/best-open-source-video-editor-sdks-2025-roundup/)
- GenCNX competitive analysis: `business_gencnx.md`
