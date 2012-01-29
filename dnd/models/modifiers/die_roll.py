from django.db import models

from dnd.models.abstract import AbstractLibraryModel
from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT

class DieRoll(AbstractLibraryModel):

    """
    A D&D die roll.
    """
    # TODO: Check that this class still works with 'New ideas'
    # TODO: add math between dice

    number_of_dice = models.PositiveIntegerField(blank=False)
    sides_on_die = models.PositiveIntegerField(blank=False)

    def __unicode__(self):
        return u"%sd%s" % (self.number_of_dice, self.sides_on_die)
