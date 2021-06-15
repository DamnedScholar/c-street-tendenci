import logging; logger = logging.getLogger('Mediabox')

from django.core.management.base import BaseCommand, CommandError

from lib.mediabox.wagtail import media_walk

class Command(BaseCommand):
    help = 'Walks the Mediabox filesystem to generate a tree of Wagtail collections and tries to import each file into a Wagtail model.'

    def handle(self, *args, **options):
        return media_walk()
        # except Exception as e:
        #     logger.warn(f"We broke it. Here's what went wrong:")
        #     logger.warn(e)
