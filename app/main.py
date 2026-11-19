from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.db import init_db
from app.api.v1.router import api_router

# 1. Database Initialization Logic (Startup Event)
# Isse hi hamari 'dev_kb.db' (SQLite file) auto-create hogi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    print("🚀 Initializing Database...")
    init_db()
    yield
    # Shutdown logic (agar kuch ho to yahan aayega)
    print("🔌 Shutting down...")

# 2. FastAPI Instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A smart Developer Knowledge Base API with GitHub integration.",
    lifespan=lifespan
)

# 3. Routes mapping (Like app.use('/api/v1', router))
app.include_router(api_router, prefix="/api/v1")

# 4. Root Health Check
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "online",
        "database": "connected (SQLite)",
        "project": settings.PROJECT_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)