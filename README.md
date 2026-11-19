# 🚀 Dev KB & Bookmark Engine (No-AI REST Service)

A production-ready Developer Knowledge Base backend service built with Python, FastAPI, SQLModel, and Pydantic v2.

---

## 🛠️ Features
- **Bookmark Management (CRUD)**: Save and organize developer code links and tech notes.
- **Async External API Integration**: Automatically detects GitHub URLs and asynchronously fetches repository metadata (Stars, Language, Open Issues, Description) using `httpx`.
- **Search & Filtering**: Filter bookmarks by programming language, tags, or pagination limits.
- **Analytics Engine**: `GET /api/v1/bookmarks/stats` aggregating total bookmarks and combined stars.
- **Automated Tests**: Unit & Integration tests using `pytest` and `TestClient`.

---

## 🏗️ Architecture

dev-kb-api/
├── app/
│ ├── api/v1/ # Route controllers and endpoints
│ ├── core/ # Configuration (pydantic-settings) & DB engine
│ ├── models/ # SQLModel table definitions & Pydantic schemas
│ ├── services/ # External GitHub API async fetcher (httpx)
│ └── main.py # FastAPI application & Lifespan init
├── tests/ # Pytest automated test suite
├── Dockerfile # Production container build
└── pyproject.toml # Modern uv package manager configuration


---

## ⚡ Quickstart

### 1. Prerequisites
- Python 3.10+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### 2. Setup & Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd dev-kb-api

# Install dependencies with uv
uv sync

# Run the development server
uv run fastapi dev app/main.py