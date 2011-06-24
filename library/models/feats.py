from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.feats import FEAT_CLASSES
from library.models.abstract import AbstractLibraryEntity
from library.models.modifiers import Modifier
from library.models.unknown import SavingThrow

class Feat(AbstractLibraryEntity):
    """
    Feats.
    """
    
    saving_throw = models.ForeignKey("SavingThrow", blank=True)
    feat_type = models.ForeignKey("FeatType", blank=False)
    feat_class = models.CharField(blank=False, max_length=STND_ID_CHAR_LIMIT, choices=FEAT_CLASSES)
    prerequisites = models.ManyToManyField("self", blank=True)
    modifiers = models.ManyToManyField("Modifier", related_name="feats", blank=True)

class FeatType(AbstractLibraryEntity):
    """
    A type of a feat.
    """
