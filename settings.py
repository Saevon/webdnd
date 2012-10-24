# Django settings for webdnd project.
import os.path
import re

########################################
# Local Settings
########################################
# The local settings file needs to exist, and have defined certain
# settings before this project will work
try:
    from local_settings import *
except ImportError:
    import sys
    if 'localize' not in sys.argv:
        raise AssertionError("Local settings file not defined")
    else:
        # use the template so that localize can still work
        from shared.config.settings_tmpl import *

########################################
# Testing
########################################

TEST_RUNNER = "tests.runner.DiscoveryRunner"

# location of the tests folder
BASE_PATH = WEBDND_ROOT
TEST_DISCOVERY_ROOT = os.path.join(WEBDND_ROOT, "tests")

# Regexp pattern to match when looking for test files
# The runner will look in these files for TestCase classes
TEST_FILE_PATTERN = '*_test.py'


# format: 'major.minor.bug name'
VERSION = '0.2.0 BETA'


##################################################
# App settings
##################################################

ROOT_URLCONF = 'webdnd.urls'

INSTALLED_APPS = (
    # User login and authentication
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'django.contrib.sites',
    'django.contrib.messages',

    # Django Admin
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # Webdnd apps
    'webdnd.player',
    # 'webdnd.dnd',
    'webdnd.shared',

    # Compression for static files
    'compressor',
    'django.contrib.staticfiles',

    # Syncrae: Tornado websockets app
    'webdnd.syncrae',

    # Alerts
    'webdnd.alerts',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_ROOT, 'webdnd.sqlite3'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

# CharField
STND_CHAR_LIMIT = 100
STND_ID_CHAR_LIMIT = 5
ADMIN_CHAR_CUTOFF = 20

#DecimalField
STND_DECIMAL_PLACES = 3

# Fixtures
INITIAL_FIXTURE_DIRS = (
    'player/fixtures',
)

# TODO: Prehaps we should get a cache?


##################################################
# Media and Static files
##################################################

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(WEBDND_ROOT, 'media/')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
STATIC_ROOT = os.path.join(WEBDND_ROOT, 'static/')
# URL that handles the static files served from STATIC_ROOT.
STATIC_URL = '/static/'
# A list of locations of additional static files
STATICFILES_DIRS = (
    ('shared', os.path.join(WEBDND_ROOT, 'shared/static/')),
    ('alerts', os.path.join(WEBDND_ROOT, 'alerts/static/')),
    ('player', os.path.join(WEBDND_ROOT, 'player/static/')),
    ('syncrae', os.path.join(WEBDND_ROOT, 'syncrae/static/')),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# Parse to use for static file compression
COMPRESS_PARSER = 'compressor.parser.BeautifulSoupParser'
# Location of the static files
COMPRESS_ROOT = os.path.join(WEBDND_ROOT, 'static/')
COMPRESS_OUTPUT_DIR = '/compressed'
# COMPRESS_JS_FILTERS = ('compressor.filters.yui.YUIJSFilter',)
# COMPRESS_CSS_FILTERS = ('compressor.filters.yui.YUICSSFilter',)

COMPRESS_PRECOMPILERS = (
    # CSS Pre-compilers
    ('text/less', 'lessc {infile} {outfile} --verbose'
        # Prevent bad debug messages, e.g. [31m that form colors
        + (' --no-color' if DEBUG else '')
        # Compress output on Prod
        + ('' if DEBUG else ' -x')
        # Show line numbers in compiled code as comments
        + (' --line-numbers="comments"' if LESS_DEBUG else '')
    ),

    # JS Pre-Compilers
    # ('text/x-handlebars-template',
    #     'handlebars {infile} --output {outfile}'
        # Minimize compiled template in production
    #     + (' --min' if DEBUG else '')
    # ),


    # e.g. using classes
    # ('text/foobar', 'path.to.MyPrecompilerFilter'),
    # e.g.
    # ('text/coffeescript', 'coffee --compile --stdio'),
)


# Locations of the template files
TEMPLATE_DIRS = (
    os.path.join(WEBDND_ROOT, 'shared/templates'),
    os.path.join(WEBDND_ROOT, 'player/templates'),
)
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)
# Functions which add onto the context before rendering a template
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",

    # alerts plugin
    "alerts.alert.template_processor",
    "alerts.highlighter.template_processor",
)



##################################################
# Login
##################################################

# How long cookies will last
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_COOKIE_NAME = 'webdndID'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Default url to redirect to for login
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/'


##################################################
# Contact info and TZ
##################################################

# Site breakdowns
ADMINS = ADMINS.extend([
    # ('Dmitry Blotsky', 'dmitry.blotsky@gmail.com'),
])
# Broken links
MANAGERS = ADMINS
# email server emails are sent from
SERVER_EMAIL = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Canada/Eastern'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-ca'
LANGUAGE_COOKIE_NAME = 'webdnd-language'



##################################################
# Logging
##################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s - %(message)s - %(module)s@%(funcName)s %(lineno)s - %(process)d %(thread)d',
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s - %(message)s - %(module)s@%(funcName)s %(lineno)s',
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
    },
    'filters': {

    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'webdnd.syncrae.config.log.ColorizingStreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        # Root logger that colors output
        # Any other loggers should have propagate False if they output
        # to the console to prevent duplicated console messages
        '': {
            'handlers': ['console'],
            'propagate': False,
            'level': 'INFO',
        },
        # Built-in Django loggers
        # 'django': {

        # },
        # 'django.request': {
        #     'handlers': ['console'],
        #     'level': 'ERROR' if not DEBUG else 'INFO',
        #     'propagate': False,
        # },
        # 'django.db.backends': {

        # },
    }
}



##################################################
# Misc
##################################################

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True


MIDDLEWARE_CLASSES = (
    'shared.middleware.HtmlPrettifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'alerts.middleware.AlertMiddleware',
    'alerts.middleware.FieldHighlightMiddleware',
)

INDEX_DIR = os.path.join(WEBDND_ROOT, 'index/')
USER_INDEX_DIR = os.path.join(INDEX_DIR, 'user/')

# Characters that a user can't search for
USER_CHAR_RE = re.compile(r'[^.@-_a-zA-Z0-9]*')



##################################################
# Installed apps settings
##################################################
def version(ver):
    '''
    Return the major and minor version numbers
    '''
    return '.'.join(ver.split('.'[:2]))


# Alerts
from alerts.settings import *


# Syncrae
from syncrae.config.settings import *

# make sure you're using matching versions
if SYNCRAE_VERSION_CHECK and version(VERSION) != version(SYNCRAE_VERSION):
    raise AssertionError('Invalid Syncrae Version: %s', SYNCRAE_VERSION)




