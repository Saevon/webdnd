from django.core.management.base import BaseCommand
from django.conf import settings

from optparse import make_option
from webdnd.player.models.alignments import Alignment

class Command(BaseCommand):
    help = 'Clears useless alignments'

    def handle(self, *args, **options):
        objs = Alignment.objects.filter(owner=None)
        objs.delete()
