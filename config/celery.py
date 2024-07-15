from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Tashkent')

app.config_from_object(settings, namespace='CELERY') 

# Celery Beat Settings
app.conf.beat_schedule = {
    # 'send-email-every-day-at-8': {
    #     'task': 'email_sender.tasks.send_email',
    #     'schedule': crontab(hour=8, munute=0),
    #     # 'args': (),
    # }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: { self.request!r }')
