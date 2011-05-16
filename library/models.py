from django.db import models
from datetime import *

from library.constants import *
from library.items import *

class DieRoll(models.Model):
    number_of_dice = models.PositiveIntegerField()
    sides_on_die = models.PositiveIntegerField()
    
    def __unicode__(self):
        return '%sd%s' %(self.number_of_dice, self.sides_on_die)

class Modifier(models.Model):
    dieroll = models.ForeignKey('DieRoll', null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    property_modified = models.CharField(max_length=STND_CHAR_LIMIT, blank=True)
    is_bonus = models.BooleanField(default=True)
    text = models.TextField(blank=True)
    
    def __unicode__(self):
        return_string = ""
        if self.is_bonus:
            return_string += "+("
        else:
            return_string += "-("
        return "%s%s to %s)" %(return_string, formatted_num_and_roll(self.amount, self.dieroll, 1), self.property_modified)
