import os.path


########################################
# DEBUG
########################################
DEV_MODE = True
DEBUG = True
TEMPLATE_DEBUG = DEBUG
LESS_DEBUG = DEBUG
COMPRESS_ENABLED = not DEBUG

SYNCRAE_VERSION_CHECK = True

# This cleans up the HTML, it should not be doing that...
# So its disabled for now
# We need it to NOT autoescape stuff in <script> tags
# basically it should just fix whitespace problems and indentation
PRETTIFY_HTML = False  # DEBUG


########################################
# Localization
########################################
# WEBDND_ROOT = '/apps/webdnd'
WEBDND_ROOT = os.path.dirname(__file__)
DATABASE_ROOT = WEBDND_ROOT

ADMINS = [
    # ('Name', 'email@webdnd.com'),
]

SECRET_KEY = '%(SECRET_KEY)s'
