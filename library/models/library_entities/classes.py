from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.classes import CLASS_CATEGORIES, CLASS_SKILL_TYPES
from library.config.magic import MAGIC_SOURCES
from library.config.unknown import ATTRIBUTES
from library.models.abstract import AbstractLibraryModel
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.library_entities.abilities import Ability
from library.models.library_entities.skills import Skill

class DnDClass(AbstractLibraryEntity):
    """
    A class in D&D.
    """

    class Meta(AbstractLibraryEntity.Meta):
        verbose_name_plural = "DnD Classes"

    class_abv = models.CharField(
        primary_key=True, #Not sure if this will break since parent has PK
        unique=True, #in case the above breaks
        max_length=STND_ID_CHAR_LIMIT,
        blank=False)
    class_category = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=CLASS_CATEGORIES,
        blank=False)
    save_progression = models.ForeignKey('SaveProgression')
    hit_die = models.PositiveIntegerField(blank=False, null=False)
    base_attack_bonus = models.ForeignKey('BABProgression')
    skill_points = models.PositiveIntegerField(blank=False, null=False)
    # Spell Related
    spell_stat = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=ATTRIBUTES,
        blank=True)
    spellcasting_type=models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=MAGIC_SOURCES
        blank=True)
    # If you fail to follow prohibitions/rules what happens
    ex_class = TextField(blank=True)

    # TODO: finish this
    # Proficiencies
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
        Ability,
        blank=False)
    level = models.IntegerField(blank=False, null=False)

class ClassSkill(AbstractLibraryModel):
    """
    Class Specific Abilities
    """
    class Meta(AbstractLibraryModel):
        unique_together = (
            ('dnd_class', 'skill'),
        )

    dnd_class = models.ForeignKey(
        DnDClass,
        related_field='class_skills',
        blank=False)
    skill = models.ForeignKey(
        Skill,
        blank=False)
    type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=CLASS_SKILL_TYPES,
        default='class',
        blank=False)

class ClassSpellLevel(AbstractLibraryModel):
    """
    Class Spells of a certain type at a certain level
    """
    class Meta(AbstractLibraryModel):
        unique_together = (
            ('dnd_class','spell_level', 'type', 'level'),
        )

    dnd_class = models.ForeignKey(
        DnDClass,
        related_field='class_spells',
        blank=False)
    # 0-9 + epic? TODO look over ALL possible spell levels
    spell_level = models.IntegerField(
        blank=False,
        null=False)
    # +N type at this spell level
    spell_level_increase = models.IntegerField(
        blank=False,
        null=False)
    type = dnd_class = models.ForeignKey(
        'ClassSpellType',
        related_field='class_spell_level',
        blank=False)
    level = models.PositiveIntegerField(blank=False, null=False)

class ClassSpellType(AbstractLibraryEntity):
    """
    A type of spell,
      e.g. spell/day, known spell
    """
