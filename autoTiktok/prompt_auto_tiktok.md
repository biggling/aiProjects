# Prompt: Design High-Level Python Automation for TikTok Growth & Monetization

## Context & Strategy Summary

Based on manual workflow in `ex_step.md` — a step-by-step TikTok affiliate marketing and content strategy.

**Business Model:**
- TikTok affiliate marketing (TikTok Shop + Amazon Associates)
- Short-form video content (15–60s) with embedded product promotions
- Revenue streams: affiliate commissions + brand sponsorships
- Target: $3,000+/month from 100k+ followers

**Current Manual Time:** 3–4 hours/day across 8 workflow areas
**Automation Goal:** Reduce to < 30 minutes/day (human review only)

---

## Prompt for Claude / AI Design Session

```
Design a high-level Python automation system for a TikTok growth and monetization
business that replicates the 8-area manual workflow from ex_step.md with minimal
human intervention.

Break the design into clearly separated automated job modules — one per workflow area.
Each job module should be independently schedulable (cron/APScheduler) and define:
- Purpose (which area it automates)
- Inputs / Outputs
- Key Python libraries and APIs
- Data flow to other modules
- Scheduling cadence
- Human review checkpoint (if any)

Target: 2–3 videos/day per account, multiple niche accounts supported
Platform: TikTok (primary) + cross-post to Instagram Reels, YouTube Shorts
Affiliate networks: TikTok Shop, Amazon Associates, ShareASale

Constraints:
- Python 3.11+
- Use async where applicable
- Store state in SQLite
- Secrets managed via .env / python-dotenv
- Modular: each job can run standalone
- Human-in-the-loop: flag AI-generated content for optional review before posting
```

---

## High-Level System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                    AUTO TIKTOK PIPELINE                               │
│                                                                      │
│  [Job 1]          [Job 2]          [Job 3]          [Job 4]           │
│  Niche &          Content          Script &          Video            │
│  Product  ──────► Research  ──────► Creative  ──────► Production      │
│  Research          (Trends)        (AI-gen)          (Render+TTS)     │
│                                                                      │
│  [Job 5]          [Job 6]          [Job 7]          [Job 8]           │
│  Auto-Post        Engagement       Affiliate &       Analytics &      │
│  & Hashtags ──────► Bot     ──────► Monetize  ──────► Optimize        │
└──────────────────────────────────────────────────────────────────────┘
                         │
                  [Human Review Queue]
              Optional approval before posting
```

---

## Automated Job Modules (8 Areas from ex_step.md)

---

### Job 1: Niche & Product Research
**Automates:** Area 1 (Niche Setup) + Area 7 (Affiliate research)
**Purpose:** Discover profitable niche-product combinations with high affiliate potential

**Schedule:** Daily at 06:00 UTC

**Inputs:**
- Seed niches: beauty, fitness, gadgets, food, pets, tech
- Affiliate API credentials (TikTok Shop, Amazon)

**Outputs:**
- `niches.db`: `(niche, product_name, product_url, commission_pct, affiliate_link, trend_score)`
- Top 5 niche-product pairs ranked by (trend × commission)

**Tasks:**
- Fetch TikTok Shop trending products via TikTok Shop API or scraper
- Fetch Amazon bestsellers in niche categories via Amazon Product Advertising API
- Check ShareASale / ClickBank for high-commission niche products
- Score: `(search_volume × commission_rate) / competition`
- Update `niches.db` with top products for each niche
- Alert via Slack if new high-commission product detected

**Libraries:**
```
requests, beautifulsoup4, amazon-paapi, sqlite3, slack-sdk
```

---

### Job 2: Content & Trend Research
**Automates:** Area 2 (Content Research)
**Purpose:** Identify top-performing competitor videos, trending sounds, and hashtags

**Schedule:** Every 4 hours

**Inputs:**
- Active niches from `niches.db`
- TikTok competitor account list (manual seed)

**Outputs:**
- `trends.db`: `(niche, trending_sound_id, sound_name, hashtags, hook_pattern, top_video_url, views)`
- Competitor analysis notes per niche

**Tasks:**
- Scrape TikTok search results for niche keywords (top 10 by views this week)
- Extract: hook text (first 3s caption), video duration, hashtags used, sound ID
- Identify trending sounds: sounds used in top 3 videos per niche
- Analyze hook patterns: question | bold claim | story | reaction | tutorial
- Save trending data to `trends.db`
- Flag hooks with > 100k views as "proven patterns"

**Libraries:**
```
selenium/playwright (TikTok scraper), beautifulsoup4, pandas, sqlite3
```

---

### Job 3: Script & Creative Generation
**Automates:** Area 3 (Script & Content Creation)
**Purpose:** Generate AI-powered video scripts, captions, and creative briefs for each product

**Schedule:** Every 6 hours (after Job 2)

**Inputs:**
- Top products from `niches.db`
- Proven hook patterns from `trends.db`
- Product details (name, features, price, affiliate link)

**Outputs:**
- `scripts.db`: `(script_id, product_id, hook, body, cta, voiceover, caption, hashtags, sound_id)`
- Script JSON files: `/scripts/{product_slug}/script.json`

**Tasks:**
- For each product, generate:
  - Hook using top-performing hook pattern for niche
  - Body script (product demo in 3 scenes)
  - CTA text ("Comment LINK for access" or "Link in bio")
  - Caption (max 2200 chars, 3–5 hashtags: 1 broad + 2 niche + 1 trending)
  - Voiceover script (conversational, 2nd person, ~75 words for 30s)
- Assign trending sound from `trends.db` to each script
- Generate 3 thumbnail text variations for A/B testing
- Queue for human review OR auto-approve if confidence score > 0.85

**Claude API prompt template:**
```
You are a viral TikTok content creator for {niche}. Generate a {duration}s video script
promoting {product_name} (affiliate) using the "{hook_pattern}" hook style.

Format:
- HOOK: 0–3s (max 12 words, {hook_pattern} style)
- BODY: 3 scenes showing product value (10s each)
- CTA: "Comment {keyword} for the link"
- CAPTION: 150 chars + 5 hashtags
- VOICEOVER: Natural, conversational, 75 words
Return JSON only.
```

**Libraries:**
```
anthropic (claude-sonnet-4-6), sqlite3, json
```

---

### Job 4: Video Production
**Automates:** Area 4 (Video Production)
**Purpose:** Auto-produce TikTok-ready MP4 from script + assets

**Schedule:** Triggered by Job 3 (or every 6 hours)

**Inputs:**
- Scripts from `scripts.db`
- Product images/videos from affiliate product URLs
- Brand templates: intro.mp4, outro.png, font kit
- Trending sound audio file (downloaded)

**Outputs:**
- Final MP4: `/videos/{script_id}/final.mp4` (1080×1920, 30fps, 30–60s)
- Thumbnail: `/videos/{script_id}/thumbnail.jpg`
- `videos.db`: `(video_id, script_id, file_path, duration, status, created_at)`

**Tasks:**
- Download product images from URLs (3–5 per video)
- Generate AI scene images via DALL-E 3 if product images unavailable
- Generate TTS voiceover (ElevenLabs → OpenAI TTS → gTTS fallback)
- Assemble video: scenes + voiceover + transitions (MoviePy)
- Add hook text overlay (large bold, bottom-third position)
- Add on-screen captions (word-by-word sync with voiceover, TikTok caption style)
- Add CTA text overlay (last 5 seconds)
- Mix trending sound at 20% volume under voiceover
- Add brand watermark (logo, 30% opacity, top-right)
- Export: 1080×1920px, H.264, 30fps, max 30MB

**Libraries:**
```
moviepy, Pillow, ffmpeg-python, openai (TTS), elevenlabs, pydub, requests
```

---

### Job 5: Auto-Post & Hashtags
**Automates:** Area 5 (Posting & Hashtags)
**Purpose:** Schedule and auto-publish videos at optimal times with keyword-rich metadata

**Schedule:** 3× daily at optimal times (07:00, 13:00, 19:00 UTC)

**Inputs:**
- Ready videos from `videos.db`
- Approved scripts with captions + hashtags from `scripts.db`
- Account config: TikTok account credentials + niche

**Outputs:**
- `posts.db`: `(post_id, video_id, platform, tiktok_video_id, url, posted_at, status)`

**Tasks:**
- Select next video from queue (ordered by product priority score)
- Upload to TikTok via Content Posting API v2
- Set caption: hook headline + 3–5 hashtags (niche-specific)
- Attach TikTok Shop product link sticker (if product in TikTok Shop)
- Set cover frame: highest-energy frame (first 0.5s or detected via thumbnail)
- Enable: duet ON, stitch ON, comment ON (maximize engagement signals)
- Cross-post to Instagram Reels + YouTube Shorts (if enabled)
- Record post URL + video ID in `posts.db`
- Notify via Slack

**Optimal Posting Times by Niche:**
```
Beauty/Fashion: 12:00, 20:00 UTC
Tech/Gadgets: 14:00, 21:00 UTC
Food/Recipes: 11:00, 17:00 UTC
Fitness: 06:00, 12:00, 18:00 UTC
```

**Libraries:**
```
requests (TikTok Content API), instagrapi, google-api-python-client, slack-sdk
```

---

### Job 6: Engagement Bot
**Automates:** Area 6 (Engagement & Growth)
**Purpose:** Boost algorithm signals in the first 30 minutes after posting

**Schedule:** Triggered 5 minutes after each post + every 2 hours for follow activity

**Inputs:**
- New posts from `posts.db`
- Competitor account list (for stitch/follow targets)
- Comment reply templates per niche

**Outputs:**
- `engagement_log.db`: `(action, target, platform, performed_at, result)`

**Tasks:**
- Reply to incoming comments on our videos within 30 minutes (AI-generated replies)
- Like + comment on 10 trending videos per niche (appear in trending comment sections)
- Follow 20 targeted accounts per day (niche followers, not competitors)
- Stitch/duet top competitor video once per week (reaction video content)
- Pin best-performing video to profile (if better than current pin)
- Track follow/unfollow ratio (unfollow non-followers after 3 days)

**Comment Reply Generation (Claude API):**
```
Given comment: "{comment_text}" on video about {product/niche},
generate a warm, authentic reply that:
1. Answers questions directly
2. Encourages more engagement
3. Subtly promotes the product if relevant
Max 150 chars. No promotional spam tone.
```

**⚠️ Rate limit:** Max 50 actions/hour to avoid TikTok shadowban.

**Libraries:**
```
anthropic, playwright/selenium (TikTok engagement), sqlite3, schedule
```

---

### Job 7: Affiliate & Monetization Tracker
**Automates:** Area 7 (Affiliate & Monetization)
**Purpose:** Track affiliate clicks, commissions, and identify top-converting products

**Schedule:** Every 6 hours

**Inputs:**
- TikTok analytics (link clicks from posts)
- Amazon Associates API (clicks + commissions)
- TikTok Shop dashboard (sales data)

**Outputs:**
- `affiliate.db`: `(product, platform, clicks, conversions, commission, revenue, period)`
- Weekly affiliate performance report

**Tasks:**
- Poll Amazon Associates API for clicks + earnings by product
- Poll TikTok Shop for order completions linked to our videos
- Calculate conversion rate per product: conversions / link_clicks
- Identify top converters: conversion_rate > 2% AND commission > $10
- Flag high performers for Job 3 (generate more content for this product)
- Flag low performers (< 5 clicks after 3 posts) for replacement
- Send weekly earnings report via Slack

**Libraries:**
```
requests, amazon-paapi, sqlite3, pandas, slack-sdk
```

---

### Job 8: Analytics & Optimization
**Automates:** Area 8 (Analytics & Optimization)
**Purpose:** Track KPIs, identify winners/losers, and drive content strategy via data

**Schedule:** Daily at 23:00 UTC

**Inputs:**
- `posts.db` (post history)
- TikTok Analytics API (views, retention, follows)
- `affiliate.db` (revenue per video)

**Outputs:**
- `analytics.db`: `(video_id, views_24h, views_7d, likes, comments, shares, follows_gained, revenue)`
- Daily optimization report: `reports/YYYY-MM-DD.md`
- Action queue: videos to replicate, hooks to A/B test

**Tasks:**
- Fetch video stats from TikTok Analytics API for all posts in last 30 days
- Identify "winners": views_24h > 1,000 AND engagement_rate > 5%
- Identify "losers": views_48h < 200
- Generate replication plan for winners (Job 3 receives: "make 3 more like video X")
- Generate retry plan for losers (Job 3 receives: "remake with different hook")
- A/B test tracker: compare video pairs with same topic, different hooks
- Update `niches.db` scores based on performance data
- Generate markdown report + Slack summary

**Libraries:**
```
requests (TikTok Analytics API), pandas, matplotlib, sqlite3, slack-sdk, jinja2
```

---

## Data Store Schema (SQLite)

```sql
-- niches.db (products × niches)
CREATE TABLE niches (
    id INTEGER PRIMARY KEY,
    niche TEXT,
    product_name TEXT,
    product_url TEXT,
    affiliate_link TEXT,
    commission_pct REAL,
    trend_score REAL,
    performance_score REAL DEFAULT 0,
    status TEXT DEFAULT 'active',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- trends.db (competitor analysis)
CREATE TABLE trends (
    id INTEGER PRIMARY KEY,
    niche TEXT,
    hook_pattern TEXT,
    trending_sound_id TEXT,
    sound_name TEXT,
    hashtags TEXT,
    top_video_url TEXT,
    views INTEGER,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- scripts.db (AI-generated video scripts)
CREATE TABLE scripts (
    id INTEGER PRIMARY KEY,
    product_id INTEGER REFERENCES niches(id),
    hook TEXT,
    body TEXT,  -- JSON scenes array
    cta TEXT,
    voiceover_text TEXT,
    caption TEXT,
    hashtags TEXT,
    sound_id TEXT,
    status TEXT DEFAULT 'pending',  -- pending | approved | rejected | posted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- videos.db (rendered MP4s)
CREATE TABLE videos (
    id INTEGER PRIMARY KEY,
    script_id INTEGER REFERENCES scripts(id),
    file_path TEXT,
    thumbnail_path TEXT,
    duration REAL,
    status TEXT DEFAULT 'ready',  -- ready | posted | archived
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- posts.db (published posts)
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    video_id INTEGER REFERENCES videos(id),
    platform TEXT,
    tiktok_video_id TEXT,
    url TEXT,
    caption TEXT,
    hashtags TEXT,
    posted_at TIMESTAMP,
    status TEXT DEFAULT 'posted'
);

-- analytics.db (performance metrics)
CREATE TABLE analytics (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    views_24h INTEGER DEFAULT 0,
    views_7d INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    follows_gained INTEGER DEFAULT 0,
    link_clicks INTEGER DEFAULT 0,
    engagement_rate REAL DEFAULT 0,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- affiliate.db (commission tracking)
CREATE TABLE affiliate (
    id INTEGER PRIMARY KEY,
    post_id INTEGER REFERENCES posts(id),
    product_name TEXT,
    platform TEXT,  -- amazon | tiktok_shop | shareasale
    clicks INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    commission REAL DEFAULT 0,
    period TEXT,  -- YYYY-MM-DD
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Project File Structure

```
autoTiktok/
├── .env
├── .env.example
├── requirements.txt
├── config.py
├── main.py                         # CLI
├── scheduler.py                    # APScheduler
├── database/
│   ├── models.py
│   └── init_db.py
├── jobs/
│   ├── job1_niche_research.py
│   ├── job2_content_research.py
│   ├── job3_script_generation.py
│   ├── job4_video_production.py
│   ├── job5_auto_post.py
│   ├── job6_engagement_bot.py
│   ├── job7_affiliate_tracker.py
│   └── job8_analytics.py
├── utils/
│   ├── ai_utils.py
│   ├── tts_utils.py
│   ├── video_utils.py
│   ├── tiktok_api.py
│   ├── affiliate_api.py
│   └── notify.py
├── review_queue/                   # Videos awaiting human approval
├── scripts/                        # Generated script JSON files
├── videos/                         # Rendered MP4s
├── reports/                        # Daily analytics reports
├── logs/
└── tests/
```

---

## Tech Stack Summary

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| Scheduling | APScheduler |
| AI - Script | Anthropic Claude API (claude-sonnet-4-6) |
| AI - Image | OpenAI DALL-E 3 |
| AI - TTS | ElevenLabs / OpenAI TTS |
| Video | MoviePy + FFmpeg |
| Image | Pillow |
| Browser automation | Playwright (TikTok engagement) |
| TikTok API | Content Posting API v2, Analytics API |
| Instagram | Graph API / instagrapi |
| YouTube | Data API v3 |
| Affiliate | Amazon PAAPI, TikTok Shop API |
| Database | SQLite (dev) → PostgreSQL (prod) |
| Notifications | slack-sdk |
| Config | python-dotenv |

---

## 90-Day Revenue Projection

| Days | Videos Posted | Followers | Daily Revenue | Monthly Revenue |
|---|---|---|---|---|
| 1–10 | 20–30 | 0–500 | $0 | $0 |
| 11–30 | 60–90 | 500–3,000 | $5–20 | $50–400 |
| 31–60 | 60–90/mo | 3k–15k | $20–80 | $600–2,400 |
| 61–90 | 90/mo | 15k–60k | $80–200 | $2,400–6,000 |
