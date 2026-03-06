"""Claude and OpenAI wrappers for autoTiktok."""
import json
import anthropic
import openai
from tenacity import retry, stop_after_attempt, wait_exponential
from config import ANTHROPIC_API_KEY, OPENAI_API_KEY, CLAUDE_MODEL, get_logger

logger = get_logger("ai_utils")
_claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
_openai = openai.OpenAI(api_key=OPENAI_API_KEY)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
def ask_claude(prompt: str, system: str = "", max_tokens: int = 1024) -> str:
    msgs = [{"role": "user", "content": prompt}]
    kwargs = {"model": CLAUDE_MODEL, "max_tokens": max_tokens, "messages": msgs}
    if system:
        kwargs["system"] = system
    return _claude.messages.create(**kwargs).content[0].text


def ask_claude_json(prompt: str, system: str = "", max_tokens: int = 1024) -> dict:
    raw = ask_claude(prompt, system=system, max_tokens=max_tokens)
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0].strip()
    return json.loads(raw)


def generate_tiktok_script(
    product_name: str, niche: str, hook_pattern: str,
    duration: int = 30, language: str = "en"
) -> dict:
    words_target = int(duration * 2.5)
    prompt = f"""You are a viral TikTok content creator for {niche}.
Generate a {duration}s video script promoting "{product_name}" using the "{hook_pattern}" hook style.
Language: {language}. Target ~{words_target} words voiceover.

Return ONLY valid JSON:
{{
  "hook": "0–3s hook (max 12 words, {hook_pattern} style)",
  "body": ["scene1: product intro (10s)", "scene2: product demo (10s)", "scene3: benefit or social proof (7s)"],
  "cta": "Comment LINK for the link!",
  "caption": "Max 150 chars headline",
  "voiceover_text": "Natural conversational script ~{words_target} words",
  "hashtags": ["#broad", "#niche1", "#niche2", "#trending", "#fyp"],
  "confidence_score": 0.85
}}"""
    return ask_claude_json(prompt)


def classify_hook_pattern(hook_text: str) -> dict:
    prompt = f"""Classify this TikTok hook: "{hook_text}"
Patterns: question, bold_claim, tutorial, reaction, curiosity_gap
Return ONLY: {{"pattern": "...", "confidence": 0.0}}"""
    return ask_claude_json(prompt)


def generate_comment_reply(comment_text: str, niche: str, product_name: str) -> str:
    prompt = f"""Reply to this TikTok comment about {niche}/{product_name}:
Comment: "{comment_text}"
Write a warm, authentic reply (max 100 chars). No spam tone. Encourage engagement.
Return ONLY the reply text."""
    return ask_claude(prompt, max_tokens=100)


def generate_dalle_scene(scene_description: str) -> str:
    """Generate product scene image via DALL-E 3, return URL."""
    r = _openai.images.generate(
        model="dall-e-3",
        prompt=f"Vertical 9:16 photo of {scene_description}, vibrant, professional, no text, social media style",
        size="1024x1792",
        quality="standard",
        n=1,
    )
    return r.data[0].url
