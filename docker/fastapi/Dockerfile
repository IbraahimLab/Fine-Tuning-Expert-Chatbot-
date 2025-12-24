# # docker/fastapi/Dockerfile

# FROM python:3.11-slim

# # Prevent Python from writing pyc files
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# WORKDIR /app

# # System deps (minimal)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Copy dependency files first (better caching)
# COPY pyproject.toml uv.lock ./

# # Install uv
# RUN pip install --no-cache-dir uv

# # Install dependencies
# RUN uv sync --frozen

# # Copy application code
# COPY app ./app

# # Expose FastAPI port
# EXPOSE 8000

# # Start FastAPI

# # Install deps with uv

# # Start app
# CMD ["python", "-m", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]



# docker/fastapi/Dockerfile
FROM python:3.11-slim

# Basic Python hygiene
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Tell uv to install dependencies into a local venv
ENV UV_PROJECT_ENV=/app/.venv

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency metadata first (for caching)
COPY pyproject.toml uv.lock ./

# Install uv
RUN pip install --no-cache-dir uv

# Install Python dependencies into .venv
RUN uv sync --frozen

# Make sure Python uses the uv-managed venv
ENV PATH="/app/.venv/bin:$PATH"

# Copy application code
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["python", "-m", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
