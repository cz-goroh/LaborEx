import os
import django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LaborEx.settings')
django.setup()

app = Celery('LaborEx', broker='redis://127.0.0.1:6379/0')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
