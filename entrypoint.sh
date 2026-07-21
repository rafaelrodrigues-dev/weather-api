#!/bin/sh

su-exec fuser flask db upgrade

su-exec fuser python -c "import telemetry; telemetry.start_telemetry()"

exec su-exec fuser gunicorn -b 0.0.0.0:5000 app.wsgi:app