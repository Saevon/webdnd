from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.models.abstract import AbstractDnDModel
from dnd.models.modifiers.die_roll import DieRoll

#TODO add math between these types
class Value(AbstractDnDModel):
    """
    A Value including Decimals and Die Rolls
    """
    die_roll = models.ManyToManyField(
        DieRoll,
        related_name='values',
        blank=False
    )
    modifier = models.IntegerField(blank=False, null=False)

class Multiplier(AbstractDnDModel):
    """
    A DnD Multiplier
    """
    value = models.PositiveIntegerField(blank=False, null=False)

