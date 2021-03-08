from django.core.management.base import BaseCommand, CommandError
from lib.drone_hangar.dropbox.minutes import merge_minutes

class Command(BaseCommand):
    help = 'Compile CID minutes'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            merge_minutes()
        except BaseException as e:
            raise CommandError("> > > Couldn't compile minutes. %s" % e)
