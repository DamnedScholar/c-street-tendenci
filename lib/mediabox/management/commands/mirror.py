import logging; logger = logging.getLogger('Mediabox')

from django.core.management.base import BaseCommand, CommandError

from lib.mediabox.core import mediabox

class Command(BaseCommand):
    help = 'Mirrors the Dropbox to the local server.'

    def handle(self, *args, **options):
        return mediabox.mirror()
