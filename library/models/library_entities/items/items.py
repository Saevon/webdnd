from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.library_entities.abstract import AbstractLibraryEntity
from library.models.items.abstract import AbstractItem
from library.models.combat.weapon_info import RangedWeaponInfo

class Item(AbstractItem):
    """
    A Generic Item
    """

class RangedWeapon(AbstractItem):
    ranged = models.ForeignKey(
        RangedWeaponInfo,
        blank=True,
        null=True)

