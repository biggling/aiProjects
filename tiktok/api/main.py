"""FastAPI backend — app factory, mounts routers, serves dashboard."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routers import analytics, brief, products, schedule, videos
from api.ws import manager
from modules.01_research.db import init_db

load_dotenv()

app = FastAPI(title="TikTok Automation API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(videos.router)
app.include_router(brief.router)
app.include_router(analytics.router)
app.include_router(products.router)
app.include_router(schedule.router)


@app.on_event("startup")
async def startup():
    init_db()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Serve React dashboard (production)
DASHBOARD_DIST = Path(__file__).parent.parent / "dashboard" / "dist"

if DASHBOARD_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(DASHBOARD_DIST / "assets")), name="static")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """SPA fallback — serve index.html for all non-API routes."""
        file_path = DASHBOARD_DIST / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(DASHBOARD_DIST / "index.html"))
