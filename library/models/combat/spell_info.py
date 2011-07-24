from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.combat.weapon_info import AbstractWeaponInfo

class TouchAttackInfo(AbstrachWeaponInfo):
    """
    A Touch Attack, Includes Ranged Touch Attacks
    """

