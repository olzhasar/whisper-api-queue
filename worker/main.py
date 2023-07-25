import tasks  # noqa
from celery_app import app

app.autodiscover_tasks()
