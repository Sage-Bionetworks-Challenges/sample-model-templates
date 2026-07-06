# Define the base of your image.
# We recommend to always specify a tag. `latest` may not 
# always ensure reproducibility.
FROM python:3.12-slim

# Install uv for fast, reliable Python package management.
# https://docs.astral.sh/uv/guides/integration/docker/
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# For best practice, run container as non-root user.
RUN groupadd -r user && useradd -m --no-log-init -r -g user user
USER user

# Set the working directory for the COPY, RUN, and ENTRYPOINT
# commands of the Dockerfile.
WORKDIR /home/user

# Copy files over to the image.
# We recommend copying over each file individually, as to take
# advantage of cache building (which helps reduce build time).
COPY --chown=user:user pyproject.toml .

# Install needed libraries/packages.
# Your model will be run without network access, so the dependencies
# must be installed here (and not during code execution).

# Tip: run `uv lock` locally to generate a uv.lock file, then copy it
# here alongside pyproject.toml and add --frozen for reproducible builds.
RUN uv sync --no-dev --no-cache

COPY --chown=user:user run_model.py .

# Set the main command of the image.
# We recommend using this form instead of `ENTRYPOINT command param1`.
ENTRYPOINT ["uv", "run", "python", "run_model.py"]
