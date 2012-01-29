from django.db import models

from player.models.accounts import Account
from dnd.constants.database import STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.models.abstract import AbstractDnDModel
from dnd.models.references import Reference
from player.models.accounts import Account

class AbstractDnDEntity(AbstractDnDModel):
    """
    A D&D entity in the dnd.
    """

    class Meta(AbstractDnDModel.Meta):
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
