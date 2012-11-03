##################################################
# Wrapper around the config files
##################################################
import sys
import os
os.chdir(os.path.dirname(__file__))


# Version comparison function
def version(ver):
    '''
    Return the major and minor version numbers
    '''
    return '.'.join(ver.split('.'[:2]))

# Localize doesn't need settings (it sets them up)
# So no actual settings imports
if 'localize' in sys.argv:
    INSTALLED_APPS = (
        # Location of the localize command
        'webdnd.shared'
    )
else:
    # General setting file
    from shared.config.settings_main import *

    # Alerts
    from alerts.settings import *

    # Syncrae
    from syncrae.config.settings import *


    # make sure you're using matching versions
    if SYNCRAE_VERSION_CHECK and version(VERSION) != version(SYNCRAE_VERSION):
        raise AssertionError('Invalid Syncrae Version: %s', SYNCRAE_VERSION)

