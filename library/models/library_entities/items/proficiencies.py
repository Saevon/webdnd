from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.items.proficiencies import PROFICIENCY_TYPES
from library.models.abstract import AbstractLibraryEntity

class ProficiencyGroup(AbstractLibraryEntity):
    """
    A Proficiency:
        e.g. simple, martial etc.
    """
    type = CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=PROFICIENCY_TYPES,
        blank=False)

