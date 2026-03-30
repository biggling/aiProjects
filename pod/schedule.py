from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    # ── BIWEEKLY: 1st and 15th — Blue ocean runs after Gemini trends are fresh ─
    # Runs the day after gemini-trend (Mon/Wed) to have fresh context
    "blue-ocean":       {"task": "tasks.run_blue_ocean_scraper",   "schedule": crontab(hour=0,  minute=30, day_of_month="1,15")},

    # ── PRE-MIDNIGHT: Sun/Tue/Thu — Gemini runs before pytrends so scorer
    #    has all sources ready when it runs Mon/Wed/Fri at 01:00 ──────────
    "gemini-trend":     {"task": "tasks.run_gemini_trend_scraper", "schedule": crontab(hour=23, minute=30, day_of_week="0,2,4")},

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
