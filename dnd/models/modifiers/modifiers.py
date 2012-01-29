from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.modifiers import MODIFIER_TARGETS, STAT_UPDATE_TYPES
from dnd.models.abstract import AbstractLibraryModel
from dnd.models.modifiers.bonuses import Bonus
from dnd.models.modifiers.die_roll import DieRoll
from dnd.models.modifiers.values import Value


class Modifier(AbstractLibraryModel):
    """
    """
    target = models.CharField(
        max_length=STND_CHAR_LIMIT,
        choices=MODIFIER_TARGETS,
        blank=False)
    #stat affected is based on the target
    stat = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False)
    # Change
    value = models.ForeignKey(
        Value,
        related_name='modifiers',
        blank=False)
    change_type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=STAT_UPDATE_TYPES,
        blank=False)
    bonus_type = models.ForeignKey(
        Bonus,
        related_name='modifiers',
        blank=False)

