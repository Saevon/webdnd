from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity

# are we sure that it should inherit from an abstract le?
class Bonus(AbstractLibraryEntity):
    """
    A type of Bonus that can be granted
    """
    stackable = models.BooleanField(blank=False)

