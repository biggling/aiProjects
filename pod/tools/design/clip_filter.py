import torch
from PIL import Image
from sqlalchemy import select
from transformers import CLIPModel, CLIPProcessor

from tools.shared.db import get_session
from tools.shared.models import Design, Niche
from tools.shared.logger import get_logger

logger = get_logger("clip_filter")

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"
REJECT_THRESHOLD = 0.20

_model = None
_processor = None


def get_clip():
    """Load CLIP model and processor (singleton)."""
    global _model, _processor
    if _model is None:
        _model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
        _processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
    return _model, _processor


def compute_clip_score(image_path: str, text: str) -> float:
    """Compute cosine similarity between image and text using CLIP."""
    model, processor = get_clip()

    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=[text], images=image, return_tensors="pt", padding=True)

    with torch.no_grad():
        outputs = model(**inputs)
        # Normalise and compute cosine similarity
        image_embeds = outputs.image_embeds / outputs.image_embeds.norm(dim=-1, keepdim=True)
        text_embeds = outputs.text_embeds / outputs.text_embeds.norm(dim=-1, keepdim=True)
        similarity = (image_embeds @ text_embeds.T).item()

    return similarity


def run():
    """Score all processed designs with CLIP and auto-approve/reject."""
    logger.info("Starting CLIP filtering")

    with get_session() as session:
        designs = session.execute(
            select(Design).where(
                Design.status == "processed",
                Design.processed_path.isnot(None),
            )
        ).scalars().all()
        design_data = [(d.id, d.processed_path, d.niche_id) for d in designs]

    if not design_data:
        logger.info("No designs to filter")
        return "0 designs filtered"

    # Load niche keywords
    niche_ids = {nid for _, _, nid in design_data}
    with get_session() as session:
        niches = {n.id: n.keyword for n in session.execute(
            select(Niche).where(Niche.id.in_(niche_ids))
        ).scalars().all()}

    approved = 0
    rejected = 0

    for design_id, path, niche_id in design_data:
        keyword = niches.get(niche_id, "design")
        try:
            score = compute_clip_score(path, keyword)
            status = "approved" if score >= REJECT_THRESHOLD else "rejected"

            with get_session() as session:
                design = session.get(Design, design_id)
                design.clip_score = score
                design.status = status

            if status == "approved":
                approved += 1
            else:
                rejected += 1

            logger.info(f"  Design {design_id}: score={score:.3f} → {status}")
        except Exception as e:
            logger.error(f"  Design {design_id} CLIP failed: {e}")

    logger.info(f"CLIP filter complete: {approved} approved, {rejected} rejected")
    return f"{approved} approved, {rejected} rejected"
