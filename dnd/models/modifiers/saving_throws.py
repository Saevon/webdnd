from django.db import models

from dnd.models.abstract import AbstractLibraryModel
from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.saving_throws import SAVE_AFFECTS, SAVE_STATS

class SavingThrow(AbstractLibraryModel):
    """
    A saving throw.
    """

    stat = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SAVE_STATS,
        blank=False)
    save_dc = models.IntegerField(blank=False)
    save_affect = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SAVE_AFFECTS,
        blank=False)

