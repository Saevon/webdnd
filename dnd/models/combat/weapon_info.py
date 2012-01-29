from django.db import models

from dnd.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.abstract import AbstractLibraryModel
from library.models.library_entities.combat.damage import DamageType
from library.models.library_entities.combat.proficiencies import ProficiencyGroup

class AbstractWeaponInfo(AbstractLibraryModel):
    """
    The main Combat Stats needed for a weapon
    """
    class Meta(AbstractLibraryModel.Meta):
        abstract = True

    proficiency_group = models.ForeignKey(
        ProficiencyGroup,
        related_name='%(class)s',
        blank=False)
    # weapon_class = #sword, bow, etc
    # damage = #
    damage_type = models.ForeignKey(
        DamageType,
        related_name='%(class)s',
        blank=False)
    touch_attack = models.BooleanField(
        default=False,
        blank=True)

    critical_range = models.PositiveIntegerField(
        blank=False,
        null=False)
    critical_multiplier = models.PositiveIntegerField(
        blank=False,
        null=False)

class MeleeWeaponInfo(AbstractWeaponInfo):
    """
    The main Combat Stats needed for a melee waepon
    """
    reach = models.PositiveIntegerField(
        default=5,
        blank=False,
        null=False)
    double_weapon = models.ForeignKey(
        'self',
        related_name='+',
        blank=True,
        null=True)

class ThrownWeaponInfo(AbstractWeaponInfo):
    """
    The main Combat Stats needed to throw an Item
    """
    range_increment = models.PositiveIntegerField(
        default=10,
        blank=False,
        null=False)

class RangedWeaponInfo(AbstractWeaponInfo):
    """
    The Main Combat Stats needed to use a Ranged Weapon
    """
    range_increment = models.PositiveIntegerField(
        blank=False,
        null=False)
    double_weapon = models.ForeignKey(
        'self',
        related_name='+',
        blank=True,
        null=True)
    # TODO: Ammunition
    # TODO: need DnDAction Time
    #reload_time = 
