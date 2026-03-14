from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tools.shared.db import init_db
from tools.upload.order_router import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="POD Dashboard", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(order_router)

from app.routes import dashboard, tasks_view, designs, listings, niches, logs, report

app.include_router(dashboard.router)
app.include_router(tasks_view.router)
app.include_router(designs.router)
app.include_router(listings.router)
app.include_router(niches.router)
app.include_router(logs.router)
app.include_router(report.router)
