"""
MedQuery – Medical Information Retrieval System
FastAPI Application Entrypoint
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure project root is in python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.api.routes import router, get_search_service

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Preloading MedQuery search service on startup...")
    service = get_search_service()
    print("MedQuery backend startup complete and ready to serve queries.")
    yield

app = FastAPI(
    title="MedQuery – Medical Information Retrieval System",
    description="Hybrid Medical Document Retrieval and Semantic Ranking using BM25 and BERT",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount results directory as static files for evaluation charts
os.makedirs(os.path.join(ROOT_DIR, "results"), exist_ok=True)
app.mount("/static/results", StaticFiles(directory=os.path.join(ROOT_DIR, "results")), name="results")

# Include routes for both direct and /api prefixed access
app.include_router(router, prefix="")
app.include_router(router, prefix="/api")

# Serve built React frontend if available
from fastapi.responses import FileResponse
frontend_dist = os.path.join(ROOT_DIR, "frontend", "dist")
if os.path.exists(frontend_dist):
    frontend_assets = os.path.join(frontend_dist, "assets")
    if os.path.exists(frontend_assets):
        app.mount("/assets", StaticFiles(directory=frontend_assets), name="frontend-assets")

    @app.get("/app", include_in_schema=False)
    @app.get("/dashboard", include_in_schema=False)
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_dist, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
