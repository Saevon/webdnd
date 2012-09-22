from django.core.management.base import BaseCommand

from optparse import make_option
from webdnd.alerts.models import Alert
import datetime

class Command(BaseCommand):
    '''
    Removes expired tokens
    '''

    option_list = BaseCommand.option_list + (
        make_option('-F', '--flush',
            default=False,
            action='store_true',
            dest='flush',
            help='Deletes all tokens'),
        )

    def handle(self, *args, **options):
        if options['flush']:
            alerts = Alert.objects.all()
        else:
            alerts = Alert.objects.filter(expiry__lte=datetime.datetime.now())

        deleted = len(alerts)
        alerts.delete()
        print '%s alert%s deleted.' % (deleted, 's' if deleted != 1 else '')