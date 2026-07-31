# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies:
#   libpq-dev  — required by psycopg (C extension)
#   gcc        — compiler for C extensions
#   postgresql-client — provides pg_isready used in entrypoint.sh
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       gcc \
       postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first (layer-cache friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Make the entrypoint script executable
RUN chmod +x entrypoint.sh

# Expose the FastAPI port
EXPOSE 8000

# Run migrations then start Uvicorn
ENTRYPOINT ["./entrypoint.sh"]
