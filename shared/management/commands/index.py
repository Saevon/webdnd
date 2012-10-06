from django.core.management.base import BaseCommand
from django.conf import settings

from webdnd.player.views.index import UserIndex
from optparse import make_option

class Command(BaseCommand):
    help = 'Creates with the search index'

    option_list = BaseCommand.option_list + (
        make_option('--flush',
            action='store_true',
            dest='flush',
            default=False,
            help='Remake the index from scratch'
        ),
        make_option('--index',
            action='append',
            default=['all'],
            dest='indicies',
            help='Specify which index to refresh'
        ),
    )

    INDICIES = {
        'users': {'class': UserIndex, 'dir': settings.USER_INDEX_DIR},
    }

    def handle(self, *args, **options):
        self.flush = options['flush']

        if 'all' in options['indicies']:
            for index in self.INDICIES.values():
                self.index(index)
        else:
            for index in options['indicies']:
                if index in self.INDICIES:
                    self.index(self.INDICIES[index])

    def index(self, index):
        index = index['class'].get(index['dir'])
        index.create_schema(flush=self.flush)


