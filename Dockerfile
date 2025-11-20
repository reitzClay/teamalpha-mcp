# Use the official Python image
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy all project files into the container.
COPY . .

# Configure uv to use the container's main python environment
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

# Install dependencies from uv.lock if present; fall back to `uv sync --no-dev` when lock mismatch
RUN if [ -f uv.lock ]; then uv sync --locked --no-dev || uv sync --no-dev; else uv sync --no-dev; fi

# Run the FastAPI app with uvicorn on container start
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
