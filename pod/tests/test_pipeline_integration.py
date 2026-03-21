"""Integration tests — verify the full pipeline status flow and task logging."""

import pytest
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

from tools.shared.db import get_session
from tools.shared.models import Niche, Prompt, Design, Listing, TaskLog


class TestStatusTransitions:
    """Verify status fields drive the pipeline correctly."""

    def test_niche_status_flow(self, setup_db):
        """Niche: active → paused → killed."""
        with get_session() as session:
            niche = Niche(keyword="test-niche", trend_score=80, status="active")
            session.add(niche)
            session.flush()
            niche_id = niche.id

        # Transition to paused
        with get_session() as session:
            niche = session.get(Niche, niche_id)
            assert niche.status == "active"
            niche.status = "paused"

        with get_session() as session:
            niche = session.get(Niche, niche_id)
            assert niche.status == "paused"
            niche.status = "killed"

        with get_session() as session:
            niche = session.get(Niche, niche_id)
            assert niche.status == "killed"

    def test_design_status_flow(self, setup_db):
        """Design: pending → generated → processed → approved → mockup_ready."""
        with get_session() as session:
            niche = Niche(keyword="design-test", status="active")
            session.add(niche)
            session.flush()
            prompt = Prompt(niche_id=niche.id, prompt_text="test prompt")
            session.add(prompt)
            session.flush()
            design = Design(
                prompt_id=prompt.id, niche_id=niche.id,
                raw_path="/tmp/raw.png", status="pending",
            )
            session.add(design)
            session.flush()
            design_id = design.id

        statuses = ["generated", "processed", "approved", "mockup_ready"]
        for status in statuses:
            with get_session() as session:
                design = session.get(Design, design_id)
                design.status = status
            with get_session() as session:
                design = session.get(Design, design_id)
                assert design.status == status

    def test_listing_status_flow(self, setup_db):
        """Listing: pending → copy_ready → uploaded → live."""
        with get_session() as session:
            niche = Niche(keyword="listing-test", status="active")
            session.add(niche)
            session.flush()
            prompt = Prompt(niche_id=niche.id, prompt_text="test")
            session.add(prompt)
            session.flush()
            design = Design(prompt_id=prompt.id, niche_id=niche.id, status="mockup_ready")
            session.add(design)
            session.flush()
            listing = Listing(
                design_id=design.id, niche_id=niche.id,
                title="Test Product", status="pending",
            )
            session.add(listing)
            session.flush()
            listing_id = listing.id

        for status in ["copy_ready", "uploaded", "live"]:
            with get_session() as session:
                listing = session.get(Listing, listing_id)
                listing.status = status
            with get_session() as session:
                listing = session.get(Listing, listing_id)
                assert listing.status == status


class TestTaskLogging:
    """Verify _run_with_logging wrapper behavior."""

    def test_successful_task_logged(self, setup_db):
        """Successful task creates a TaskLog with status=done."""
        from tasks import _run_with_logging

        result = _run_with_logging("test_task", lambda: {"items": 5})

        with get_session() as session:
            logs = session.query(TaskLog).filter_by(task_name="test_task").all()
            assert len(logs) == 1
            assert logs[0].status == "done"
            assert logs[0].finished_at is not None
            assert "5" in logs[0].result_summary

    def test_failed_task_logged(self, setup_db):
        """Failed task creates a TaskLog with status=failed and error message."""
        from tasks import _run_with_logging

        def _failing():
            raise ValueError("something broke")

        with pytest.raises(ValueError):
            _run_with_logging("failing_task", _failing)

        with get_session() as session:
            logs = session.query(TaskLog).filter_by(task_name="failing_task").all()
            assert len(logs) == 1
            assert logs[0].status == "failed"
            assert "something broke" in logs[0].error


class TestPipelineEndToEnd:
    """Smoke test: create records through the full pipeline chain."""

    def test_full_pipeline_chain(self, setup_db):
        """Niche → Prompt → Design → Listing with correct relationships."""
        with get_session() as session:
            # Phase 1: Create niche (trend research output)
            niche = Niche(
                keyword="minimalist cat art",
                trend_score=85.0,
                velocity=12.5,
                competition=0.3,
                final_score=78.0,
                status="active",
            )
            session.add(niche)
            session.flush()
            niche_id = niche.id

            # Phase 2: Create prompt (design generation input)
            prompt = Prompt(
                niche_id=niche_id,
                prompt_text="A minimalist line drawing of a cat sitting",
                status="pending",
            )
            session.add(prompt)
            session.flush()
            prompt_id = prompt.id

            # Phase 2: Create design (image generation output)
            design = Design(
                prompt_id=prompt_id,
                niche_id=niche_id,
                raw_path="/data/designs/raw_001.png",
                processed_path="/data/designs/processed_001.png",
                mockup_path="/data/designs/mockup_001.png",
                clip_score=0.82,
                status="mockup_ready",
            )
            session.add(design)
            session.flush()
            design_id = design.id

            # Phase 3+4: Create listing (copy + upload)
            listing = Listing(
                design_id=design_id,
                niche_id=niche_id,
                title="Minimalist Cat Art Print",
                description="Beautiful minimalist cat line art",
                tags=["cat", "minimalist", "art", "print"],
                status="live",
                etsy_listing_id="etsy_123",
                printify_product_id="printify_456",
            )
            session.add(listing)
            session.flush()
            listing_id = listing.id

        # Verify full chain via relationships
        with get_session() as session:
            niche = session.get(Niche, niche_id)
            assert len(niche.prompts) == 1
            assert len(niche.designs) == 1
            assert len(niche.listings) == 1
            assert niche.listings[0].title == "Minimalist Cat Art Print"
            assert niche.listings[0].design.clip_score == 0.82
            assert niche.listings[0].design.prompt.prompt_text.startswith("A minimalist")
