from django.db.models.signals import post_syncdb
from django.conf import settings
from django.core import management

import os
import re

FIXTURE_RE = re.compile(r'^[^.]*.json$')

def load_data(sender, **kwargs):
    """
    Loads fixture data after loading the last installed app
    """
    if kwargs['app'].__name__ == settings.INSTALLED_APPS[-1] + ".models":
        fixture_files = []
        for loc in settings.INITIAL_FIXTURE_DIRS:
            loc = os.path.abspath(loc)
            if os.path.exists(loc):
                fixture_files += os.listdir(loc)
        fixture_files = filter(lambda v: FIXTURE_RE.match(v), fixture_files)
        fixture_files = [os.path.join(loc, f) for f in fixture_files]

        if len(fixture_files) > 0:
            print "Initializing Fixtures:"

            for fixture in fixture_files:
                print "  >> %s" % (fixture)
                management.call_command('loaddata', fixture, verbosity=0)

post_syncdb.connect(load_data)
