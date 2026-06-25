import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Carshering.settings')

app = Celery('Carshering')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'update-rent-status-every-hour': {
        'task': 'carservice.tasks.update_rent_statuses',
        'schedule': crontab(minute=0),  # Run every hour
    },
    'cleanup-expired-sessions': {
        'task': 'carservice.tasks.cleanup_expired_sessions',
        'schedule': crontab(hour=3, minute=0),  # Run daily at 3 AM
    },
}

app.conf.timezone = 'Europe/Warsaw'


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Made with Bob
