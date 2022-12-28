#!/bin/sh

# run migrations
venv3/bin/alembic upgrade head

# run worker
venv3/bin/celery -A app.tasks worker --loglevel=DEBUG
