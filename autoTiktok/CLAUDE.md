# autoTiktok — Claude Session Context

## Project Goal
Automate TikTok affiliate revenue: $3,000+/month from TikTok Shop commissions + sponsored content.

## Build Status (2026-03-06) — ALL COMPLETE

| Component | File | Status |
|---|---|---|
| Config & Env | `config.py`, `.env.example`, `requirements.txt` | Complete |
| DB Models | `database/models.py` (6 tables) | Complete |
| DB Init | `database/init_db.py` | Complete |
| Job 1: Niche Research | `jobs/job1_niche_research.py` | Complete |
| Job 2: Trend Research | `jobs/job2_content_research.py` | Complete |
| Job 3: Script Gen | `jobs/job3_script_generation.py` | Complete |
| Job 4: Video Production | `jobs/job4_video_production.py` | Complete |
| Job 5: Auto-Post | `jobs/job5_auto_post.py` | Complete |
| Job 6: Engagement Bot | `jobs/job6_engagement_bot.py` | Complete |
| Job 7: Affiliate Tracker | `jobs/job7_affiliate_tracker.py` | Complete |
| Job 8: Analytics | `jobs/job8_analytics.py` | Complete |
| Scheduler | `scheduler.py` | Complete |
| CLI Entry | `main.py` | Complete |
| Utils | `utils/` (5 modules) | Complete |
| Tests | `tests/test_job1.py`, `tests/test_models.py` | Complete |

## Key Architecture
- **DB:** SQLite (dev) via SQLAlchemy — 6 tables: `niches`, `trends`, `scripts`, `videos`, `posts`, `analytics`, `affiliate`
- **AI:** Claude `claude-sonnet-4-6` for script generation + hook classification
- **TTS:** ElevenLabs (primary) → gTTS (fallback)
- **Video:** MoviePy + ffmpeg (1080×1920, 30fps, H.264, ≤30MB)
- **Posting:** TikTok Content API v2 (official)
- **Scheduler:** APScheduler with cron + interval triggers

## Job Schedule
| Job | Trigger |
|---|---|
| Job 1 (Niche Research) | Daily 06:00 UTC |
| Job 2 (Trend Research) | Every 4 hours |
| Job 3 (Script Gen) | Every 6 hours |
| Job 4 (Video Prod) | Every 6 hours |
| Job 5 (Auto-Post) | 07:00, 13:00, 19:00 UTC |
| Job 6 (Engagement Bot) | Every 30 min + 2× daily |
| Job 7 (Affiliate) | Every 6 hours |
| Job 8 (Analytics) | Daily 23:00 UTC |

## Setup for Production
```bash
python main.py --init-db
cp .env.example .env  # fill API keys
pip install -r requirements.txt
playwright install chromium
apt install ffmpeg
python main.py --job 1   # test Job 1
python main.py --scheduler  # start all jobs
```

## Required API Keys (.env)
- `ANTHROPIC_API_KEY` — script generation
- `ELEVENLABS_API_KEY` — TTS voiceover
- `TIKTOK_CLIENT_KEY` / `TIKTOK_CLIENT_SECRET` / `TIKTOK_ACCESS_TOKEN` — posting
- `TIKTOK_SHOP_APP_KEY` / `TIKTOK_SHOP_APP_SECRET` / `TIKTOK_SHOP_ACCESS_TOKEN` — affiliate
- `AMAZON_ACCESS_KEY` / `AMAZON_SECRET_KEY` / `AMAZON_PARTNER_TAG` — Amazon affiliate
- `PEXELS_API_KEY` / `PIXABAY_API_KEY` — stock media
- `OPENAI_API_KEY` — DALL-E fallback images
- `SLACK_WEBHOOK_URL` — notifications

## Anti-Shadowban Rules (CRITICAL)
- Max 50 actions/hour (likes + comments + follows)
- 30–120s random delay between actions
- Max 3 posts/day per TikTok account
- 30-minute gap between posts on same account

## Reference
- Build plan: `plan_auto_tiktok.md`
- Design prompt: `prompt_auto_tiktok.md`
- 8-step manual workflow: `ex_step.md`
