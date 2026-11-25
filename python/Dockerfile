# Define the base of your image.
# Always specify a tag; `latest` is not guaranteed to be reproducible.
FROM python:3.12-slim AS builder

# Install uv for fast, reliable Python package management.
# https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:0.5.21 /uv /uvx /bin/

# Use copy semantics for uv's cache, since it may live on a different filesystem.
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies before copying your code to maximize build cache reuse.
# No network access at runtime, so all dependencies must be installed here.
# Run `uv lock` locally to generate/update uv.lock before building.
COPY pyproject.toml uv.lock .
RUN uv sync --frozen --no-dev --no-cache

# Final image: only the app and its dependencies, without build tools like uv.
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv .venv

# Copy each file individually to take advantage of Docker's layer cache.
COPY run_model.py .

# Set the main command of the image.
# Use exec form so signals (e.g. timeouts) reach the process directly.
ENTRYPOINT [".venv/bin/python", "run_model.py"]
