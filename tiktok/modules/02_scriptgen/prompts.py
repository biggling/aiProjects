"""Prompt templates for TikTok video script generation."""

SYSTEM_PROMPT = """You are an energetic, authentic TikTok creator from Thailand.
You write scripts for short-form affiliate marketing videos that feel natural and engaging.
Your tone is enthusiastic but genuine — like a friend recommending something they actually use.
Always write in Thai unless instructed otherwise.
Always respond with valid JSON only."""

USER_PROMPT_TEMPLATE = """Write a TikTok video script for this product:

Product: {product_name}
Creative angle: {angle}
Hook idea: {hook_idea}
Trending sound: {trending_sound}
Target duration: {duration_min}-{duration_max} seconds (about {word_min}-{word_max} words)

Create a script with these sections:
1. **Hook** (first 3 seconds) — attention-grabbing opening line
2. **Body** (main content) — demonstrate value, show the product, build desire
3. **CTA** (call to action) — tell them to click the link, buy now, etc.
4. **Caption** — the text caption for the TikTok post
5. **Hashtags** — 5 relevant hashtags

Return JSON with keys: hook, body, cta, caption, hashtags (array of strings)"""

TRIM_PROMPT = """This script is {word_count} words but needs to be {word_min}-{word_max} words.
Please shorten it while keeping the hook punchy and the CTA clear.

Current script:
Hook: {hook}
Body: {body}
CTA: {cta}

Return the trimmed version as JSON with keys: hook, body, cta"""

EXPAND_PROMPT = """This script is {word_count} words but needs to be {word_min}-{word_max} words.
Please expand the body with more compelling details while keeping it natural.

Current script:
Hook: {hook}
Body: {body}
CTA: {cta}

Return the expanded version as JSON with keys: hook, body, cta"""
