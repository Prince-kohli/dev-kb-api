# Dev KB API - Agent Instructions

## Commands
- Run Server: `uv run fastapi dev app/main.py`
- Run Tests: `uv run pytest`
- Add Package: `uv add <package_name>`

## Tech Stack & Architecture Rules
- Framework: FastAPI with modern async routes
- Database ORM: SQLModel (Always use `datetime.now(timezone.utc)` for timestamps)
- Package Manager: `uv` (Never use `pip install` directly)
- Data Validation: Pydantic v2
- External Client: `httpx.AsyncClient`