from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.models.library_entities.abstract import AbstractDnDEntity

# are we sure that it should inherit from an abstract le?
class Bonus(AbstractDnDEntity):
    """
    A type of Bonus that can be granted
    """
    stackable = models.BooleanField(blank=False)

