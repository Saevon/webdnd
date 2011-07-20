from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity

class DnDClass(AbstractLibraryEntity):
    """
    A class in D&D.
    """
    
    # TODO: finish this
