from django.db import models

from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.combat.weapon_info import AbstractWeaponInfo

class TouchAttackInfo(AbstractWeaponInfo):
    """
    A Touch Attack, Includes Ranged Touch Attacks
    """

