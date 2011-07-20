from django.db import models

from library.models.abstract import AbstractLibraryModel
from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.unknown import SAVE_TYPES

class SavingThrow(AbstractLibraryModel):
    """
    A saving throw.
    """

    save_type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SAVE_TYPES,
        blank=False)
    save_dc = models.IntegerField(blank=False)
    save_reduction = models.DecimalField(
        max_digits=4,
        decimal_places=3,
        blank=False)

