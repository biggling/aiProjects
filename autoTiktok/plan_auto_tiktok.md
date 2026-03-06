# Build Plan: autoTiktok — TikTok Growth & Monetization Automation

**Goal:** $3,000+/month from TikTok affiliate commissions + sponsored posts
**Strategy Reference:** `ex_step.md` (8-area manual workflow)
**Prompt Reference:** `prompt_auto_tiktok.md`
**Status:** Planning Phase

---

## Phase Overview

| Phase | Days | Focus | Milestone |
|---|---|---|---|
| Phase 1 | 1–5 | Foundation: scaffold, DB, config | Infra ready |
| Phase 2 | 6–10 | Jobs 1–2: Niche + Trend Research | Data flowing |
| Phase 3 | 11–16 | Jobs 3–4: Script + Video Production | Videos rendering |
| Phase 4 | 17–21 | Job 5: Auto-posting | First auto-posts live |
| Phase 5 | 22–28 | Job 6: Engagement Bot | Engagement automated |
| Phase 6 | 29–35 | Job 7: Affiliate Tracker | Revenue tracked |
| Phase 7 | 36–42 | Job 8: Analytics & Optimization | Feedback loop |
| Phase 8 | 43–90 | Scale: multi-account, niche expansion | $3k/month target |

---

## Phase 1: Foundation (Days 1–5)

### 1.1 Project Structure

```
autoTiktok/
├── .env
├── .env.example
├── requirements.txt
├── config.py                       # Env loading, constants
├── main.py                         # CLI
├── scheduler.py                    # APScheduler job registry
├── database/
│   ├── models.py                   # SQLAlchemy ORM (6 tables)
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
├── review_queue/
├── scripts/, videos/, reports/, logs/
└── tests/
```

### 1.2 Required API Keys

```
# AI
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
ELEVENLABS_API_KEY=

# TikTok
TIKTOK_CLIENT_KEY=
TIKTOK_CLIENT_SECRET=
TIKTOK_ACCESS_TOKEN=

# Instagram
INSTAGRAM_ACCESS_TOKEN=
INSTAGRAM_BUSINESS_ACCOUNT_ID=

# YouTube
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=

# Affiliate
AMAZON_ACCESS_KEY=
AMAZON_SECRET_KEY=
AMAZON_PARTNER_TAG=
TIKTOK_SHOP_APP_KEY=
TIKTOK_SHOP_APP_SECRET=
TIKTOK_SHOP_ACCESS_TOKEN=

# Content
PEXELS_API_KEY=
PIXABAY_API_KEY=

# Notifications
SLACK_WEBHOOK_URL=
```

### 1.3 Database Tables (6 total)

| Table | Purpose |
|---|---|
| `niches` | Products + niches + affiliate links |
| `trends` | Competitor analysis + trending sounds |
| `scripts` | AI-generated video scripts |
| `videos` | Rendered MP4 files |
| `posts` | TikTok/Instagram/YouTube post records |
| `analytics` | Performance metrics |
| `affiliate` | Commission tracking per post |

### 1.4 Dependencies

```
# AI
anthropic>=0.25.0, openai>=1.30.0, elevenlabs>=1.0.0

# Video
moviepy>=1.0.3, Pillow>=10.3.0, ffmpeg-python>=0.2.0, pydub>=0.25.1, gTTS>=2.5.1

# Automation
playwright>=1.44.0, selenium>=4.20.0, apscheduler>=3.10.4

# Data
requests>=2.31.0, beautifulsoup4>=4.12.3, pandas>=2.2.2, sqlite3 (stdlib)

# Platform
instagrapi>=2.0.0, google-api-python-client>=2.130.0, slack-sdk>=3.27.2
python-dotenv>=1.0.1, tenacity>=8.3.0
```

**System requirement:** `ffmpeg` (`apt install ffmpeg`) + `playwright install chromium`

---

## Phase 2: Jobs 1–2 — Research (Days 6–10)

### 2.1 Job 1: Niche & Product Research

**File:** `jobs/job1_niche_research.py`
**Schedule:** Daily 06:00 UTC

**Product scoring formula:**
```
score = (search_volume × commission_rate) / competition_count
```

**Product sources (priority):**
1. TikTok Shop trending (best affiliate rates + native integration)
2. Amazon bestsellers (via Amazon PAAPI)
3. ShareASale high-commission products

**Output to `niches` table:**
- product_name, affiliate_link, commission_pct, trend_score

**Rate limits:**
- Amazon PAAPI: 1 request/second
- TikTok Shop API: Follows standard REST limits (check partner docs)

### 2.2 Job 2: Content & Trend Research

**File:** `jobs/job2_content_research.py`
**Schedule:** Every 4 hours

**Scraping approach for TikTok:**
- Use Playwright (headless Chromium) to browse TikTok search results
- Search: `{niche} + "tiktok" + "#ad"` or just niche keywords
- Extract: title card text (hook), duration, hashtags, view count
- No login required for public content

**Output to `trends` table:**
- hook_pattern classification: question | bold_claim | tutorial | reaction | curiosity_gap
- trending_sound_id (from video source attribute)
- hashtags extracted from caption

**Hook classification (Claude API):**
```
Classify this TikTok hook into one of: question, bold_claim, tutorial,
reaction, curiosity_gap. Hook: "{hook_text}"
Return: {"pattern": "...", "confidence": 0.0–1.0}
```

---

## Phase 3: Jobs 3–4 — Script + Video (Days 11–16)

### 3.1 Job 3: Script Generation

**File:** `jobs/job3_script_generation.py`
**Schedule:** Every 6 hours

**Script workflow:**
1. Query top 3 products per niche (by score)
2. Get matching hook pattern from `trends.db`
3. Call Claude API → generate JSON script
4. Validate: hook ≤ 12 words, voiceover ~75 words/30s
5. Set `status = 'pending'` → place in review queue (optional)
6. Auto-approve if confidence_score > 0.85

**Human review queue:**
- Save to `review_queue/YYYY-MM-DD/{script_id}.json`
- Slack notification: "N scripts await review at /review_queue/"
- After 2 hours with no human action → auto-approve

### 3.2 Job 4: Video Production

**File:** `jobs/job4_video_production.py`
**Schedule:** Triggered by Job 3 (or every 6 hours)

**Asset acquisition waterfall:**
1. Product image from affiliate product URL (requests + BeautifulSoup)
2. Pexels API (royalty-free stock)
3. Pixabay API (royalty-free alternative)
4. DALL-E 3 fallback (only if all others fail — most expensive)

**Video spec:**
- Resolution: 1080×1920 (9:16 portrait)
- FPS: 30
- Duration: 15–30s (optimal TikTok retention)
- Max file size: 287MB (TikTok limit, target <30MB)
- Format: MP4, H.264

**Scene structure:**
```
0–3s:  Hook text overlay + scene image
3–10s: Scene 1 (product intro)
10–20s: Scene 2 (product demo/benefit)
20–27s: Scene 3 (social proof or before/after)
27–30s: CTA overlay ("Comment LINK for the link")
```

**Trending sound integration:**
- Download trending audio snippet (15s) from TikTok CDN URL (if available)
- Mix at 20% volume under voiceover
- Fall back to `assets/music/` royalty-free collection

---

## Phase 4: Job 5 — Auto-Post (Days 17–21)

### 4.1 Job 5: Auto-Post & Hashtags

**File:** `jobs/job5_auto_post.py`
**Schedule:** 3× daily at 07:00, 13:00, 19:00 UTC

**Platform priority:**
1. TikTok (primary — Content Posting API v2)
2. Instagram Reels (same video, Graph API)
3. YouTube Shorts (Google Data API v3)

**TikTok post flow:**
1. Read video from `videos` table (status=ready)
2. Read script for caption + hashtags + CTA
3. TikTok Content Posting API: Init upload → Upload file → Confirm
4. Set cover frame: auto-detect high-contrast frame (Pillow analysis)
5. Enable duet + stitch (algorithm boost)
6. Record in `posts` table

**Hashtag strategy per post:**
```
#niche_broad (1×) + #niche_specific (2×) + #trending_this_week (1×) + #fyp (1×)
```
Total: 5 hashtags max (TikTok algorithm rewards quality over quantity)

**Rate limit compliance:**
- Max 3 posts/day per TikTok account
- 30-minute gap between posts on same account
- Never post same video twice on same platform

---

## Phase 5: Job 6 — Engagement Bot (Days 22–28)

### 5.1 Job 6: Engagement Bot

**File:** `jobs/job6_engagement_bot.py`
**Schedule:** Every 30 minutes (check for new comments) + 2× daily (follow activity)

**Comment reply workflow:**
1. Poll TikTok API for new comments on our videos (last 30 min)
2. For each unanswered comment, generate reply via Claude API
3. Post reply via TikTok API

**Follow strategy:**
- Follow 20 accounts/day from niche hashtag followers
- Unfollow accounts not following back after 3 days (track in DB)
- Never follow competitors directly (scrape their followers instead)

**⚠️ Anti-shadowban rules:**
- Max 50 total actions/hour (likes + comments + follows combined)
- Add random delay: 30–120 seconds between actions
- Skip if account has active shadowban detection (sudden view drop > 80%)

**Stitch/Duet automation:**
- Weekly: identify top trending video in niche
- Generate "reaction" script (Job 3 receives flag)
- Auto-produce reaction video (Job 4)
- Post as Stitch (boosts organic reach by appearing alongside trending content)

---

## Phase 6: Job 7 — Affiliate Tracker (Days 29–35)

### 6.1 Job 7: Affiliate & Monetization Tracker

**File:** `jobs/job7_affiliate_tracker.py`
**Schedule:** Every 6 hours

**Data collection:**
- Amazon Associates: use PAAPI earnings report endpoint
- TikTok Shop: poll TikTok Shop Partner API for order completions
- Manual input fallback: CSV import from affiliate dashboards

**Optimization triggers:**
- If product conversion_rate > 3% → flag for Job 3 (create 3 more videos)
- If product has < 5 clicks after 3 posts → replace with different product
- If commission > $50 in one day → Slack alert + immediate replication

---

## Phase 7: Job 8 — Analytics & Optimization (Days 36–42)

### 7.1 Job 8: Analytics

**File:** `jobs/job8_analytics.py`
**Schedule:** Daily 23:00 UTC

**Winner/Loser criteria:**
- Winner: views_24h > 1,000 OR follows_gained > 50 in 24h
- Loser: views_48h < 200

**Action queue output format:**
```json
{
  "replicate": ["video_id_1", "video_id_2"],
  "remake": [{"video_id": "...", "reason": "low views", "new_hook_suggestion": "..."}],
  "retire": ["video_id_3"]
}
```

Job 3 reads this queue at next run.

---

## Phase 8: Scheduler & Orchestration

**Job registry:**
| Job | Trigger | Frequency |
|---|---|---|
| job1_niche_research | cron | Daily 06:00 UTC |
| job2_content_research | interval | Every 4 hours |
| job3_script_generation | interval | Every 6 hours |
| job4_video_production | interval | Every 6 hours |
| job5_auto_post | cron | 07:00, 13:00, 19:00 UTC |
| job6_engagement_bot | interval | Every 30 min + 2× daily |
| job7_affiliate_tracker | interval | Every 6 hours |
| job8_analytics | cron | Daily 23:00 UTC |

---

## Human Review Checkpoint

```
scripts/review_queue/ ← Job 3 places new scripts here
       ↓
Human reviews (optional, 2h window)
       ↓
If approved → moves to Job 4 queue
If rejected → Job 3 regenerates with different parameters
If no action after 2h → auto-approved
```

**Slack notification format:**
```
🎬 3 new scripts ready for review
Topic: "5 Best Kitchen Gadgets Under $20"
Hook: "You're overpaying for this kitchen tool..."
[Approve] [Reject] — auto-approves in 2h
```

---

## Risk & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| TikTok shadowban | Views drop to 0 | Max 50 actions/hr, random delays |
| TikTok API rate limit | Post failures | Exponential backoff, queue retry |
| Account ban | Total revenue loss | Multiple accounts, manual fallback |
| DALL-E cost overrun | Budget spike | Pexels/product images first |
| Affiliate link rejection | No commissions | Rotate affiliate networks |
| TTS quality issues | Low viewer retention | ElevenLabs preferred for quality |

---

## Build Order

1. Phase 1: Scaffold + DB + Config
2. Job 1: Niche/Product Research (Amazon PAAPI + TikTok Shop)
3. Job 2: Trend Research (Playwright TikTok scraper)
4. Job 3: Script Generation (Claude API)
5. Job 4: Video Production (MoviePy + TTS)
6. Job 5: Auto-Post (TikTok Content API — test with 1 video first)
7. Job 7: Affiliate Tracker (read-only, safe to add early)
8. Job 6: Engagement Bot (add AFTER accounts are live and stable)
9. Job 8: Analytics (wire last, needs 1 week of data)
10. Scheduler: Wire all jobs + CLI

---

## Status Log

| Date | Phase | Status | Notes |
|---|---|---|---|
| 2026-03-06 | Planning | Complete | Plan document created |
| 2026-03-06 | Phase 1: Scaffold | Complete | config.py, requirements.txt, .env.example, dirs |
| 2026-03-06 | Phase 1: DB Models | Complete | models.py (6 tables: niches, trends, scripts, videos, posts, analytics, affiliate) |
| 2026-03-06 | Phase 1: Utils | Complete | ai_utils, tts_utils, tiktok_api, affiliate_api, notify |
| 2026-03-06 | Job 1: Niche Research | Complete | Amazon PAAPI + TikTok Shop trending |
| 2026-03-06 | Job 2: Trend Research | Complete | Playwright TikTok scraper + hook classification |
| 2026-03-06 | Job 3: Scripts | Complete | Claude API + review queue + auto-approve |
| 2026-03-06 | Job 4: Video Production | Complete | MoviePy + TTS + Pexels/DALL-E assets |
| 2026-03-06 | Job 5: Auto-Post | Complete | TikTok Content API v2 |
| 2026-03-06 | Job 6: Engagement Bot | Complete | Comment polling + AI replies (rate-limited) |
| 2026-03-06 | Job 7: Affiliate Tracker | Complete | Amazon/TikTok Shop earnings sync |
| 2026-03-06 | Job 8: Analytics | Complete | TikTok stats + winner/loser detection + action queue |
| 2026-03-06 | Scheduler | Complete | APScheduler + main.py CLI |
| 2026-03-06 | Tests | Complete | test_job1.py (score_product + mocked API runs), test_models.py (all 6 tables + relationships) |
| 2026-03-06 | CLAUDE.md | Complete | Session context file for future Claude sessions |

## Next Steps for Production
1. `python main.py --init-db`
2. `.env.example` → `.env`, fill API keys
3. `pip install -r requirements.txt` + `playwright install chromium` + `apt install ffmpeg`
4. Test: `python main.py --job 1` → `--job 2` → `--job 3` → `--job 4`
5. First manual post: `python main.py --job 5` (verify TikTok API works)
6. Start: `python main.py --scheduler`
