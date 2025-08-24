FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1001 appuser

# Copy project files with correct ownership
COPY --chown=appuser:appuser pyproject.toml ./
COPY --chown=appuser:appuser app/ ./app/
COPY --chown=appuser:appuser agents/ ./agents/

# Switch to non-root user
USER appuser

# Install dependencies using UV with Python 3.11
RUN uv pip install --python python3.11 --user .

# Add user's local bin to PATH
ENV PATH="/home/appuser/.local/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]