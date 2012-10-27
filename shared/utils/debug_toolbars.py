import django
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from debug_toolbar.panels import DebugPanel
import sys


class VersionDebugPanel(DebugPanel):
    '''
    Panel that displays the Django version.
    '''
    name = 'Version'
    has_content = True

    def nav_title(self):
        return _('Versions')

    def nav_subtitle(self):
        return 'Django %s' % django.get_version()

    def url(self):
        return ''

    def title(self):
        return _('Versions')

    def content(self):
        versions = {}

        versions['Web D&D'] = settings.VERSION
        versions['Syncrae'] = settings.SYNCRAE_VERSION

        context = self.context.copy()
        context.update({
            'versions': versions,
            'paths': sys.path,
        })

        return render_to_string('debug_toolbar/panels/versions.html', context)

class SyncraeSpyDebugPanel(DebugPanel):
    '''
    Panel that shows Syncrae Messages
    '''
    name = 'Syncrae'
    has_content = True

    def nav_title(self):
        return _('Syncrae')

    def nav_subtitle(self):
        return ''

    def url(self):
        return ''

    def title(self):
        return _('Syncrae')

    def content(self):
        return render_to_string('debug_syncrae.html', self.context)


class DividerDebugPanel(DebugPanel):
    name = 'Divider'
    has_content = False

    def nav_title(self):
        return ' '







