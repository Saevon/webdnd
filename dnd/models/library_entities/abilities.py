from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.abilities import ABILITY_CLASSES
from dnd.models.library_entities.abstract import AbstractDnDEntity
from dnd.models.modifiers.modifiers import Modifier
from dnd.models.modifiers.saving_throws import SavingThrow

class Ability(AbstractDnDEntity):
    """
    Ability
    """

    saving_throw = models.ForeignKey(SavingThrow, blank=True)
    type = models.ForeignKey("AbilityType", blank=False)
    ability_class = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=ABILITY_CLASSES,
        blank=False)
    prerequisites = models.ManyToManyField("self", blank=True)
    modifiers = models.ManyToManyField(
        Modifier,
        related_name="abilities",
        blank=True)
    #uses per day/week/ rnd etc
    #Also ensure a difference between passive/active abilities aka qualities and abiities
    #Automatic use abilities e.g. swarm attacks

class AbilityType(AbstractDnDEntity):
    """
    A type of a ability.
    """
