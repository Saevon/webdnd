from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.models.library_entities.abstract import AbstractDnDEntity

class DamageType(AbstractDnDEntity):
    """
    A damage type
    """
    damage_group = models.ForeignKey(
        'DamageGroup',
        related_name='damage_types',
        blank=False)

class DamageGroup(AbstractDnDEntity):
    """
    A damage group
    """

