from django.db import models

from player.models.account import Account
from dnd.constants.database import ADMIN_CHAR_CUTOFF, STND_CHAR_LIMIT, STND_ID_CHAR_LIMIT
from dnd.constants.references import SOURCE_DOC_PATH
from dnd.models.abstract import AbstractLibraryModel

class Reference(AbstractLibraryModel):
    """
    A D&D reference.
    """

    pages = models.CommaSeparatedIntegerField(
        max_length=STND_CHAR_LIMIT,
        blank=False,
        null=False)
    source = models.ForeignKey(
        Source,
        related_name='references',
        blank=False,
        null=False)
    added_by = models.ForeignKey(
        Account,
        related_name='references',
        blank=False,
        null=False)

    def __unicode__(self):
        return u"%(pages)s from %(source)s" % {
            'source': str(self.source),
            'pages': self.pages[:ADMIN_CHAR_CUTOFF]
        }

class Source(AbstractLibraryModel):
    """
    A D&D Source such as a book, or homebrew text
    """
    details = models.TextField(blank=True)
    authors = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
    added_by = models.ForeignKey(
        Account,
        related_name='sources',
        blank=False,
        null=False)
    document = models.FilePathField(
        path=SOURCE_DOC_PATH,
        recursive=True,
        blank=True,
        null=True)
    # if these are filled in its a book otherwise Homebrew
    title = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
    publisher = models.CharField(
        max_length=STND_CHAR_LIMIT,
        blank=True)
