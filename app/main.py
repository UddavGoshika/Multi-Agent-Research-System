import logging
import os

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.orchestrator import run_pipeline

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Multi-Agent Research System",
    description="A planner -> researcher -> analyst -> writer agent pipeline "
    "that researches any topic on the open web and streams its progress live.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.get("/api/research")
async def research(
    topic: str = Query(..., min_length=3, max_length=300),
    model: str | None = Query(default=None),
):
    """
    Streams Server-Sent Events describing each agent's progress, ending
    with a `final` event containing the full markdown report.
    """
    return StreamingResponse(
        run_pipeline(topic, model=model),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable proxy buffering (e.g. on Render/Nginx)
        },
    )
