FROM python:3.9-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for development
RUN useradd -m -s /bin/bash dev
USER dev

# Python packages will be installed via pip in postCreateCommand
