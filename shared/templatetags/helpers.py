from django import template
from django.conf import settings

import logging
logging = logging.getLogger('templatetags')

register = template.Library()

@register.simple_tag
def setting(k, default=None):
    return get_setting(k, default)

@register.assignment_tag
def setting_var(k, default=None):
    return get_setting(k, default)

def get_setting(k, default=None):
    if hasattr(settings, k):
        return getattr(settings, k)
    else:
        logging.warn('Setting not found: "%s"' % k)
    if default is None:
        return ''
    return default

