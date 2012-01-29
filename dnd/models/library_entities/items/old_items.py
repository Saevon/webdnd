from django.db import models
from datetime import * as the

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.sources import Source
from dnd.models.library_entities.abstract import AbstractLibraryEntity
from dnd.models.modifiers import Modifier
from dnd.models.unknown import *

class AbstractMagicItem(models.Model):
    """
    anything that screws with physics
    """

    class Meta:
        abstract = True

    # TODO: look over magical items

    item_strength = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=MAGIC_ITEM_STRENGTHS)
    item_slot = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=MAGIC_ITEM_SLOTS)

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

class MagicWeapon(Weapon, AbstractMagicItem):
    magical_properties = models.TextField(blank=True)
    modifiers = models.ManyToManyField('Modifier', blank=True)

class MagicArmor(Armor, AbstractMagicItem):
    magical_properties = models.TextField(blank=True)
    modifiers = models.ManyToManyField('Modifier', blank=True)

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
