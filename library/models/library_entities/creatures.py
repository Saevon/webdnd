from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.library_entities.abilities import Ability
from library.models.library_entities.classes import SaveProgression

class CreatureType(AbstractLibraryEntity):
    """
    A Monster Type.
    """
    hit_die = models.PositiveIntegerField(blank=False, null=False)
    base_attack_bonus = models.DecimalField(max_digits=5, decimal_places=2)
    saves = models.ForeignKey(
        SaveProgression,
        related_field="creatures")
    skill_points = models.PositiveIntegerField(blank=False, null=False)
    abilities = models.ManyToManyField(
        Ability,
        related_field="creature_types",
        blank=True,
        null=True)
    # TODO: Restrictions? e.g. animal = Neutral Alignment
    # TODO: Stat Changes?

class CreatureSubType(AbstractLibraryEntity):
    """
    A Creature's Subtype
    """
    abilities = models.ManyToManyField(
        Ability,
        related_field="creature_types",
        blank=True,
        null=True)
    # TODO: Restrictions? e.g. animal = Neutral Alignment
    # TODO: Stat Changes?

