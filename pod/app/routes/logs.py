import os

from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse

from app.deps import templates, verify_credentials

router = APIRouter()

LOG_DIR = os.path.join("data", "logs")


@router.get("/logs", response_class=HTMLResponse)
def log_viewer(
    request: Request,
    file: str = Query(default=""),
    user: str = Depends(verify_credentials),
):
    log_files = []
    if os.path.exists(LOG_DIR):
        log_files = sorted([
            f for f in os.listdir(LOG_DIR)
            if f.endswith(".log")
        ])

    lines = []
    if file and file in log_files:
        filepath = os.path.join(LOG_DIR, file)
        with open(filepath) as f:
            all_lines = f.readlines()
            lines = all_lines[-200:][::-1]  # last 200, newest first

    return templates.TemplateResponse("logs.html", {
        "request": request,
        "log_files": log_files,
        "selected_file": file,
        "lines": lines,
    })
