from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.magic import SCHOOLS_OF_MAGIC
from library.config.magic.spells import SPELL_RANGES
from library.models.abstract import AbstractLibraryEntity
from library.models.modifiers import Modifier
from library.models.unknown import ActionTimeDuration, DnDClass, SavingThrow

class Spell(AbstractLibraryEntity):
    """
    Spell
    """
    
    school = models.CharField(max_length=STND_ID_CHAR_LIMIT, choices=SCHOOLS_OF_MAGIC, blank=False)
    sub_school = models.ForeignKey("SpellSubSchool", blank=True)
    descriptors = models.ManyToManyField("SpellDescriptor", related_name="spells", blank=True)
    levels = models.ManyToManyField("CastingLevelClassPair", blank=False)
    short_description = models.CharField(max_length=STND_CHAR_LIMIT, blank=True)
    saving_throw = models.ForeignKey("SavingThrow", blank=True)
    modifiers = models.ManyToManyField("Modifier", related_name="spells", blank=True)
    range = models.CharField(blank=True, max_length=100)
    
    # components
    verbal_component = models.BooleanField(default=False)
    somatic_component = models.BooleanField(default=False)
    material_component = models.BooleanField(default=False)
    focus_component = models.BooleanField(default=False)
    divine_focus_component = models.BooleanField(default=False)
    xp_component = models.BooleanField(default=False)
    
    casting_time = models.ForeignKey("ActionTimeDuration", blank=False)
    resistable = models.BooleanField(default=True)

class SpellDescriptor(AbstractLibraryEntity):
    """
    A spell descriptor.
    """

class CastingLevelClassPair(AbstractLibraryEntity):
    """
    A pair of a class and a casting level.
    """
    
    dnd_class = models.ForeignKey("DnDClass", blank=False)
    casting_level = models.PositiveSmallIntegerField(blank=False)

class SpellSubSchool(AbstractLibraryEntity):
    """
    A spell sub-school.
    """

class SpellRange(AbstractLibraryEntity):
    """
    A range of a spell. FFUUUUUUU!
    """
    
    range_type = models.CharField(blank=True, max_length=STND_ID_CHAR_LIMIT, choices=SPELL_RANGES)
    

