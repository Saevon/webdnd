from django.db import models

from library.models.abstract import AbstractLibraryModel
from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.sources import REFERENCE_TYPES

class Source(AbstractLibraryModel):
    """
    A D&D reference.
    """
    
    reference_type = models.CharField(
        max_length=STND_ID_CHAR_LIMIT,
        choices=REFERENCE_TYPES,
        blank=False)
    citation = models.TextField(blank=False)
    
    def __unicode__(self):
        return self.citation[:20]
