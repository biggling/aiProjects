# TikTok Automation — Dataflow Diagram

## End-to-End Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DAILY AUTOMATION PIPELINE                            │
│                          Asia/Bangkok Timezone                              │
└─────────────────────────────────────────────────────────────────────────────┘

06:00  ┌──────────────────────────────────────────────────────┐
       │  PHASE 1 — Research                                  │
       │                                                      │
       │  TikTok API ──► tiktok_trends.py ──► Trend table    │
       │  Shop API   ──► shop_products.py ──► Product table  │
       │  TikTok API ──► competitor.py                        │
       │                   └── GPT-4o (hook extract)          │
       │                        └──────────────► Hook table  │
       └──────────────────────────────────────────────────────┘
                                    │
                                    ▼  DB: Trend + Product + Hook rows
07:00  ┌──────────────────────────────────────────────────────┐
       │  PHASE 2 — Strategy                                  │
       │                                                      │
       │  DB (trends + products + hooks)                      │
       │    └── GPT-4o prompt ──► 5 ranked ideas JSON         │
       │         └──► ContentBrief table                      │
       │         └──► data/analytics/brief_YYYY-MM-DD.json    │
       └──────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┘
                    ▼  HUMAN CHECKPOINT (Mon 07:00, 20 min)
             ┌──────────────────┐
             │  Dashboard:      │
             │  Content Brief   │  ← Human toggles ideas on/off
             │  + Products page │  ← Human sets approved=true
             └──────────────────┘
                    │
                    ▼  ContentBrief.human_approved = true
07:30  ┌──────────────────────────────────────────────────────┐
       │  PHASE 3 — Script Generation                         │
       │                                                      │
       │  ContentBrief (approved ideas)                       │
       │    └── GPT-4o (per idea)                             │
       │         ├── hook + body + cta + caption + hashtags   │
       │         ├── Word count check (80-120 words)          │
       │         │    ├── Too long → GPT trim                 │
       │         │    └── Too short → GPT expand              │
       │         └──► Script table                            │
       │              └──► data/assets/scripts/script_{id}.json │
       └──────────────────────────────────────────────────────┘
                                    │
                                    ▼  DB: Script rows
08:00  ┌──────────────────────────────────────────────────────┐
       │  PHASE 4 — Voiceover                                 │
       │                                                      │
       │  Script (hook + body + cta text)                     │
       │    └── ElevenLabs TTS API                            │
       │         ├── stability=0.4, similarity=0.8            │
       │         ├── 3x retry with backoff                    │
       │         └──► data/assets/audio/voice_{id}.mp3        │
       │              └──► Voiceover table (+ duration_sec)   │
       └──────────────────────────────────────────────────────┘
                                    │
                                    ▼  MP3 files + duration
09:00  ┌──────────────────────────────────────────────────────┐
       │  PHASE 5 — Video Generation                          │
       │                                                      │
       │  Script.body                                         │
       │    └── GPT-4o → 15-word scene prompt                 │
       │         └── Kling AI API (primary)                   │
       │              ├── Submit job → poll every 5s           │
       │              ├── Download MP4 on complete            │
       │              └── Runway Gen-4 (fallback on failure)  │
       │                   └──► data/assets/clips/clip_{id}.mp4│
       │                        └──► VideoClip table          │
       └──────────────────────────────────────────────────────┘
                                    │
                                    ▼  MP4 clips
10:30  ┌──────────────────────────────────────────────────────┐
       │  PHASE 6 — Auto-Editor                               │
       │                                                      │
       │  voice_{id}.mp3 ──► Whisper STT                      │
       │                       └──► SRT → ASS captions        │
       │                                                      │
       │  clip_{id}.mp4 + voice_{id}.mp3 + captions_{id}.ass  │
       │    └── FFmpeg pipeline:                              │
       │         ├── Scale/pad → 1080x1920                    │
       │         ├── Concat clips to match audio duration      │
       │         ├── Mix audio (voice + -20dB bg music)        │
       │         ├── Burn ASS captions                         │
       │         ├── Fade-in 0.3s                             │
       │         └──► data/output/video_{id}.mp4              │
       │                                                      │
       │  video_{id}.mp4 @ 1.5s frame                        │
       │    └── Pillow (product name overlay)                 │
       │         └──► data/output/thumb_{id}.jpg              │
       │                                                      │
       │  Validates: < 60s duration, < 100MB                  │
       │  ──► EditedVideo table (status=pending_review)        │
       └──────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┘
                    ▼  HUMAN CHECKPOINT (daily 11:00, 15-20 min)
             ┌──────────────────┐
             │  Dashboard:      │
             │  QC Review page  │  ← Human watches each video
             │  (keyboard: a/r) │  ← Approve or Reject + reason
             └──────────────────┘
                    │
                    ▼  EditedVideo.status = "approved"
12:00  ┌──────────────────────────────────────────────────────┐
       │  PHASE 7 — Publisher (Slot 1)                        │
       │                                                      │
       │  EditedVideo (approved, unpublished)                 │
       │    ├── link_tagger.py → affiliate URL + UTM params   │
       │    ├── caption = script + hashtags + affiliate link  │
       │    │                                                 │
       │    └── TikTok Content API v2:                        │
       │         ├── Init upload                              │
       │         ├── Chunked upload (10MB chunks)             │
       │         └──► post_id                                 │
       │              └──► PublishedVideo table (tiktok)      │
       └──────────────────────────────────────────────────────┘
                                    │
15:30                               ▼  30 min after TikTok publish
       ┌──────────────────────────────────────────────────────┐
       │  PHASE 7 — Cross-post                                │
       │                                                      │
       │  PublishedVideo (tiktok, not cross-posted)            │
       │    ├── Instagram Graph API → Reel                    │
       │    │    └──► PublishedVideo table (instagram)        │
       │    └── YouTube Data API v3 → Short                   │
       │         └──► PublishedVideo table (youtube)          │
       └──────────────────────────────────────────────────────┘
                                    │
18:00                               ▼  (Slot 2 repeats same flow)
       ┌──────────────────────────────────────────────────────┐
       │  PHASE 7 — Publisher (Slot 2)                        │
       │  (same as 12:00, next approved video in queue)       │
       └──────────────────────────────────────────────────────┘
                                    │
21:00                               ▼
       ┌──────────────────────────────────────────────────────┐
       │  PHASE 8 — Analytics Pull                            │
       │                                                      │
       │  PublishedVideo (last 14 days)                       │
       │    └── TikTok Analytics API                          │
       │         ├── views, watch_time, likes, shares         │
       │         ├── CTR, GMV (from Shop affiliate API)       │
       │         └──► VideoMetric table                       │
       └──────────────────────────────────────────────────────┘

Fri    ┌──────────────────────────────────────────────────────┐
21:00  │  PHASE 8 — Scorer (Weekly)                           │
       │                                                      │
       │  VideoMetric (all recent)                            │
       │    └── Composite score:                              │
       │         (views×0.3) + (watch_time×0.3)               │
       │         + (ctr×0.2) + (gmv×0.2)                     │
       │    └── Top 20% → winner=True                        │
       │         └──► Remix ideas → ContentBrief (next Mon)  │
       └──────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┘
                    ▼  HUMAN CHECKPOINTS (Fri, ~30 min total)
             ┌──────────────────┐
             │  Dashboard:      │
             │  Analytics page  │  ← 15:00: Review weekly charts
             │  (winner panel)  │  ← 21:00: Approve remix winners
             └──────────────────┘
```

---

## Data Store Map

```
SQLite DB (data/db/app.db)
│
├── trends              ← Phase 1 output
├── products            ← Phase 1 output
├── competitor_hooks    ← Phase 1 output
├── content_briefs      ← Phase 2 output + human approval
├── scripts             ← Phase 3 output
├── voiceovers          ← Phase 4 output
├── video_clips         ← Phase 5 output
├── edited_videos       ← Phase 6 output + human QC status
├── published_videos    ← Phase 7 output (per platform)
└── video_metrics       ← Phase 8 output

File System
│
├── data/assets/
│   ├── scripts/        ← script_{id}.json         (Phase 3)
│   ├── audio/          ← voice_{id}.mp3            (Phase 4)
│   ├── clips/          ← kling_{id}.mp4            (Phase 5)
│   └── captions/       ← captions_{id}.ass         (Phase 6)
├── data/output/        ← video_{id}.mp4            (Phase 6)
│                          thumb_{id}.jpg           (Phase 6)
└── data/analytics/     ← brief_YYYY-MM-DD.json     (Phase 2)
                           weekly_report_YYYY-WW.json (Phase 8)

Config Files
├── config/settings.yaml   ← timing, limits, resolution
└── config/products.yaml   ← affiliate products (human-managed)
```

---

## API / WebSocket Event Flow

```
Browser (localhost:5173)
        │
        │  HTTP  GET/POST /api/*
        │◄──────────────────────► FastAPI (localhost:8000)
        │                                │
        │  WS    /ws                     ├── /api/videos/*   ──► EditedVideo DB
        │◄──────────────────────►        ├── /api/brief/*    ──► ContentBrief DB
        │                                ├── /api/analytics/* ─► VideoMetric DB
        │                                ├── /api/products/* ──► products.yaml
        │  WebSocket Events:             └── /api/schedule/* ──► APScheduler
        │  job_started
        │  job_done / job_failed
        │  video_ready
        │  video_approved / rejected
        │  published

Scheduler (APScheduler)
  └── Fires jobs on cron → calls module functions
       └── Job completion → broadcasts WS event → React Query cache invalidated
```

---

## Human Touchpoint Summary

```
Mon 07:00  Content Brief  → Review ideas + approve products     (20 min)
Mon 08:00  Products page  → Paste affiliate links               (15 min)
Tue-Fri
  11:00    QC Review      → Watch & approve/reject videos       (15-20 min)
Fri 15:00  Analytics      → Weekly charts + top hooks           (20 min)
Fri 21:00  Analytics      → Approve winners for remix           (10 min)
Sat 11:00  QC Review      → Weekend batch scan                  (10 min)
                                                          ──────────────
                                                          ~90 min/week
```
