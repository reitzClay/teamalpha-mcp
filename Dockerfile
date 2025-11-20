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

# Install dependencies from uv.lock, skipping development packages.
RUN uv sync --locked --no-dev

# Set the default command to run the crew
CMD ["python", "crew.py"]
