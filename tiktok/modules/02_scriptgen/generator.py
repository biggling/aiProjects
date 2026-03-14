"""Generate video scripts from approved content brief ideas."""

import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

from modules.01_research.db import SessionLocal, init_db
from modules.01_research.models import ContentBrief
from modules.02_scriptgen.models import Script
from modules.02_scriptgen.prompts import (
    EXPAND_PROMPT,
    SYSTEM_PROMPT,
    TRIM_PROMPT,
    USER_PROMPT_TEMPLATE,
)

load_dotenv()

SCRIPTS_DIR = Path("data/assets/scripts")
SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

WORD_MIN = 80
WORD_MAX = 120


def generate_scripts() -> list[dict]:
    """Generate scripts for all approved ideas in today's brief."""
    init_db()
    db = SessionLocal()
    client = OpenAI()
    generated = []

    try:
        today = date.today().isoformat()
        brief = (
            db.query(ContentBrief)
            .filter(ContentBrief.date == today)
            .order_by(ContentBrief.id.desc())
            .first()
        )

        if not brief:
            logger.warning("No content brief found for today")
            return []

        ideas = json.loads(brief.ideas_json)
        logger.info(f"Generating scripts for {len(ideas)} ideas")

        for idea in ideas:
            try:
                script_data = _generate_single_script(client, idea)
                script_data = _adjust_length(client, script_data)

                # Save to DB
                script = Script(
                    brief_id=brief.id,
                    product_id=idea.get("product_id", ""),
                    hook=script_data["hook"],
                    body=script_data["body"],
                    cta=script_data["cta"],
                    caption=script_data["caption"],
                    hashtags=json.dumps(script_data["hashtags"], ensure_ascii=False),
                )
                db.add(script)
                db.flush()

                # Save to file
                script_path = SCRIPTS_DIR / f"script_{script.id}.json"
                script_path.write_text(
                    json.dumps(script_data, ensure_ascii=False, indent=2)
                )
                logger.info(f"Script {script.id} saved to {script_path}")

                generated.append(script_data)

            except Exception as e:
                logger.error(f"Failed to generate script for idea: {e}")
                continue

        db.commit()
        logger.info(f"Generated {len(generated)} scripts")

    except Exception as e:
        db.rollback()
        logger.error(f"Script generation failed: {e}")
        raise
    finally:
        db.close()

    return generated


def _generate_single_script(client: OpenAI, idea: dict) -> dict:
    """Generate a single script from an idea."""
    user_prompt = USER_PROMPT_TEMPLATE.format(
        product_name=idea.get("product_name", "Unknown"),
        angle=idea.get("angle", "General review"),
        hook_idea=idea.get("hook_idea", ""),
        trending_sound=idea.get("trending_sound", "original"),
        duration_min=30,
        duration_max=45,
        word_min=WORD_MIN,
        word_max=WORD_MAX,
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        timeout=30,
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    return {
        "hook": data.get("hook", ""),
        "body": data.get("body", ""),
        "cta": data.get("cta", ""),
        "caption": data.get("caption", ""),
        "hashtags": data.get("hashtags", []),
    }


def _adjust_length(client: OpenAI, script_data: dict) -> dict:
    """Trim or expand script to target word count."""
    full_text = f"{script_data['hook']} {script_data['body']} {script_data['cta']}"
    word_count = len(full_text.split())

    if word_count > WORD_MAX:
        logger.info(f"Script too long ({word_count} words), trimming...")
        return _call_adjust(client, script_data, word_count, TRIM_PROMPT)
    elif word_count < WORD_MIN:
        logger.info(f"Script too short ({word_count} words), expanding...")
        return _call_adjust(client, script_data, word_count, EXPAND_PROMPT)

    return script_data


def _call_adjust(client: OpenAI, script_data: dict, word_count: int, template: str) -> dict:
    """Call GPT to adjust script length."""
    prompt = template.format(
        word_count=word_count,
        word_min=WORD_MIN,
        word_max=WORD_MAX,
        hook=script_data["hook"],
        body=script_data["body"],
        cta=script_data["cta"],
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        timeout=30,
        response_format={"type": "json_object"},
    )

    adjusted = json.loads(response.choices[0].message.content)
    script_data["hook"] = adjusted.get("hook", script_data["hook"])
    script_data["body"] = adjusted.get("body", script_data["body"])
    script_data["cta"] = adjusted.get("cta", script_data["cta"])
    return script_data


if __name__ == "__main__":
    scripts = generate_scripts()
    print(f"Generated {len(scripts)} scripts")
