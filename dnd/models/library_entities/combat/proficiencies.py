from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.items.proficiencies import PROFICIENCY_TYPES
from library.models.abstract import AbstractLibraryModel
from library.models.library_entities.abstract import AbstractLibraryEntity

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
    # TODO: fix this class, relating to abstract item fails :'(
    
    # # main == the one you put on the Char Sheet
    # main = models.ForeignKey(
    #     "AbstractItem",#Check if you can point to an abstract?
    #     related_name='shared_proficiencies_main',
    #     blank=False)
    # other = models.ForeignKey(
    #     "AbstractItem",#Check if you can point to an abstract?
    #     related_name='shared_proficiencies_other',
    #     blank=False)
