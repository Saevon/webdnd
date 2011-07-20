from django.db import models

from library.models.abstract import AbstractLibraryModel
from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.unknown import SAVE_TYPES

class SavingThrow(AbstractLibraryModel):
    """
    A saving throw.
    """

    save_type = models.CharField(blank=False, max_length=STND_ID_CHAR_LIMIT, choices=SAVE_TYPES)
    save_dc = models.IntegerField(blank=False)
    save_fraction_numerator = models.IntegerField(blank=False)
    save_fraction_denominator = models.IntegerField(blank=False)

