# Use official Python image with Node.js pre-installed
FROM mcr.microsoft.com/devcontainers/python:3.11-bullseye

# Install Node.js 18 LTS
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y postgresql-client

# Install Python development tools
RUN pip install --upgrade pip setuptools wheel

# Set working directory
WORKDIR /workspace

# Copy and install Python dependencies
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install additional development tools
RUN pip install black pylint pytest ipython

# Set up non-root user (vscode user is created by base image)
USER vscode

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    NODE_ENV=development
