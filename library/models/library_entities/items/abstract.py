from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.items.weapons import WEAPON_CLASSES
from library.config.unknown import SIZES
from library.models.combat.weapon_info import MeleeWeaponInfo, RangedWeaponInfo, ThrownWeaponInfo
from library.models.items.item_groups import ItemCategory
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.library_entities.items.materials import Material

class AbstractItem(AbstractLibraryEntity):
    """
    A generic item
    """
    class Meta(AbstractLibraryEntity.Meta):
        abstract = True

    # Info needed to Buy the Item
    item_category = models.ForeignKey(
        ItemCategory,
        related_field='item_%(class)s',
        blank=False)

    #base_price = models.PositiveIntegerField(blank=True, default=0)
    #dieroll_price = models.ForeignKey('DieRoll', blank=True)
    #dieroll_price_multiplier = models.PositiveIntegerField(blank=True, default=1)
    #trading_units = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=TRADING_MEASURING_UNITS)

    #base_hp = models.PositiveIntegerField(blank=True, default=1)
    #base_mass = models.FloatField(blank=True, default=0)

    base_material = models.ForeignKey(
        Material
        related_field='%(class)s_item',
        blank=False)
    size = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SIZES,
        blank=False)
    wield_size = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=WEAPON_CLASSES,
        blank=True)

    # Melee
    melee = models.ForeignKey(
        MeleeWeaponInfo,
        related_field='%(class)s_item',
        blank=True,
        null=True)
    #is this made to be used as a melee weapon?
    melee_stnd = models.BooleanField(blank=False)
    # Thrown
    thrown = models.ForeignKey(
        ThrownWeaponInfo,
        related_field='%(class)s_item',
        blank=True,
        null=True)
    #is this made to be used as a thrown weapon?
    thrown_stnd = models.BooleanField(blank=False)

    #TODO: Ammo? Liquids, containers, potions?
    # gems, poison vehicles, consumable, animal...
    # packages

    #def formatted_price(self):
    #    formatted_string = formatted_num_and_roll(self.base_price, self.dieroll_price, self.dieroll_price_multiplier)
    #    return "%s cp per %s" %(formatted_string, self.trading_units)

