from django.db import models
from game.models import *
from library.constants import *

class LibraryAccount(models.Model):
    """
    A webdnd library account.
    """
    
    name = models.CharField(blank=False, max_length=STND_CHAR_LIMIT)
    # TODO: finish making this

    def __unicode__(self):
        return u"%s" %(self.name)

class AbstractLibraryEntity(models.Model):
    """
    A D&D entity in the library.
    """
    
    class Meta:
        abstract = True

    title = models.CharField(max_length=STND_CHAR_LIMIT, blank=False, unique=True)
    reference = models.ForeignKey("Source", blank=False)
    description = models.TextField(blank=True)
    creator = models.ForeignKey("LibraryAccount", blank=False)

    def __unicode__(self):
        return u"%s" %(self.title)

class Source(models.Model):
    """
    A D&D reference.
    """
    
    reference_type = models.CharField(choices=REFERENCE_TYPES, blank=False, max_length=STND_ID_CHAR_LIMIT)
    citation = models.TextField(blank=False)
    
    def __unicode__(self):
        return self.citation[:20]

class DieRoll(models.Model):
    
    """
    A D&D die roll.
    """
    
    number_of_dice = models.PositiveIntegerField()
    sides_on_die = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%sd%s" %(self.number_of_dice, self.sides_on_die)
        
class Modifier(models.Model):
    dieroll = models.ForeignKey("DieRoll", null=True, blank=True)
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
