from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.classes import CLASS_SKILL_TYPES
from library.models.abstract import AbstractLibraryModel
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.library_entities.feats import Feat
from library.models.library_entities.skills import Skill

class DnDClass(AbstractLibraryEntity):
    """
    A class in D&D.
    """

    class Meta(AbstractLibraryEntity.Meta):
        verbose_name_plural = "DnD Classes"

    # TODO: finish this
    # Proficiencies
    # Domain Spells
    # Spell List
    # Requiremnent and Prohibitions

class SaveProgression(AbstractLibraryEntity):
    """
    The amount a Characters Base Save Increases per Level
    """
    
    fort = models.DecimalField(max_digits=5, decimal_places=2)
    ref = models.DecimalField(max_digits=5, decimal_places=2)
    will = models.DecimalField(max_digits=5, decimal_places=2)

class BABProgression(AbstractLibraryEntity):
    """
    The amount a Characters Base Attack Bonus Increase per Level
    """

    increase = models.DecimalField(max_digits=5, decimal_places=2)

class ClassAbility(AbstractLibraryModel):
    """
    The abilities a DnDClass gets at a specific level
    """

    dnd_class = models.ForeignKey(
        DnDClass,
        related_field='class_abilities',
        blank=False)
    ability = models.ForeignKey(
        Feat,
        blank=False)
    level = models.IntegerField(blank=False, null=False)

class ClassSkill(AbstractLibraryModel):
    """
    Class Specific Abilities
    """
    dnd_class = models.ForeignKey(
        DnDClass,
        related_field='class_abilities',
        blank=False)
    skill = models.ForeignKey(
        Feat,
        blank=False)
    type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=CLASS_SKILL_TYPES,
        default='class',
        blank=False)

