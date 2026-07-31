#!/bin/sh
# entrypoint.sh — runs inside the API container on every start.
# 1. Waits for PostgreSQL to accept connections (belt-and-suspenders on top of
#    the Compose healthcheck).
# 2. Applies any pending Alembic migrations.
# 3. Starts Uvicorn.

set -e

echo "==> Waiting for PostgreSQL..."
until pg_isready -h db -p 5432 -U "${POSTGRES_USER:-postgres}" > /dev/null 2>&1; do
  echo "    PostgreSQL not ready — sleeping 2s"
  sleep 2
done
echo "==> PostgreSQL is ready."

echo "==> Running Alembic migrations..."
alembic upgrade head

echo "==> Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
