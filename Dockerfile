# 1. Base Python image
FROM python:3.13-slim

# 2. Environment variables set karein
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# 3. Install 'uv' for ultra-fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 4. Copy dependency files first (Docker caching layer)
COPY pyproject.toml uv.lock ./

# 5. Install dependencies without creating virtualenv inside container
RUN uv pip install --system --no-cache -r pyproject.toml

# 6. Copy application code
COPY . .

# 7. Expose default port
EXPOSE 8000

# 8. Start server using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]