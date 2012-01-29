from django.db import models

from dnd.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity

class ItemCategory(AbstractLibraryEntity):
    """
    Item Category for the sake of purchases
    """

#TODO: Item Kits
