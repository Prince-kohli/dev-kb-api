from fastapi import APIRouter
from app.api.v1.endpoints import bookmarks

api_router = APIRouter()
api_router.include_router(bookmarks.router, prefix="/bookmarks", tags=["Bookmarks"])