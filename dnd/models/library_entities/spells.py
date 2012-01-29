from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.magic import SCHOOLS_OF_MAGIC
from dnd.constants.magic.spells import SPELL_RANGES
from dnd.models.abstract import AbstractLibraryModel
from dnd.models.combat.spell_info import TouchAttackInfo
from dnd.models.library_entities.abstract import AbstractLibraryEntity
from dnd.models.library_entities.abilities import Ability
from dnd.models.library_entities.classes import DnDClass
from dnd.models.library_entities.conditions import Condition
from dnd.models.modifiers.modifiers import Modifier
from dnd.models.modifiers.saving_throws import SavingThrow
from dnd.models.units import ActionTimeDuration

class Spell(AbstractLibraryEntity):
    """
    Spell
    """

    school = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SCHOOLS_OF_MAGIC,
        blank=False)
    descriptors = models.ManyToManyField(
        'SpellDescriptor',
        related_name="spells",
        blank=True)
    short_description = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
    saving_throw = models.ForeignKey(SavingThrow, blank=True)
    modifiers = models.ManyToManyField(
        Modifier,
        related_name="spells",
        blank=True)
    # target?
# Duration?
    #range = models.CharField(blank=True, max_length=100)
    touch_attack = models.ForeignKey(
        TouchAttackInfo,
        related_name='spells',
        blank=True)
    conditions = models.ManyToManyField(
        Condition,
        related_name='spells',
        blank=True)
    # All Effects are in the description

    # Components
    verbal_component = models.BooleanField(default=False)
    somatic_component = models.BooleanField(default=False)
    material_component = models.BooleanField(default=False)
    focus_component = models.BooleanField(default=False)
    divine_focus_component = models.BooleanField(default=False)
    xp_component = models.BooleanField(default=False)

    # Special Tags
    shapeable = models.BooleanField(default=False)
    affects_objects = models.BooleanField(default=False)
    harmless = models.BooleanField(default=False)
    dismiss = models.BooleanField(default=False)

    casting_time = models.ForeignKey("ActionTimeDuration", blank=False)
    resistable = models.BooleanField(default=True)

    negates = models.ManyToManyField(
        'self',
        related_name='negated_by',
        blank=True)
    versions = models.ManyToManyField(
        'self',
        blank=True)
    #upgraded spells? cure moderate -> serious -> critical

class Domain(AbstractLibraryEntity):
    """
    A Domain
    """
    granted_power = models.ForeignKey(
        Ability,
        related_name='domains',
        blank=False)

class DomainSpellLevel(AbstractLibraryModel):
    """
    A domain Spell level
    """
    class Meta(AbstractLibraryModel.Meta):
        unique_together = (
            ('domain','level'),
        )

    domain = models.ForeignKey(
        Domain,
        related_name='spells',
        blank=False)
    level = models.PositiveIntegerField(null=False, blank=False)
    spell = models.ForeignKey(
        Spell,
        related_name='domain_spells',
        blank=False)

class SpellDescriptor(AbstractLibraryEntity):
    """
    A spell descriptor.
    """

class CastingLevelClassPair(AbstractLibraryModel):
    """
    A pair of a class and a casting level.
    """
    class Meta(AbstractLibraryModel.Meta):
        unique_together = (
            ('dnd_class', 'spell'),
        )

    dnd_class = models.ForeignKey(
        DnDClass,
        related_name='spell_list',
        blank=False)
    #Or is it? related to class.py spell/day class
    casting_level = models.PositiveSmallIntegerField(blank=False)
    spell = models.ForeignKey(
        Spell,
        related_name='spell_levels',
        blank=False)
