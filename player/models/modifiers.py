from django.db import models
from django.conf import settings

from webdnd.shared.utils.decorators import dirty_cache
from webdnd.player.modifier_env import modifier
import re


class Modifier(models.Model):
    '''
    An optional modifier to a character
    '''

    condition = models.TextField(blank=True)
    modifier = models.TextField(blank=False)

    DISALLOWED_CODE = re.compile('|'.join(['(%s)' % i for i in (
        # Imports
        r' *(from +[a-zA-Z0-9_.]+ +)?import +[0-9a-zA-Z_]+( *\n)?',

        # exec
        r' *exec *(.*) *',
    )]))

    @dirty_cache
    def compile(self):
        return modifier(self, lambda *args, **kwargs: None)

    def save(self, *args, **kwargs):
        # Remove code that isn't allowed
        self.condition = self.DISALLOWED_CODE.sub('', self.condition)
        self.modifier = self.DISALLOWED_CODE.sub('', self.modifier)


        super(Modifier, self).save(*args, **kwargs)
        self._compile_dirty = True




def calculate(data):
    '''
    # None values aren't allowed

    data: {
        'active': bool,
        'character': {
            'ambidextrous': bool,
            ...
        },
        'mainhand': {
            # if the player is using it with both hands
            'twohanded': bool,
            'type': False or '2H' or '1.5H' or ...
            ...
        },
        'offhand': {
            'type': False or 'shield' or 'light' or ...
            ...
        }
    }

    returns: {
        'character': {
            'field': val # increase by
            # don't list unchanged fields
        },
        'mainhand': {
            ...
        },
        'offhand': {
            ...
        }
    }
    '''

    # cond = self._compile_condition()
    # if not cond(data):
    #     return {}
    # else:
    #     mod = self._compile_modifier()
    #     return mod(data)
    return

