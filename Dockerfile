# Multi-stage production Dockerfile using uv and Python 3.13
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Enable bytecode compilation and optimize uv caching
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies without copying the entire project first (layer caching)
COPY pyproject.toml uv.lock* README.md ./
RUN uv sync --frozen --no-install-project --no-dev || uv sync --no-install-project --no-dev

# Copy source code and data files
COPY src/ ./src/
COPY data/ ./data/

# Install the project itself into the virtual environment
RUN uv sync --frozen --no-dev || uv sync --no-dev

# Final runtime image
FROM python:3.13-slim AS runner

# Create a non-root user and group
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy the pre-built virtual environment and application files from builder
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/data /app/data
COPY --from=builder /app/README.md /app/README.md

# Set ownership to non-root user
RUN chown -R appuser:appgroup /app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOST=0.0.0.0 \
    PORT=8000 \
    ENVIRONMENT=production

USER appuser

EXPOSE 8000

# Health check using python urllib
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

# Start the MCP server using python module runner
CMD ["python", "-m", "src.server"]
