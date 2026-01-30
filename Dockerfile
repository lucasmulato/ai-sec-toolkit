# STAGE 1: Builder (Compiling dependencies)
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies (removed in final image)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment for isolation
python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# STAGE 2: Runner (Production Runtime)
FROM python:3.11-slim as runner

# Security: Create a non-root user
RUN groupadd -r artt_group && useradd -r -g artt_group -d /app -s /sbin/nologin artt_user

WORKDIR /app

# Copy virtual env from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Runtime basics (curl for healthchecks)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy Application Code
COPY . .

# Create directory for SQLite DB/logs and set permissions
RUN mkdir -p backups logs && \
    chown -R artt_user:artt_group /app

# Switch to non-root user
USER artt_user

# Environment Variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ARTT_ENV=production

# Expose the MCP port (default usually 8000 or configurable)
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint
CMD ["fastmcp", "run", "mcp_server/server.py", "--host", "0.0.0.0", "--port", "8000"]
