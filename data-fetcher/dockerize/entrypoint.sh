#!/bin/sh

# Run migrations
venv3/bin/alembic upgrade head

# Run scheduler
venv3/bin/celery -A app.tasks beat --loglevel=INFO &

# Run worker
venv3/bin/celery -A app.tasks worker --loglevel=INFO
