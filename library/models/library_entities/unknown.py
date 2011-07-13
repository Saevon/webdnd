"""
Non sorted models
"""
#TODO: move any existing models to a fitting module
from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.unknown import SAVE_TYPES
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.modifiers.modifiers import Modifier

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
