#!/bin/sh

# db migrations

venv3/bin/celery -A app.tasks worker --loglevel=DEBUG
