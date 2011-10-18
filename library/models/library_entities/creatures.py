from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity

class MonsterType(AbstractLibraryEntity):
    """
    A Monster Type.
    """

    #modifiers
    #hitdie=
    #attack_bonus=
    good_fort = models.BooleanField(blank=False)
    good_ref = models.BooleanField(blank=False)
    good_will = models.BooleanField(blank=False)
    #skill_points = models.I
    #feats = 
