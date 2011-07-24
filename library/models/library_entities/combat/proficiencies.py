from django.db import models

from library.config import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.items.proficiencies import PROFICIENCY_TYPES
from library.models.abstract import AbstractLibraryEntity, AbstractLibraryModel

class ProficiencyGroup(AbstractLibraryEntity):
    """
    A Proficiency:
        e.g. simple, martial etc.
    """
    type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=PROFICIENCY_TYPES,
        blank=False)

class SharedProficiency(AbstractLibraryModel):
    """
    A Shared Proficiency
    """
    # main == the one you put on the Char Sheet
    main = models.ForeignKey(
        AbstractItem,#Check if you can point to an abstract?
        related_field='shared_proficiencies_main',
        blank=False)
    other = models.ForeignKey(
        AbstractItem,#Check if you can point to an abstract?
        related_field='shared_proficiencies_other',
        blank=False)

