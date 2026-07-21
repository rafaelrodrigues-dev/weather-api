#!/bin/sh
set -e

su-exec fuser flask db upgrade --directory /app/src/weather_api/migrations

PYTHONPATH=/app/src su-exec fuser python -c "import telemetry; telemetry.start_telemetry()"

exec su-exec fuser gunicorn \
    -b 0.0.0.0:5000 \
    --workers 2 \
    --timeout 30 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    app.wsgi:app