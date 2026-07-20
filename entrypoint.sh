#!/bin/sh

su-exec fuser flask db upgrade

exec su-exec fuser gunicorn -b 0.0.0.0:5000 app.wsgi:app