from django.db import models

from library.models.abstract import AbstractLibraryModel
from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT

class ActionTimeDuration(AbstractLibraryModel):
    """
    A length of time in actions.
    """
    
    time = models.IntegerField(blank=False)

# TODO: Make a measurement module:
#   - mass
#   - time
#   - distance
#   - volume
#   - cost
