from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.items.armor import SHIELD_SIZES
from library.models.combat.armor_info import ArmorInfo
from library.models.items.abstract import AbstractItem
from library.models.library_entities.abstract import AbstractLibraryEntity

class AbstractArmor(AbstractItem):
    """
    Generic Armor
    """
    class Meta(AbstractItem.Meta):
        abstract=True

    armor = models.ForeignKey(
        ArmorInfo,
        related_field='item_%(class)s',
        blank=False)

class BodyArmor(AbstractArmor):
    # TODO: Action Time Needed
    #time_to_equip = 
    #time_to_don_hastily = 
    #time_to_remove = 

class Shield(AbstractArmor):
    """
    A Shield
    """
    shield_size = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=SHIELD_SIZES,
        blank=False)
