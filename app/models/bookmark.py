from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional

def get_utc_now() -> datetime:
    """Returns timezone-aware UTC datetime (Python 3.12+ compliant)"""
    return datetime.now(timezone.utc)

# --- Base Schema ---
class BookmarkBase(SQLModel):
    url: str = Field(index=True)
    title: Optional[str] = None
    notes: Optional[str] = None
    tags: str = Field(default="")

# --- Database Table Model ---
class Bookmark(BookmarkBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    is_github: bool = Field(default=False)
    github_stars: int = Field(default=0)
    github_language: Optional[str] = None
    github_description: Optional[str] = None
    github_open_issues: int = Field(default=0)
    
    # Timezone-aware UTC datetimes
    created_at: datetime = Field(default_factory=get_utc_now)
    updated_at: datetime = Field(default_factory=get_utc_now)

# --- DTOs ---
class BookmarkCreate(BookmarkBase):
    pass

class BookmarkUpdate(SQLModel):
    title: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[str] = None

class BookmarkResponse(BookmarkBase):
    id: int
    is_github: bool
    github_stars: int
    github_language: Optional[str]
    github_description: Optional[str]
    github_open_issues: int
    created_at: datetime