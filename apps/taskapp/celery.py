from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from dotenv import load_dotenv


load_dotenv()  # loads the configs from .env


ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')


os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{ENVIRONMENT}')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
