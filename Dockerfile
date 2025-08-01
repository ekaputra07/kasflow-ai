FROM python:3.12-slim-bookworm

# Install UV
COPY --from=ghcr.io/astral-sh/uv:0.8.3 /uv /uvx /bin/

# Set working directory
WORKDIR /app

ARG uv_args=""

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_PROJECT_ENVIRONMENT="/app/.venv"
ENV PATH="/app/.venv/bin:$PATH"

# Copy UV lock file and project configuration
COPY uv.lock pyproject.toml alembic.ini ./

# Copy source code
COPY src/ ./src/

# Install only production dependencies using UV
RUN uv sync --frozen --no-dev --no-cache $uv_args

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

CMD ["kasflow"]