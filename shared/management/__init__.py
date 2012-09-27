from django.db.models.signals import post_syncdb
from django.conf import settings

def load_data(sender, **kwargs):
    """
    Loads fixture data after loading the last installed app
    """
    if kwargs['app'].__name__ == settings.INSTALLED_APPS[-1] + ".models":
        pass
        # load fixtures here

post_syncdb.connect(load_data)