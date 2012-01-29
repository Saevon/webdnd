from django.db import models

from dnd.models import *
from game.constants import *
from lib.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT

class Character(models.Model):
    name = models.CharField(max_length=STND_CHAR_LIMIT)
    # account
    # groups

    def __unicode__(self):
        return self.name

class CharacterSheet(models.Model):
    owner_character = models.ForeignKey('Character')

    def __unicode__(self):
        return "%s's character sheet." %(self.owner_character)

class Item(models.Model):
    """
    an item
    """

    class Meta:
        abstract = True

    character_sheet = models.ForeignKey('CharacterSheet')

    def full_name(self):
        raise NotImplemented

    def __unicode__(self):
        return "%s belonging to %s" %(self.full_name(), self.character_sheet)

class WeaponItem(Item):
    default_object = models.ForeignKey('dnd.Weapon')
    material = models.ForeignKey('dnd.Material', null=True, blank=True)
    physical_enhancements = models.ManyToManyField('dnd.PhysicalEnhancement', null=True, blank=True)
    magical_enhancements = models.ManyToManyField('dnd.MagicEnhancement', null=True, blank=True)

    magical_bonus = models.CharField(max_length=1, choices=WEAPON_PLUSES, default='0')

    def print_material(self):
        if not self.material or self.material == self.default_object.base_material:
            return ''
        else:
            return "%s " %(self.material)

    def list_physical_enhancements(self):
        return_string = ""
        if self.physical_enhancements.count() == 0:
            return return_string
        else:
            return_string += " with "
            for enhancement in self.physical_enhancements.all():
                return_string += str(enhancement) + ", "

            return return_string[:-2]

    def list_magical_enhancements(self):
        return_string = ""
        if self.magical_enhancements.count() == 0:
            return return_string
        else:
            for enhancement in self.magical_enhancements.all():
                return_string += str(enhancement) + ", "

            return return_string[:-2] + " "

    def print_magical_bonus(self):
        if self.magical_bonus == '0':
            return ''
        else:
            return '+%s' % (self.magical_bonus) + " "

    def full_name(self):
        return "%s%s%s%s%s" %(self.print_magical_bonus(), self.list_magical_enhancements(), self.print_material(), self.default_object, self.list_physical_enhancements())
