import os

import markdown
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse

from app.deps import templates, verify_credentials

router = APIRouter()

LOG_DIR = os.path.join("data", "logs")


@router.get("/report", response_class=HTMLResponse)
def report_viewer(
    request: Request,
    file: str = Query(default=""),
    user: str = Depends(verify_credentials),
):
    report_files = []
    if os.path.exists(LOG_DIR):
        report_files = sorted([
            f for f in os.listdir(LOG_DIR)
            if f.startswith("report_") and f.endswith(".md")
        ], reverse=True)

    report_html = ""
    if file and file in report_files:
        filepath = os.path.join(LOG_DIR, file)
        with open(filepath) as f:
            report_html = markdown.markdown(f.read())

    return templates.TemplateResponse("report.html", {
        "request": request,
        "report_files": report_files,
        "selected_file": file,
        "report_html": report_html,
    })
