# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (minimal for Python MCP server)
RUN apt-get update && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1000 mcpuser
RUN chown -R mcpuser:mcpuser /app
USER mcpuser

# MCP servers typically use stdio communication, not HTTP
# Remove port exposure and health check for stdio-based MCP server

# Default command to run the MCP server
# Keep container running for MCP stdio communication
CMD ["python", "homegenie_mcp_server.py"]