from django.db import models

from library.models.abstract import AbstractLibraryModel
from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT

class LibraryAccount(AbstractLibraryModel):
    """
    A webdnd library account.
    """
    
    name = models.CharField(blank=False, max_length=STND_CHAR_LIMIT)
    # TODO: finish making this

    def __unicode__(self):
        return u"%s" %(self.name)
