from django.db import models

from game.models.accounts import Account
from dnd.config.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from library.models.abstract import AbstractLibraryModel
from library.models.references import Reference
from game.models.accounts import Account

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
    reference = models.ForeignKey(
        Reference,
        blank=False,
        null=False)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(
        Account,
        blank=False,
        null=False)
    copyrighted = models.BooleanField(default=False, null=False)

    def __unicode__(self):
        return unicode(self.title)
