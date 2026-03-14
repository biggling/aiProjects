"""Convert script body into video generation prompts."""

import json

from loguru import logger
from openai import OpenAI


def build_video_prompt(script_body: str) -> dict:
    """Use GPT-4o to produce a visual scene description for video generation."""
    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You convert text descriptions into short visual scene prompts for AI video generation. "
                    "Keep prompts under 15 words. Focus on visual action and product showcase. "
                    "Always respond with valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Create a video generation prompt for this script:\n\n{script_body}\n\n"
                    f"Return JSON with: scene (15 words max), style, aspect_ratio"
                ),
            },
        ],
        max_tokens=200,
        timeout=30,
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    result = {
        "scene": data.get("scene", "Product showcase with dynamic lighting"),
        "style": data.get("style", "realistic product demo"),
        "aspect_ratio": data.get("aspect_ratio", "9:16"),
    }
    logger.info(f"Video prompt: {result['scene']}")
    return result
