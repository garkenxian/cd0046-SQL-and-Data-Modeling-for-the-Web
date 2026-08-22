FROM python:3.9-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    git \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user for development
RUN useradd -m -s /bin/bash dev
USER dev
