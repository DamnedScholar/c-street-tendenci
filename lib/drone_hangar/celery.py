import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')

rabbit = {
    'user': os.environ.get('RABBITMQ_USER', default='guest'),
    'password': os.environ.get('RABBITMQ_PASSWORD', default='guest'),
    'vhost': os.environ.get('RABBITMQ_VHOST', default='/'),
}

app = Celery(
    'c-street',
    backend='rpc://',
    broker=f'amqp://{rabbit["user"]}:{rabbit["password"]}@localhost:5672{rabbit["vhost"]}'
    )

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
