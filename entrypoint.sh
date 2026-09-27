#!/bin/sh
set -e

# Run alembic migrations before starting application
echo "Running database migrations..."
alembic upgrade head

exec "$@"
