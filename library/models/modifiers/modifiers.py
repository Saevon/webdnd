from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.modifiers import MODIFIER_TARGETS, STAT_UPDATE_TYPES
from library.models.abstract import AbstractLibraryModel
from library.models.modifiers.bonuses import Bonus
from library.models.modifiers.die_roll import DieRoll
from library.models.modifiers.values import Value


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
        related_field='modifiers',
        blank=False)
    change_type = models.CharField(
        max_length=STND_CHAR_ID_LIMIT,
        choices=STAT_UPDATE_TYPES,
        blank=False)
    # blank string == no conditions
    conditions = models.TextField(blank = True)
    bonus_type = models.ForeignKey(
        Bonus,
        related_field='modifiers',
        blank=False)

