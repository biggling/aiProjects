# POD (Print on Demand) — Session State

## Current Phase
Phase 9: Integration Tests — COMPLETE ✅
Phase 10: Shop Launch — IN PROGRESS

## Last Session
2026-03-30 — Added Gemini image generation, prompt metadata, trend snapshot system. All 68 tests pass.

## What Was Done
1. **New DB table: `TrendSnapshot`** (`tools/shared/models.py`)
   - Stores point-in-time trend readings per niche per source
   - Fields: niche_id, source, trend_score, velocity, rank_position, reason, is_upcoming, horizon_days, snapshot_date
   - Accumulates over time → enables popularity comparison across Gemini / pytrends / Reddit / Etsy

2. **New fields on `Niche`**: gemini_reason, upcoming_score, source_scores (JSON breakdown per source)

3. **New fields on `Prompt`**: keywords (JSON), design_style, product_types (JSON), target_persona, color_palette, image_backend
   - Prompts now store full SEO and design metadata for each product

4. **New fields on `Design`**: image_backend, generation_params (JSON audit trail)

5. **`tools/design/image_generator.py`** — Full rewrite with 3-backend router:
   - `_generate_gemini()` — Imagen 3 (`imagen-3.0-generate-002`) or Gemini 2.0 Flash image gen
   - `_generate_stability()` — Stability AI SDXL (unchanged)
   - `_generate_dalle()` — DALL-E 3 (new)
   - `generate_image()` — routes by IMAGE_BACKEND env var ("auto" = Gemini first)
   - "auto" priority: Gemini → Stability → DALL-E (cheapest + best first)

6. **`tools/trend/gemini_trend_scraper.py`** — Major enhancement:
   - Two-phase run: current trends (20) + upcoming trends (15 with horizon_days)
   - Both phases save `TrendSnapshot` rows (is_upcoming flag)
   - `get_trend_rankings()` — composite-scored ranking across all sources
   - Upcoming bonus: niches with upcoming_score > trend_score get +10% composite boost

7. **`tools/trend/niche_scorer.py`** — Multi-source snapshot scoring:
   - `_compute_niche_score()` — weighted composite: gemini×0.40 + pytrends×0.30 + reddit×0.15 + etsy×0.15
   - Velocity boost (±20%), upcoming bonus (+15%), competition penalty
   - Falls back to legacy direct-field scoring if no snapshots exist
   - `compute_score(trend, velocity, competition)` preserved for unit tests

8. **`tools/design/prompt_generator.py`** — Enhanced to generate full metadata JSON:
   - Claude now returns objects with: prompt_text, keywords, design_style, product_types, target_persona, color_palette
   - Backward compatible (handles legacy string-only responses)

9. **`tools/shared/api_clients.py`** — Added `get_gemini()` singleton

10. **`tools/shared/config.py`** — Added IMAGE_BACKEND, GEMINI_IMAGE_MODEL config vars

11. **`tasks.py`** — Added `run_gemini_trend_scraper` task

12. **`schedule.py`** — Gemini trend runs Sun/Tue/Thu 23:30 (feeds snapshots before pytrends runs Mon/Wed/Fri 00:00)

13. **`requirements.txt`** — Added `google-genai>=1.0.0`

14. All 68 tests pass ✅

## New .env Variables Required
```bash
GEMINI_API_KEY=...            # from Google AI Studio (aistudio.google.com)
IMAGE_BACKEND=auto            # auto | gemini | stability | dalle
GEMINI_IMAGE_MODEL=imagen-3.0-generate-002   # or gemini-2.0-flash-preview-image-generation
```

## Architecture: Trend Pipeline Data Flow
```
Sun/Tue/Thu 23:30  → gemini_trend_scraper  → TrendSnapshot (gemini, is_upcoming=False/True)
Mon/Wed/Fri 00:00  → trend_scraper         → TrendSnapshot (pytrends)
Mon/Wed/Fri 00:30  → reddit_scraper        → TrendSnapshot (reddit)
Mon/Wed/Fri 01:00  → niche_scorer          → Niche.final_score (composite from all snapshots)
Mon/Wed/Fri 02:00  → prompt_generator      → Prompt rows with full metadata
Mon/Wed/Fri 03:00  → image_generator       → Design rows (Gemini/Stability/DALL-E auto-routing)
```

## Next Actions
1. **URGENT — Shop A launch (this week):**
   - Create Etsy account, Gelato account
   - Set all env vars in .env (ETSY_API_KEY, ETSY_SHOP_ID, GELATO_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY)
   - Run Alembic migration: `alembic revision --autogenerate -m "add trend snapshot and prompt metadata"` then `alembic upgrade head`
   - Start Celery worker + beat

2. **Phase 8 — VPS deploy:**
   - Create docker-compose.prod.yml + deploy.sh

3. **Dashboard — expose TrendSnapshot rankings:**
   - Add `/api/trends/rankings` endpoint using `get_trend_rankings()` from gemini_trend_scraper
