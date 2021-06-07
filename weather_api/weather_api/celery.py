from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, shared_task

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_api.settings')

app = Celery('weather_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.beat_schedule = {
    'send-mail-every-30-mins': {
        'task': 'email_weather',
        'schedule': 1800.0,
    }
}
