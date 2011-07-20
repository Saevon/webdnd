from django.db import models

from library.models.abstract import AbstractLibraryModel
from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.modifiers.die_roll import DieRoll

class Modifier(AbstractLibraryModel):
    #TODO: look over class to ensure it fits with our `new` ideas
    dieroll = models.ForeignKey(DieRoll, blank=True)
    amount = models.PositiveIntegerField(blank=True)
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
