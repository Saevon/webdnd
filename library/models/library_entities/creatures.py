from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.creatures import SIZES
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.library_entities.abilities import Ability
from library.models.library_entities.classes import SaveProgression

class Creature(AbstractLibraryEntity):
    """
    A base Creature
    """

    abilities = models.ManyToManyField(
        Ability,
        related_name="creature_types",
        blank=True,
        null=True)
    # TODO: spells gotten from the class

class Race(AbstractLibraryEntity):
    """
    A Race one can Play
    """
    size = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SIZES,
        blank=False)
    level_adjustment = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False)
    # One time changes/effects that occur foer being of this Race
    modifiers = models.ManyToManyField(
        Modifier,
        related_name="races",
        blank=True,
        null=True)
    # Changes that are lost during polymorph "continuous" abilities
    abilities = models.ManyToManyField(
        Ability,
        related_name="races",
        blank=True,
        null=True)
    # TODO: Restrictions? e.g. animal = Neutral Alignment
    # TODO: spells gotten from the class
    favored_class = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
    languages = models.ManyToManyField(
        Language,
        related_name="races",
        blank=True,
        null=True)

class CreatureType(AbstractLibraryEntity):
    """
    A Monster Type.
    """
    hit_die = models.PositiveIntegerField(blank=False, null=False)
    base_attack_bonus = models.DecimalField(max_digits=5, decimal_places=2)
    saves = models.ForeignKey(
        SaveProgression,
        related_name="creature_types")
    skill_points = models.PositiveIntegerField(blank=False, null=False)
    abilities = models.ManyToManyField(
        Ability,
        related_name="creature_types",
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
        related_name="creature_types",
        blank=True,
        null=True)
    # TODO: Restrictions? e.g. animal = Neutral Alignment
    # TODO: Stat Changes?
