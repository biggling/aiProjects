# CLAUDE.md

## Project Purpose
Shopee affiliate marketing automation for Thailand — discover trending products, generate content, post to Facebook/TikTok/LINE, track commissions.

## Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run trend scraper
python src/scraper.py

# Generate content batch
python src/content_gen.py

# Run tests
pytest tests/ -v
```

## Architecture

### Pipeline
```
Scrape Trending Products → Filter by Commission → Generate Content → Schedule Posts → Track Performance
```

### Key Conventions
- Target market: Thailand (Thai language content)
- Platforms: Facebook, TikTok, LINE (in priority order)
- Commission threshold: ≥10% to be worth promoting
- Mega-sale calendar drives campaign timing
- All config via `.env` + YAML
- Logging via `loguru`
- File paths via `pathlib.Path`
