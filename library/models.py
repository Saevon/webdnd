from library.constants import *
from library.items import *
from library.abstract_models import *
from library.references import *

class Condition(AbstractLibraryEntity):
    """
    A condition in which something can be.
    """
    
    modifiers = models.ManyToManyField("Modifier", related_name="conditions")
    short_description = models.CharField(blank=True, max_length=STND_CHAR_LIMIT)

class Feat(AbstractLibraryEntity):
    """
    Feats.
    """
    
    feat_type = models.ForeignKey("FeatType")
    feat_class = models.CharField(blank=True, max_length=STND_ID_CHAR_LIMIT, choices=FEAT_CLASSES)
    prerequisites = models.ManyToManyField("self", blank=True)
    modifiers = models.ManyToManyField("Modifier", related_name="feats")

class FeatType(AbstractLibraryEntity):
    """
    A type of a feat.
    """

class Spell(AbstractLibraryEntity):
    """
    Spell
    """
    
    