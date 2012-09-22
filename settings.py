# Django settings for webdnd project.
import os.path


########################################
# Testing
########################################

TEST_RUNNER = "tests.runner.DiscoveryRunner"

# location of the tests folder
BASE_PATH = os.path.dirname(__file__)
TEST_DISCOVERY_ROOT = os.path.join(BASE_PATH, "tests")

# Regexp pattern to match when looking for test files
# The runner will look in these files for TestCase classes
TEST_FILE_PATTERN = '*_test.py'

DEV_MODE = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG
COMPRESS_ENABLED = not DEBUG



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
    # 'webdnd.player',
    # 'webdnd.dnd',

    # Compression for static files
    'compressor',
    'django.contrib.staticfiles',

    # Alerts
    'webdnd.alerts',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/apps/webdnd/default.sqlite3',
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

# TODO: Prehaps we should get a cache?


##################################################
# Media and Static files
##################################################

# Absolute path to the directory that holds media.
MEDIA_ROOT = '/apps/webdnd/media/'
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
MEDIA_URL = '/media/'

# Absolute path to the directory that holds static files.
STATIC_ROOT = '/apps/webdnd/static/'
# URL that handles the static files served from STATIC_ROOT.
STATIC_URL = '/static/'
# A list of locations of additional static files
STATICFILES_DIRS = (
    ('shared', '/apps/webdnd/shared/static/'),
    ('alerts', '/apps/webdnd/alerts/static/',)
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
COMPRESS_ROOT = '/apps/webdnd/static'
COMPRESS_OUTPUT_DIR = '/compressed'
# COMPRESS_JS_FILTERS = ('compressor.filters.yui.YUIJSFilter',)
# COMPRESS_CSS_FILTERS = ('compressor.filters.yui.YUICSSFilter',)
# COMPRESS_PRECOMPILERS = (
#     # CSS Pre-compilers
#     ('text/css', 'cat {infile} > {outfile}'),
#     # ('text/less', 'lessc {infile} {outfile}'),

#     # JS Pre-Compilers
#     ('text/js', 'cat {infile} > {outfile}'),
#     # ('text/coffeescript', 'coffee --compile --stdio'),

#     # Some Examples
#     # ('text/x-sass', 'sass {infile} {outfile}'),
#     # ('text/x-scss', 'sass --scss {infile} {outfile}'),
#     # ('text/foobar', 'path.to.MyPrecompilerFilter'),
# )

# Locations of the template files
TEMPLATE_DIRS = (
    '/apps/webdnd/shared/templates',
    '/apps/webdnd/player/templates',
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
)



##################################################
# Login
##################################################

# How long cookies will last
SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_COOKIE_NAME = 'webdndID'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# TODO: make sure this works on a prod server
# I can't get it to work in dev :(
# SESSION_COOKIE_SECURE = True

# Default url to redirect to for login
LOGIN_URL = '/account/login'
LOGIN_REDIRECT_URL = '/'



##################################################
# Contact info and TZ
##################################################

# Site breakdowns
ADMINS = (
    # ('Dmitry Blotsky', 'dmitry.blotsky@gmail.com'),
)
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
# Misc
##################################################

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '1t2h3i4s5i6s7a8v9e0rysecretkeybecauseitisv0e9r8y7s6e5c4r3e2t1'



MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'alerts.middleware.AlertMiddleware',
)


# Alerts
from webdnd.alerts.settings import *


