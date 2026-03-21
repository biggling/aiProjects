# CLAUDE.md

## Project Purpose
Amazon KDP automation — research niches, generate low-content book interiors (journals, planners, logbooks), create covers, and publish to Kindle Direct Publishing.

## Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Generate book interior
python src/interior_generator.py --type lined --pages 120 --size 6x9

# Research keywords
python src/keyword_research.py --niche "gratitude journal"

# Run tests
pytest tests/ -v
```

## Architecture

### Pipeline
```
Keyword Research → Niche Selection → Interior Generation → Cover Design → KDP Upload → Ads → Analytics
```

### Key Conventions
- Start with low-content books (fastest to ship)
- Target US market (English) first
- Book sizes: 6x9" (standard), 8.5x11" (large format)
- Interior generation via ReportLab (PDF)
- Cover design via Pillow
- All paths use `pathlib.Path`
- Logging via `loguru`
