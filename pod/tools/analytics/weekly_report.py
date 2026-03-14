import os
from datetime import datetime, timezone

from sqlalchemy import select, func

from tools.shared.api_clients import get_anthropic
from tools.shared.db import get_session
from tools.shared.models import Listing, Niche
from tools.shared.notify import notify
from tools.shared.logger import get_logger

logger = get_logger("weekly_report")

REPORT_DIR = os.path.join("data", "logs")


def gather_data() -> dict:
    """Collect weekly performance data from DB."""
    with get_session() as session:
        # Top niches by revenue
        top_niches = session.execute(
            select(Niche.keyword, func.sum(Listing.revenue).label("total_rev"))
            .join(Listing, Listing.niche_id == Niche.id)
            .group_by(Niche.keyword)
            .order_by(func.sum(Listing.revenue).desc())
            .limit(5)
        ).all()

        # Top listings by revenue
        top_listings = session.execute(
            select(Listing).order_by(Listing.revenue.desc()).limit(5)
        ).scalars().all()

        # Totals
        total_revenue = session.execute(
            select(func.sum(Listing.revenue))
        ).scalar() or 0

        total_listings = session.execute(
            select(func.count(Listing.id)).where(Listing.status == "live")
        ).scalar() or 0

        total_views = session.execute(
            select(func.sum(Listing.views))
        ).scalar() or 0

        return {
            "top_niches": [(kw, float(rev or 0)) for kw, rev in top_niches],
            "top_listings": [(l.title, float(l.revenue or 0)) for l in top_listings],
            "total_revenue": float(total_revenue),
            "total_listings": total_listings,
            "total_views": int(total_views or 0),
        }


def generate_report(data: dict) -> str:
    """Use Claude to summarise weekly data and make recommendations."""
    client = get_anthropic()

    data_text = (
        f"Total revenue: ${data['total_revenue']:.2f}\n"
        f"Total live listings: {data['total_listings']}\n"
        f"Total views: {data['total_views']}\n\n"
        f"Top niches by revenue:\n"
    )
    for kw, rev in data["top_niches"]:
        data_text += f"  - {kw}: ${rev:.2f}\n"
    data_text += "\nTop listings:\n"
    for title, rev in data["top_listings"]:
        data_text += f"  - {title[:60]}: ${rev:.2f}\n"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                "Summarise this weekly POD business data. Include:\n"
                "1. Performance summary\n"
                "2. Top 3 niches to scale (and why)\n"
                "3. Top 2 niches to consider killing (and why)\n"
                "4. One actionable recommendation\n\n"
                f"{data_text}"
            ),
        }],
    )

    return response.content[0].text


def run():
    """Generate and save weekly report."""
    logger.info("Starting weekly report generation")

    data = gather_data()
    report_text = generate_report(data)

    # Save report
    os.makedirs(REPORT_DIR, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    report_path = os.path.join(REPORT_DIR, f"report_{date_str}.md")

    with open(report_path, "w") as f:
        f.write(f"# Weekly Report — {date_str}\n\n")
        f.write(report_text)

    # Notify
    summary = f"Weekly report: ${data['total_revenue']:.2f} revenue, {data['total_listings']} live listings"
    notify("Weekly Report", summary, level="info")

    logger.info(f"Report saved to {report_path}")
    return f"Report saved: {report_path}"
