from datetime import datetime
import logging

from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler

from addons.drone_hangar.models import AirBnBData
from addons.drone_hangar.scrapy.airbnb_spider import AirBnBSpider


class DroneHangarConfig(AppConfig):
    name = 'drone_hangar'

    # def ready(self):
        # super()
        
