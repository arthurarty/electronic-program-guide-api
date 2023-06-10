import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_grab.settings')
app = Celery("web_grab")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
