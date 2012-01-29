from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.models.library_entities.abstract import AbstractDnDEntity
from dnd.models.items.abstract import AbstractItem
from dnd.models.combat.weapon_info import RangedWeaponInfo

class Item(AbstractItem):
    """
    A Generic Item
    """

class RangedWeapon(AbstractItem):
    ranged = models.ForeignKey(
        RangedWeaponInfo,
        blank=True,
        null=True)

