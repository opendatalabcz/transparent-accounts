import os

from celery.schedules import crontab


class Config:
    broker_url = os.getenv('CELERY_BROKER_URL')
    timezone = os.getenv('TZ')
    # Schedule for fetching accounts
    # The place for adding new banks to be scheduled
    beat_schedule = {
        'fetch-csac-accounts-every-day': {
            'task': 'app.tasks.fetch_accounts',
            'schedule': crontab(hour=3, minute=0),
            'args': ['0800']
        },
        'fetch-fio-accounts-every-day': {
            'task': 'app.tasks.fetch_accounts',
            'schedule': crontab(hour=3, minute=0),
            'args': ['2010']
        },
        'fetch-kb-accounts-every-day': {
            'task': 'app.tasks.fetch_accounts',
            'schedule': crontab(hour=3, minute=0),
            'args': ['0100']
        }
    }
