from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.abstract import AbstractLibraryModel
from library.models.proficiencies import ProficiencyGroup

class ArmorInfo(AbstractLibraryModel):
    """
    Stats needed for generic armor
    """
    proficiency_group = models.ForeignKey(
        ProficiencyGroup,
        related_name='armor_info',
        blank=False)
    armor_bonus = models.IntegerField(blank=False)
    # store as change .: if negative == penalty
    armor_check_penalty = models.IntegerField(blank=False)
    max_dexterity = models.PositiveIntegerField(blank=False)
    arcane_spell_fail = models.IntegerField(blank=False)

