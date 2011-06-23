from django.db import models
from datetime import *
from library.abstract_models import *
from library.constants import *

class AbstractEnhancement(AbstractLibraryEntity):
    class Meta:
        abstract = True

    prerequisites = models.TextField(blank=True)

class AbstractItem(AbstractLibraryEntity):
    class Meta:
        abstract = True

    base_price = models.PositiveIntegerField(blank=True, default=0)
    dieroll_price = models.ForeignKey('DieRoll', blank=True)
    dieroll_price_multiplier = models.PositiveIntegerField(blank=True, default=1)
    trading_units = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=TRADING_MEASURING_UNITS)

    base_hp = models.PositiveIntegerField(blank=True, default=1)
    base_mass = models.FloatField(blank=True, default=0)

    base_material = models.ForeignKey('Material')

    def formatted_price(self):
        formatted_string = formatted_num_and_roll(self.base_price, self.dieroll_price, self.dieroll_price_multiplier)
        return "%s cp per %s" %(formatted_string, self.trading_units)

class AbstractMagicItem(models.Model):
    """
    anything that screws with physics
    """

    class Meta:
        abstract = True

    # TODO: look over magical items

    aura_strength = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=AURA_STRENGTHS)
    aura_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=SCHOOLS_OF_MAGIC)
    item_strength = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=MAGIC_ITEM_STRENGTHS)
    item_slot = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=MAGIC_ITEM_SLOTS)

class Material(AbstractLibraryEntity):
    price = models.PositiveIntegerField(blank=True, default=0)
    hardness = models.PositiveIntegerField(blank=True, default=10)
    density = models.FloatField(blank=True, default=7.874)
    hp_per_thickness = models.FloatField(blank=True, default=30)

    # TODO: add bonuses
    """
    main_bonuses
    weapon_bonuses
    ammunition_bonuses
    light_armor_bonuses
    medium_armor_bonuses
    heavy_armor_bonuses
    shield_bonuses
    """

class Gem(AbstractItem):
    pass

class ArtObject(AbstractItem):
    num_gem_slots = models.PositiveIntegerField(blank=True, default=0)
    num_material_slots = models.PositiveIntegerField(blank=True, default=1)

class MagicArtObject(ArtObject, AbstractMagicItem):
    modifiers = models.ManyToManyField('Modifier', blank=True)

class PhysicalEnhancement(AbstractEnhancement):
    modifiers = models.ManyToManyField('Modifier', blank=True)

class MagicEnhancement(AbstractEnhancement, AbstractMagicItem):
    equivalent_bonus = models.PositiveIntegerField(blank=True, default=1)
    modifiers = models.ManyToManyField('Modifier', blank=True)

class Weapon(AbstractItem):
    is_melee = models.BooleanField()
    is_ranged = models.BooleanField()

    weapon_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=WEAPON_TYPES)
    weapon_class = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=WEAPON_CLASSES)

    damage = models.ForeignKey('DieRoll', related_name="%(app_label)s_%(class)s_related")
    damage_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=DAMAGE_TYPES)

    critical_low = models.PositiveIntegerField(blank=True, default=20)
    critical_multiplier = models.PositiveIntegerField(blank=True, default=2)

    range_increment = models.PositiveIntegerField(blank=True, default=0)
    reload_time = models.CharField(max_length=STND_ID_CHAR_LIMIT, blank=True, choices=ACTION_TYPES)
    reach = models.PositiveIntegerField(blank=True, default=5)

    double_weapon = models.BooleanField()
    works_with_specific_ammunition = models.ManyToManyField('Ammunition', blank=True)

class MagicWeapon(Weapon, AbstractMagicItem):
    magical_properties = models.TextField(blank=True)
    modifiers = models.ManyToManyField('Modifier', blank=True)

class Armor(AbstractItem):
    armor_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=ARMOR_TYPES)
    armor_bonus = models.PositiveIntegerField()
    armor_check_penalty = models.PositiveIntegerField()
    max_dexterity = models.PositiveIntegerField()
    spell_fail = models.PositiveIntegerField(blank=True, default=0)

    time_to_equip = models.PositiveIntegerField(blank=True, default=0)
    time_to_don_hastily = models.PositiveIntegerField(blank=True, default=0)
    time_to_remove = models.PositiveIntegerField(blank=True, default=0)

class MagicArmor(Armor, AbstractMagicItem):
    magical_properties = models.TextField(blank=True)
    modifiers = models.ManyToManyField('Modifier', blank=True)

class Shield(AbstractItem):
    armor_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=ARMOR_TYPES)
    armor_bonus = models.PositiveIntegerField()
    armor_check_penalty = models.PositiveIntegerField()
    max_dexterity = models.PositiveIntegerField()
    spell_fail = models.PositiveIntegerField(blank=True, default=0)

    weapon_class = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=WEAPON_CLASSES)
    damage = models.ForeignKey('DieRoll', related_name="%(app_label)s_%(class)s_related")
    damage_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=DAMAGE_TYPES)

class MagicShield(Shield, AbstractMagicItem):
    magical_properties = models.TextField(blank=True)
    modifiers = models.ManyToManyField('Modifier', blank=True)

class WondrousMagicItem(AbstractItem, AbstractMagicItem):
    modifiers = models.ManyToManyField('Modifier', blank=True)

class Poison(AbstractItem):
    description_of_use = models.TextField(blank=True)
    poison_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=POISON_TYPES)
    saving_throw = models.ForeignKey("SavingThrow", blank=False)
    initial_effects = models.ManyToManyField('Modifier', blank=True, related_name='initial_modifiers')
    secondary_effects = models.ManyToManyField('Modifier', blank=True, related_name='secondary_modifiers')
    other_effects = models.TextField(blank=True)

class Ammunition(AbstractItem):
    works_with_weapon_type = models.CharField(max_length=STND_ID_CHAR_LIMIT, blank=True, choices=WEAPON_TYPES)
    works_with_specific_weapons = models.ManyToManyField('Weapon', blank=True)
    description_of_use = models.TextField(blank=True)

class MagicAmmunition(Ammunition, AbstractMagicItem):
    modifiers = models.ManyToManyField('Modifier', blank=True)

class Vehicle(AbstractItem):
    pass

class Container(AbstractItem):
    volume = models.PositiveIntegerField(blank=True, default=0)
    max_mass = models.PositiveIntegerField(blank=True)

class AdventuringGear(AbstractItem):
    description_of_use = models.TextField(blank=True)

# helper functions
def format_dieroll(dieroll, multiplier):
    if not dieroll:
        return ""
    return_string = "%s" %(dieroll)
    if multiplier > 1:
        return_string += " * %i" %(multiplier)
    return return_string

def formatted_num_and_roll(number, dieroll, multiplier):
    return_string = ""
    if dieroll and number != 0:
        return_string += "%i + %s" %(number, format_dieroll(dieroll, multiplier))
    elif dieroll and number == 0: 
        return_string += "%s" %(format_dieroll(dieroll, multiplier))
    else:
        return_string += "%i" %(number)
    return return_string
