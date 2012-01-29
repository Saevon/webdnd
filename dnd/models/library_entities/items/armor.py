from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.items.armor import SHIELD_SIZES
from dnd.models.combat.armor_info import ArmorInfo
from dnd.models.items.abstract import AbstractItem
from dnd.models.library_entities.abstract import AbstractLibraryEntity

class AbstractArmor(AbstractItem):
    """
    Generic Armor
    """
    class Meta(AbstractItem.Meta):
        abstract=True

    armor = models.ForeignKey(
        ArmorInfo,
        related_name='item_%(class)s',
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
