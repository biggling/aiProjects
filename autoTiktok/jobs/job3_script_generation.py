"""Job 3: Script & Creative Generation
Schedule: Every 6 hours
"""
import json
from datetime import datetime
from pathlib import Path
from database.models import SessionLocal, Niche, Trend, Script
from utils.ai_utils import generate_tiktok_script
from utils.notify import alert_review_queue
from config import SCRIPTS_DIR, REVIEW_QUEUE_DIR, REVIEW_QUEUE_TIMEOUT_HOURS, get_logger

logger = get_logger("job3_script_generation")


def auto_approve_timed_out(session):
    """Auto-approve scripts in review queue after timeout."""
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(hours=REVIEW_QUEUE_TIMEOUT_HOURS)
    pending = session.query(Script).filter(
        Script.status == "pending",
        Script.created_at < cutoff,
    ).all()
    for script in pending:
        script.status = "approved"
        logger.info(f"Auto-approved script {script.id} after {REVIEW_QUEUE_TIMEOUT_HOURS}h timeout")
    return len(pending)


def run():
    logger.info("=== Job 3: Script Generation started ===")

    session = SessionLocal()
    generated = 0

    try:
        # Auto-approve timed-out review items
        auto_approved = auto_approve_timed_out(session)
        if auto_approved > 0:
            logger.info(f"Auto-approved {auto_approved} scripts")

        # Get top products without recent scripts
        products = session.query(Niche).filter_by(status="active").order_by(
            Niche.performance_score.desc()
        ).limit(5).all()

        new_in_queue = 0
        for product in products:
            # Get best hook pattern for this niche
            trend = session.query(Trend).filter_by(niche=product.niche).order_by(
                Trend.views.desc()
            ).first()
            hook_pattern = trend.hook_pattern if trend else "bold_claim"

            try:
                script_data = generate_tiktok_script(
                    product_name=product.product_name or product.niche,
                    niche=product.niche,
                    hook_pattern=hook_pattern,
                    duration=30,
                    language="en",
                )

                confidence = float(script_data.get("confidence_score", 0.7))
                status = "approved" if confidence >= 0.85 else "pending"

                script = Script(
                    product_id=product.id,
                    hook=script_data.get("hook", ""),
                    body=json.dumps(script_data.get("body", [])),
                    cta=script_data.get("cta", "Link in bio!"),
                    voiceover_text=script_data.get("voiceover_text", ""),
                    caption=script_data.get("caption", ""),
                    hashtags=",".join(script_data.get("hashtags", [])),
                    confidence_score=confidence,
                    status=status,
                )
                session.add(script)
                session.flush()

                # Save to review queue file
                queue_file = REVIEW_QUEUE_DIR / f"{script.id}.json"
                queue_data = {
                    "script_id": script.id,
                    "product": product.product_name,
                    "niche": product.niche,
                    "hook": script_data.get("hook"),
                    "confidence": confidence,
                    "status": status,
                }
                queue_file.write_text(json.dumps(queue_data, indent=2))

                generated += 1
                if status == "pending":
                    new_in_queue += 1
                logger.info(f"Script {script.id} generated ({status}): {product.product_name[:40]}")

            except Exception as e:
                logger.error(f"Script gen failed for {product.product_name}: {e}")

        session.commit()

        if new_in_queue > 0:
            alert_review_queue(new_in_queue, str(REVIEW_QUEUE_DIR))

        logger.info(f"=== Job 3 complete — {generated} scripts generated ===")
    except Exception as e:
        session.rollback()
        logger.error(f"Job 3 failed: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    run()
