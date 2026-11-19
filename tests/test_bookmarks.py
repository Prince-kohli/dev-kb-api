import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.db import get_session

# Test ke liye in-memory isolated database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    # FastAPI Dependency Injection Override (Mock DB for tests)
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# --- Test Cases ---

def test_health_check(client: TestClient):
    """Test health endpoint returns 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_create_and_get_bookmark(client: TestClient):
    """Test creating a bookmark and fetching it"""
    # 1. Create Bookmark
    payload = {
        "url": "https://fastapi.tiangolo.com",
        "title": "FastAPI Official Documentation",
        "notes": "Best Python REST framework",
        "tags": "python,docs,api"
    }
    response = client.post("/api/v1/bookmarks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["url"] == payload["url"]
    assert data["id"] is not None

    bookmark_id = data["id"]

    # 2. Get By ID
    get_res = client.get(f"/api/v1/bookmarks/{bookmark_id}")
    assert get_res.status_code == 200
    assert get_res.json()["title"] == payload["title"]


def test_bookmark_stats(client: TestClient):
    """Test stats aggregation endpoint"""
    # Create sample item
    client.post("/api/v1/bookmarks/", json={"url": "https://example.com", "tags": "test"})
    
    response = client.get("/api/v1/bookmarks/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_bookmarks"] >= 1