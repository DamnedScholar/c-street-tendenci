from datetime import datetime
import logging

from django.apps import AppConfig


class DroneHangarConfig(AppConfig):
    name = 'lib.drone_hangar'

    def ready(self):
        # TODO: Define model signals here. This will be relevant when we get to consistently updating the stored values and want to hook off of them.
        super()
        
