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
WEBDND_ROOT = os.getcwd()
DATABASE_ROOT = WEBDND_ROOT

ADMINS = [
    # ('Name', 'email@webdnd.com'),
]

SECRET_KEY = '%(SECRET_KEY)s'


########################################
# Debug Toolbar Customization
########################################

# Order of enabled toolbar panels
DEBUG_TOOLBAR_PANELS = (
    'webdnd.shared.utils.debug_toolbars.DividerDebugPanel',
    # --

    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',

    # --
    'webdnd.shared.utils.debug_toolbars.DividerDebugPanel',
    # --

    'webdnd.shared.utils.debug_toolbars.SyncraeSpyDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',

    # --
    'webdnd.shared.utils.debug_toolbars.DividerDebugPanel',
    # --

    'debug_toolbar.panels.timer.TimerDebugPanel',
    'webdnd.shared.utils.debug_toolbars.VersionDebugPanel',
)

# Allowed IPS that will see the debug toolbar
# Only works if the original show_toolbar function is used (None)
INTERNAL_IPS = (
    '127.0.0.1',
    'localhost',
)
# Required to get debug toolbar to work
DATABASE_ENGINE = 'django.db.backends.sqlite3'

# Creates a function that checks when to show the debug toolbar
show_toolbar = None
# def show_toolba():
#     return DEBUG

DEBUG_TOOLBAR_CONFIG = {
    # Shows an Intermidiate page upon redirect to debug
    # variables
    'INTERCEPT_REDIRECTS': True,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    # Don't show django code in SQL backtraces
    'HIDE_DJANGO_SQL': True,

}


