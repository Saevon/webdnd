from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity

class DamageType(AbstractLibraryEntity):
    """
    A damage type
    """
    damage_group = models.ForeignKey(
        'DamageGroup',
        related_name='damage_types',
        blank=False)

class DamageGroup(AbstractLibraryEntity):
    """
    A damage group
    """

