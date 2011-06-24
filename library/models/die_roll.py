from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT

class DieRoll(models.Model):
    
    """
    A D&D die roll.
    """
    
    number_of_dice = models.PositiveIntegerField()
    sides_on_die = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%sd%s" %(self.number_of_dice, self.sides_on_die)
