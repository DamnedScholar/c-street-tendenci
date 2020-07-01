from datetime import datetime
import logging

from django.apps import AppConfig

from apscheduler.schedulers.background import BackgroundScheduler

from addons.drone_hangar.models import AirBnBData
from addons.drone_hangar.scrapy.airbnb_spider import AirBnBSpider


def init_scheduler():
    jobstores = {}
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

    return scheduler

def summon_airbnb_spider():
    spider = AirBnBSpider()

    if spider.check_age():
        spider.start_requests()
    else:
        pass

class DroneHangarConfig(AppConfig):
    name = 'drone_hangar'

    def ready(self):
        super()
        scheduler = init_scheduler()

        jobs = [
            {
                "func": summon_airbnb_spider,
                "trigger": None,
                "args": None,
                "kwargs": None,
                "id": None,
                "name": None,
                "misfire_grace_time": 30,
                "coalesce": True,
                "max_instances": 1,
                "next_run_time": datetime.now(),
                "jobstore": 'default',
                "executor": 'default',
                "replace_existing": False
            },
        ]

        with open('addons/drone_hangar/testing.txt', 'w') as f:
            f.write("Working on jobs.")

        for job in jobs:
            func = job.pop('func')

            logging.debug('> > > Adding job with properties {}' % job.to_str())
            scheduler.add_job(func, {job})
