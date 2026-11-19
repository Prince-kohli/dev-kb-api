from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from typing import List, Optional

from app.core.db import get_session
from app.models.bookmark import Bookmark, BookmarkCreate, BookmarkResponse, BookmarkUpdate
from app.services.github import github_service

router = APIRouter()

# 1. CREATE BOOKMARK
@router.post("/", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
async def create_bookmark(payload: BookmarkCreate, session: Session = Depends(get_session)):
    # Convert Pydantic input to DB model
    bookmark = Bookmark.model_validate(payload)
    
    # Check agar URL GitHub repo ka hai to GitHub API se details fetch karo
    if "github.com" in payload.url:
        github_data = await github_service.get_repo_details(payload.url)
        if github_data:
            bookmark.is_github = True
            bookmark.github_stars = github_data["github_stars"]
            bookmark.github_language = github_data["github_language"]
            bookmark.github_description = github_data["github_description"]
            bookmark.github_open_issues = github_data["github_open_issues"]
            if not bookmark.title:
                bookmark.title = payload.url.rstrip("/").split("/")[-1]

    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)
    return bookmark

# 2. GET ALL BOOKMARKS (With Filtering & Pagination)
@router.get("/", response_model=List[BookmarkResponse])
def get_bookmarks(
    session: Session = Depends(get_session),
    tag: Optional[str] = Query(None, description="Filter by tag keyword"),
    language: Optional[str] = Query(None, description="Filter by programming language"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    query = select(Bookmark)
    
    if tag:
        query = query.where(Bookmark.tags.contains(tag))
    if language:
        query = query.where(Bookmark.github_language.ilike(f"%{language}%"))
        
    query = query.offset(offset).limit(limit)
    return session.exec(query).all()

# 3. GET STATS / ANALYTICS (Capstone Requirement)
@router.get("/stats")
def get_stats(session: Session = Depends(get_session)):
    total_bookmarks = session.exec(select(func.count(Bookmark.id))).one()
    github_repos = session.exec(select(func.count(Bookmark.id)).where(Bookmark.is_github == True)).one()
    total_stars = session.exec(select(func.sum(Bookmark.github_stars))).one() or 0
    
    return {
        "total_bookmarks": total_bookmarks,
        "github_repos_count": github_repos,
        "total_github_stars": total_stars
    }

# 4. GET BOOKMARK BY ID
@router.get("/{bookmark_id}", response_model=BookmarkResponse)
def get_bookmark(bookmark_id: int, session: Session = Depends(get_session)):
    bookmark = session.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark

# 5. DELETE BOOKMARK
@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(bookmark_id: int, session: Session = Depends(get_session)):
    bookmark = session.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    session.delete(bookmark)
    session.commit()
    return None