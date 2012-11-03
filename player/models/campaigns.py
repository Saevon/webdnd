from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from webdnd.player.models.abstract import AbstractPlayerModel


class Campaign(AbstractPlayerModel):
    """
    A Campaign
    """

    owner = models.ForeignKey(
        User,
        related_name='owned_campaigns',
        blank=False,
        null=False
    )
    name = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )

    ROLEPLAYING_SYSTEMS = (
        ('dnd35', 'D&D 3.5'),
    )
    rp_system = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=ROLEPLAYING_SYSTEMS,
        blank=False,
        null=False
    )

    def __unicode__(self):
        return u'%s' % self.name





