from django.core.management.base import BaseCommand

from optparse import make_option
import subprocess
from random import choice
import string

class Command(BaseCommand):
    '''
    Copies over the local_settings file.
    '''

    def handle(self, *args, **options):
        print 'Copying template file'
        subprocess.call(['cp', 'shared/config/settings_tmpl.py', 'local_settings.py'])

        print 'Generating secret key'
        values = {
            'SECRET_KEY': ''.join([choice(string.hexdigits) for i in range(50)])
        }

        print 'Rendering Template'
        with open('local_settings.py', 'r') as in_file:
            tmpl = in_file.read()
        with open('local_settings.py', 'w') as out_file:
            out_file.write(tmpl % values)
