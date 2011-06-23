"""
Non sorted models
"""
#TODO: move any existing models to a fitting module
from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.unknown import SAVE_TYPES
from library.models.abstract import AbstractLibraryEntity
from library.models.modifier import Modifier

class DieRoll(models.Model):
    
    """
    A D&D die roll.
    """
    
    number_of_dice = models.PositiveIntegerField()
    sides_on_die = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%sd%s" %(self.number_of_dice, self.sides_on_die)

class Condition(AbstractLibraryEntity):
    """
    A condition in which something can be.
    """
    
    modifiers = models.ManyToManyField("Modifier", related_name="conditions", blank=True)
    short_description = models.CharField(blank=True, max_length=STND_CHAR_LIMIT)

class SavingThrow(models.Model):
    """
    A saving throw.
    """

    save_type = models.CharField(blank=False, max_length=STND_ID_CHAR_LIMIT, choices=SAVE_TYPES)
    save_dc = models.IntegerField(blank=False)
    save_fraction_numerator = models.IntegerField(blank=False)
    save_fraction_denominator = models.IntegerField(blank=False)

class DnDClass(AbstractLibraryEntity):
    """
    A class in D&D.
    """
    
    # TODO: finish this

class ActionTimeDuration(models.Model):
    """
    A length of time in actions.
    """
    
    time = models.IntegerField(blank=False)

# TODO: Make a measurement module:
#   - mass
#   - time
#   - distance
#   - volume
#   - cost
