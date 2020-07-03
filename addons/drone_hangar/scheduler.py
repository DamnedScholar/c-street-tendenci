import json
from datetime import datetime
import logging

import pytz

from apscheduler.schedulers.background import BackgroundScheduler

from addons.drone_hangar.models import AirBnBData
from addons.drone_hangar.scrapy.airbnb_spider import AirBnBSpider


def summon_airbnb_spider():
    spider = AirBnBSpider()

    if spider.check_age():
        logging.warning("> > > Starting request.")
        spider.start_requests()
    else:
        pass

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
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone="utc")

    return scheduler

def scheduler(command_list):
    scheduler = init_scheduler()

    jobs = {
        "airbnb": {
            "func": summon_airbnb_spider,
            "trigger": None,
            "args": None,
            "kwargs": None,
            "id": None,
            "name": None,
            "misfire_grace_time": 30,
            "coalesce": True,
            "max_instances": 1,
            # "next_run_time": datetime.now(pytz.timezone("America/Chicago")),
            "jobstore": 'default',
            "executor": 'default',
            "replace_existing": False
        }
    }

    logging.warning("> > > Working on jobs.")

    command_list = command_list.split(sep=" ")

    for command, job in jobs.items():
        if [value for value in [command, "all"] if value in command_list]:
            func = job.pop('func')

            logging.warning('> > > Adding job with predefined properties')
            scheduler.add_job(func, **job)

    scheduler.start()
