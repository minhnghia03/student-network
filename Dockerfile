FROM python:3.12-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install UV
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# First copy requirements files
COPY pyproject.toml uv.lock ./

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
RUN uv pip install --upgrade pip && \
    uv sync && \
    uv pip install -e .

# Copy application code
COPY ./src .env  ./

EXPOSE 5000

CMD ["uv", "run", "src/student_network/app.py"]