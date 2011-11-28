from django.db import models

from lib.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.abstract import AbstractLibraryModel
from library.models.sources import Source
from library.models.accounts import LibraryAccount

class AbstractLibraryEntity(AbstractLibraryModel):
    """
    A D&D entity in the library.
    """
    
    class Meta(AbstractLibraryModel.Meta):
        abstract = True

    title = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=False,
        unique=True)
    reference = models.ForeignKey(Source, blank=False)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(LibraryAccount, blank=False)
    copyrighted = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.title)
