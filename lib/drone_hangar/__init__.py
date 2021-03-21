from .celery import app as celery_app

default_app_config = 'lib.drone_hangar.apps.DroneHangarConfig'

__all__ = ('celery_app', 'default_app_config')
