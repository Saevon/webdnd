from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.classes import CLASS_CATEGORIES, CLASS_SKILL_TYPES
from dnd.constants.magic import MAGIC_SOURCES
from dnd.constants.creatures import ATTRIBUTES
from dnd.models.abstract import AbstractDnDModel
from dnd.models.library_entities.abstract import AbstractDnDEntity
from dnd.models.library_entities.abilities import Ability
from dnd.models.library_entities.combat.proficiencies import ProficiencyGroup
from dnd.models.library_entities.items.abstract import AbstractItem
from dnd.models.library_entities.skills import Skill

class DnDClass(AbstractDnDEntity):
    """
    A class in D&D.
    """

    class Meta(AbstractDnDEntity.Meta):
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
    saves = models.ForeignKey(
        'SaveProgression',
        related_name="classes")
    hit_die = models.PositiveIntegerField(blank=False, null=False)
    base_attack_bonus = models.DecimalField(max_digits=5, decimal_places=2)
    skill_points = models.PositiveIntegerField(blank=False, null=False)
    proficiencies = models.ManyToManyField(
        ProficiencyGroup,
        related_name='class_proficiencies',
        blank=True)
    # TODO: Change Proficiences
    #specific_proficiencies = models.ManyToManyField(
    #    AbstractItem,
    #    related_name='class_proficiencies',
    #    blank=True)
    # Spell Related
    spell_stat = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=ATTRIBUTES,
        blank=True)
    spellcasting_type=models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=MAGIC_SOURCES,
        blank=True)
    # If you fail to follow prohibitions/rules what happens
    ex_class = models.TextField(blank=True)

    # TODO: finish this
    # Proficiencies
    # Requiremnent and Prohibitions

class SaveProgression(AbstractDnDEntity):
    """
    The amount a Characters Base Save Increases per Level
    """
    fort = models.DecimalField(max_digits=5, decimal_places=2)
    ref = models.DecimalField(max_digits=5, decimal_places=2)
    will = models.DecimalField(max_digits=5, decimal_places=2)

class ClassAbility(AbstractDnDModel):
    """
    The abilities a DnDClass gets at a specific level
    """

    dnd_class = models.ForeignKey(
        DnDClass,
        related_name='class_abilities',
        blank=False)
    ability = models.ForeignKey(
        Ability,
        blank=False)
    level = models.IntegerField(blank=False, null=False)

class ClassSkill(AbstractDnDModel):
    """
    Class Specific Abilities
    """
    class Meta(AbstractDnDModel.Meta):
        unique_together = (
            ('dnd_class', 'skill'),
        )

    dnd_class = models.ForeignKey(
        DnDClass,
        related_name='class_skills',
        blank=False)
    skill = models.ForeignKey(
        Skill,
        blank=False)
    type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=CLASS_SKILL_TYPES,
        default='class',
        blank=False)

class ClassSpellLevel(AbstractDnDModel):
    """
    Class Spells of a certain type at a certain level
    """
    class Meta(AbstractDnDModel.Meta):
        unique_together = (
            ('dnd_class','spell_level', 'type', 'level'),
        )

    dnd_class = models.ForeignKey(
        DnDClass,
        related_name='class_spells',
        blank=False)
    # 0-9 + epic? TODO look over ALL possible spell levels
    spell_level = models.IntegerField(
        blank=False,
        null=False)
    # +N type at this spell level
    spell_level_increase = models.IntegerField(
        blank=False,
        null=False)
    type = models.ForeignKey(
        'ClassSpellType',
        related_name='class_spell_level',
        blank=False)
    level = models.PositiveIntegerField(blank=False, null=False)

class ClassSpellType(AbstractDnDEntity):
    """
    A type of spell,
      e.g. spell/day, known spell
    """
