import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.config import settings
from app.database import init_db
from app.cache import cache_manager
from app.search import search_manager

# Import all routers
from app.routers.auth import router as auth_router
from app.routers.dsa import router as dsa_router
from app.routers.system_design import router as system_design_router
from app.routers.lld import router as lld_router
from app.routers.ai import router as ai_router
from app.routers.backend_lab import router as backend_lab_router
from app.routers.leetcode import router as leetcode_router
from app.routers.books import router as books_router
from app.routers.tracker import router as tracker_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    # Initialize SQL database (SQLite/PostgreSQL)
    await init_db()
    
    # Initialize cache manager (Redis)
    await cache_manager.connect()
    
    # Initialize search manager (Elasticsearch)
    await search_manager.connect()
    
    yield
    # Shutdown actions (if any)
    if cache_manager.redis:
        await cache_manager.redis.close()
    if search_manager.es:
        await search_manager.es.close()

app = FastAPI(
    title=settings.APP_NAME,
    description="Full Stack Senior SDE Learning Portal with Live Backend Lab",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Setup for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API Routers
app.include_router(auth_router)
app.include_router(dsa_router)
app.include_router(system_design_router)
app.include_router(lld_router)
app.include_router(ai_router)
app.include_router(backend_lab_router)
app.include_router(leetcode_router)
app.include_router(books_router)
app.include_router(tracker_router)

# Serve the frontend directly from root paths so the application is self-contained
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))

@app.get("/styles.css")
async def serve_css():
    return FileResponse(os.path.join(BASE_DIR, "styles.css"))

@app.get("/script.js")
async def serve_js():
    return FileResponse(os.path.join(BASE_DIR, "script.js"))

@app.get("/leetcode-questions.csv")
async def serve_csv():
    return FileResponse(os.path.join(BASE_DIR, "Leetcode 100 questions - Start research.csv"))
