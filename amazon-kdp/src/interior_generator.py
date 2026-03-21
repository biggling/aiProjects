"""Generate low-content book interiors as PDF files.

Supports: lined pages, dot grid, graph paper, blank with margins.
Output is KDP-ready PDF at specified trim size.
"""

from pathlib import Path
from reportlab.lib.pagesizes import inch
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas
from loguru import logger
import argparse

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# KDP trim sizes (width, height) in inches
TRIM_SIZES = {
    "5x8": (5 * inch, 8 * inch),
    "5.5x8.5": (5.5 * inch, 8.5 * inch),
    "6x9": (6 * inch, 9 * inch),
    "7x10": (7 * inch, 10 * inch),
    "8.5x11": (8.5 * inch, 11 * inch),
}

LIGHT_GRAY = Color(0.85, 0.85, 0.85)
MEDIUM_GRAY = Color(0.7, 0.7, 0.7)
DOT_GRAY = Color(0.6, 0.6, 0.6)


def generate_lined(
    output_path: Path,
    num_pages: int = 120,
    trim_size: str = "6x9",
    line_spacing: float = 0.35 * inch,
    margin: float = 0.75 * inch,
    header_line: bool = True,
) -> Path:
    """Generate a lined notebook interior."""
    width, height = TRIM_SIZES[trim_size]
    c = canvas.Canvas(str(output_path), pagesize=(width, height))

    for page in range(num_pages):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)

        y = height - margin
        if header_line:
            # Thicker header line for date/title
            c.setStrokeColor(MEDIUM_GRAY)
            c.setLineWidth(1)
            c.line(margin, y, width - margin, y)
            c.setStrokeColor(LIGHT_GRAY)
            c.setLineWidth(0.5)
            y -= line_spacing * 1.5

        while y > margin:
            c.line(margin, y, width - margin, y)
            y -= line_spacing

        # Page number
        c.setFont("Helvetica", 8)
        c.setFillColor(MEDIUM_GRAY)
        x_pos = width - margin if page % 2 == 0 else margin
        c.drawString(x_pos, margin / 2, str(page + 1))

        c.showPage()

    c.save()
    logger.info(f"Generated lined interior: {num_pages} pages, {trim_size}, saved to {output_path}")
    return output_path


def generate_dot_grid(
    output_path: Path,
    num_pages: int = 120,
    trim_size: str = "6x9",
    dot_spacing: float = 0.2 * inch,
    margin: float = 0.75 * inch,
    dot_radius: float = 0.8,
) -> Path:
    """Generate a dot grid notebook interior."""
    width, height = TRIM_SIZES[trim_size]
    c = canvas.Canvas(str(output_path), pagesize=(width, height))

    for page in range(num_pages):
        c.setFillColor(DOT_GRAY)

        x = margin
        while x <= width - margin:
            y = margin
            while y <= height - margin:
                c.circle(x, y, dot_radius, fill=1, stroke=0)
                y += dot_spacing
            x += dot_spacing

        # Page number
        c.setFont("Helvetica", 8)
        c.setFillColor(MEDIUM_GRAY)
        x_pos = width - margin if page % 2 == 0 else margin
        c.drawString(x_pos, margin / 2, str(page + 1))

        c.showPage()

    c.save()
    logger.info(f"Generated dot grid interior: {num_pages} pages, {trim_size}, saved to {output_path}")
    return output_path


def generate_graph(
    output_path: Path,
    num_pages: int = 120,
    trim_size: str = "6x9",
    grid_spacing: float = 0.2 * inch,
    margin: float = 0.75 * inch,
) -> Path:
    """Generate a graph paper interior."""
    width, height = TRIM_SIZES[trim_size]
    c = canvas.Canvas(str(output_path), pagesize=(width, height))

    for page in range(num_pages):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.3)

        # Vertical lines
        x = margin
        while x <= width - margin:
            c.line(x, margin, x, height - margin)
            x += grid_spacing

        # Horizontal lines
        y = margin
        while y <= height - margin:
            c.line(margin, y, width - margin, y)
            y += grid_spacing

        # Page number
        c.setFont("Helvetica", 8)
        c.setFillColor(MEDIUM_GRAY)
        x_pos = width - margin if page % 2 == 0 else margin
        c.drawString(x_pos, margin / 2, str(page + 1))

        c.showPage()

    c.save()
    logger.info(f"Generated graph interior: {num_pages} pages, {trim_size}, saved to {output_path}")
    return output_path


GENERATORS = {
    "lined": generate_lined,
    "dot": generate_dot_grid,
    "graph": generate_graph,
}


def main():
    parser = argparse.ArgumentParser(description="Generate KDP book interiors")
    parser.add_argument("--type", choices=GENERATORS.keys(), default="lined")
    parser.add_argument("--pages", type=int, default=120)
    parser.add_argument("--size", choices=TRIM_SIZES.keys(), default="6x9")
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = OUTPUT_DIR / f"{args.type}_{args.pages}p_{args.size}.pdf"

    generator = GENERATORS[args.type]
    generator(output_path, num_pages=args.pages, trim_size=args.size)
    print(f"Created: {output_path}")


if __name__ == "__main__":
    main()
