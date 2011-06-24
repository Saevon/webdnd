from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.config.sources import REFERENCE_TYPES

class Source(models.Model):
    """
    A D&D reference.
    """
    
    reference_type = models.CharField(choices=REFERENCE_TYPES, blank=False, max_length=STND_ID_CHAR_LIMIT)
    citation = models.TextField(blank=False)
    
    def __unicode__(self):
        return self.citation[:20]
