"""Claude and OpenAI API wrappers for autoGenVideo."""
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


def generate_video_script(topic: str, platform: str, duration: int, language: str = "en") -> dict:
    """Generate a full video script for a short-form platform."""
    words_target = int(duration * 2.5)  # ~2.5 words/sec
    prompt = f"""You are a viral short-form video script writer for {platform}.
Create a {duration}-second script about: "{topic}"
Language: {language}
Target ~{words_target} words in voiceover.

Return ONLY valid JSON:
{{
  "hook": "First 3 seconds — bold statement or question (max 15 words)",
  "body": ["scene1 text", "scene2 text", "scene3 text"],
  "cta": "Call to action (e.g. Like and follow for more!)",
  "caption": "Platform caption max 150 chars",
  "voiceover_text": "Full natural voiceover script {words_target} words",
  "hashtags": ["#tag1", "#tag2", "#tag3", "#tag4", "#tag5"]
}}"""
    return ask_claude_json(prompt)


def generate_improved_hook(original_hook: str, topic: str) -> list[str]:
    """Generate 3 alternative hooks for underperforming video."""
    prompt = f"""The original hook "{original_hook}" for topic "{topic}" underperformed.
Generate 3 alternative hooks using: question format, bold claim, or curiosity gap.
Return ONLY valid JSON: {{"hooks": ["hook1", "hook2", "hook3"]}}"""
    result = ask_claude_json(prompt)
    return result.get("hooks", [original_hook])


def generate_dalle_image(prompt: str) -> str:
    """Generate image with DALL-E 3, return URL."""
    response = _openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1792",  # closest to 9:16
        quality="standard",
        n=1,
    )
    return response.data[0].url
