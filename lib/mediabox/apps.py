from django.apps import AppConfig
from django.db.models.signals import pre_save

class MediaboxConfig(AppConfig):
    name = 'lib.mediabox'
    
    def ready(self):
        # This is necessary to initialize the Mediabox object before you try to interact with it.
        from .core import mediabox
