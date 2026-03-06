"""Claude and OpenAI API wrappers."""
import json
import anthropic
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
from config import ANTHROPIC_API_KEY, OPENAI_API_KEY, CLAUDE_MODEL, get_logger

logger = get_logger("ai_utils")
_claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
_openai = openai.OpenAI(api_key=OPENAI_API_KEY)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def ask_claude(prompt: str, system: str = "", max_tokens: int = 2048) -> str:
    messages = [{"role": "user", "content": prompt}]
    kwargs = {"model": CLAUDE_MODEL, "max_tokens": max_tokens, "messages": messages}
    if system:
        kwargs["system"] = system
    response = _claude.messages.create(**kwargs)
    return response.content[0].text


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def ask_claude_json(prompt: str, system: str = "", max_tokens: int = 2048) -> dict:
    """Ask Claude and parse JSON response."""
    raw = ask_claude(prompt, system=system, max_tokens=max_tokens)
    # Extract JSON block if wrapped in ```json ... ```
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    return json.loads(raw)


def generate_design_brief(niche: str) -> dict:
    """Generate design brief + DALL-E prompts for a niche."""
    prompt = f"""You are a POD design expert. Given the niche "{niche}", generate:
1. A design brief (50 words): visual style, mood, color palette
2. Three DALL-E 3 prompts for print-ready artwork (transparent background, high contrast)
3. Five catchy text/quote ideas for typography designs

Return ONLY valid JSON in this format:
{{
  "brief": "...",
  "dalle_prompts": ["...", "...", "..."],
  "quotes": ["...", "...", "...", "...", "..."]
}}"""
    return ask_claude_json(prompt)


def generate_listing_seo(niche: str, style: str, platform: str = "etsy") -> dict:
    """Generate SEO-optimized listing content."""
    tag_count = 13 if platform == "etsy" else 7
    prompt = f"""Generate a {platform.title()} POD listing for niche "{niche}", style "{style}":
- title: max 140 chars, primary keyword first
- description: 150-200 words, storytelling + keyword-rich
- tags: exactly {tag_count} comma-separated keywords (no spaces around commas)
- bullets: 5 Amazon-style feature bullet points

Return ONLY valid JSON:
{{
  "title": "...",
  "description": "...",
  "tags": "tag1,tag2,...",
  "bullets": ["...", "...", "...", "...", "..."]
}}"""
    return ask_claude_json(prompt)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=5, max=30))
def generate_dalle_image(prompt: str, size: str = "1024x1024") -> str:
    """Generate image with DALL-E 3. Returns URL."""
    response = _openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality="hd",
        n=1,
    )
    return response.data[0].url
