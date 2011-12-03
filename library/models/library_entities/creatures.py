from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.library_entities.abilities import Ability

class CreatureType(AbstractLibraryEntity):
    """
    A Monster Type.
    """
    #hitdie=
    #attack_bonus=
    good_fort = models.BooleanField(blank=False)
    good_ref = models.BooleanField(blank=False)
    good_will = models.BooleanField(blank=False)
    #skill_points = models.I
    # Restrictions? e.g. animal = Neutral Alignment
    abilities = models.ManyToManyField(
        Ability,
        related_field="creature_types",
        blank=True,
        null=True)
    # Stat Changes?

class CreatureSubType(AbstractLibraryEntity):
    """
    A Creature's Subtype
    """
    # Restrictions? e.g. animal = Neutral Alignment
    abilities = models.ManyToManyField(
        Ability,
        related_field="creature_types",
        blank=True,
        null=True)
    # Stat Changes?

