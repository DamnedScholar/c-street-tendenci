from django.core.management.base import BaseCommand, CommandError
from scrapy.crawler import Crawler
from scrapy.signalmanager import SignalManager
from addons.drone_hangar.scrapy.airbnb_spider import AirBnBSpider

class Command(BaseCommand):
    help = 'Scrape a website.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            spider = Crawler(AirBnBSpider)
            spider.crawl()
        except BaseException as e:
            raise CommandError("> > > The spider died. %s" % e)
