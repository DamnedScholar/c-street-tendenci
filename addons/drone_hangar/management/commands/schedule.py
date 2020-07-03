from django.core.management.base import BaseCommand, CommandError
from addons.drone_hangar.scheduler import scheduler

class Command(BaseCommand):
    help = 'Schedule persistent tasks.'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        try:
            # TODO: Make scheduler configurable.
            scheduler("airbnb")
        except BaseException as e:
            raise CommandError("> > > The scheduler isn't running. %s" % e)
