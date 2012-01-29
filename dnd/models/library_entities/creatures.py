from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.creatures import SIZES
from dnd.models.library_entities.abstract import AbstractDnDEntity
from dnd.models.library_entities.abilities import Ability
from dnd.models.library_entities.classes import SaveProgression

class Creature(AbstractDnDEntity):
    """
    A base Creature
    """

    abilities = models.ManyToManyField(
        Ability,
        related_name="creature_types",
        blank=True,
        null=True)
    # TODO: Appearance, weight, etc
    # Movement is calculated from abilities
    # natural_weapons
    # proficiency?
    # size/Reach: based on race average and DnD "squares"
    length = models.PositiveIntegerField(blank=False, null=False)
    width = models.PositiveIntegerField(blank=False, null=False)
    height = models.PositiveIntegerField(blank=True, null=True)
    reach = models.PositiveIntegerField(blank=False, null=False)
    # base Stats
    # Climate Terrain
    # Society and organization. Treasure.  Separate table?
    # CR
    restrictions = models.ManyToManyField(
        Restriction,
        related_name="creatures",
        blank=True,
        null=True)

class Race(AbstractDnDEntity):
    """
    A Race one can Play
    """
    base_creature = models.ForeignKey(
        Creature,
        blank=False,
        null=False)
    size = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SIZES,
        blank=False)
    level_adjustment = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False)
    # One time changes/effects that occur for being of this Race
    # e.g. Stats, proficiencies etc.
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
    restrictions = models.ManyToManyField(
        Restriction,
        related_name="races",
        blank=True,
        null=True)
    # not actually going to be used for active filters or searches
    favored_class = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
    languages = models.ManyToManyField(
        Language,
        related_name="races",
        blank=True,
        null=True)

class CreatureType(AbstractDnDEntity):
    """
    A Monster Type.
    """
    hit_die = models.PositiveIntegerField(blank=False, null=False)
    base_attack_bonus = models.DecimalField(
        max_digits=5,
        decimal_places=2)
    saves = models.ForeignKey(
        SaveProgression,
        related_name="creature_types")
    skill_points = models.PositiveIntegerField(blank=False, null=False)
    abilities = models.ManyToManyField(
        Ability,
        related_name="creature_types",
        blank=True,
        null=True)
    restrictions = models.ManyToManyField(
        Restriction,
        related_name="creature_types",
        blank=True,
        null=True)
    modifiers = models.ManyToManyField(
        Modifier,
        related_name="creature_types",
        blank=True,
        null=True)

class CreatureSubType(AbstractDnDEntity):
    """
    A Creature's Subtype
    """
    abilities = models.ManyToManyField(
        Ability,
        related_name="creature_subtypes",
        blank=True,
        null=True)
    restrictions = models.ManyToManyField(
        Restriction,
        related_name="creature_subtypes",
        blank=True,
        null=True)
    modifiers = models.ManyToManyField(
        Modifier,
        related_name="creature_subtypes",
        blank=True,
        null=True)
