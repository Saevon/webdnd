from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from webdnd.player.models.abstract import AbstractPlayerModel
from webdnd.player.models.campaigns import Campaign


class Player(AbstractPlayerModel):
    """
    A User to Campaign mapping
    """

    class Meta(AbstractPlayerModel.Meta):
        unique_together = ('user', 'campaign')

    # M2M Mapping between users and campaigns
    user = models.ForeignKey(
        User,
        related_name='players',
        blank=False,
        null=False
    )
    campaign = models.ForeignKey(
        Campaign,
        related_name='players',
        blank=False,
        null=False
    )

    # To permit another player to DM for you
    can_dm = models.BooleanField(default=False)

    # For people to spectate
    is_spectator = models.BooleanField(default=False)

    @property
    def name(self):
        return unicode(self)

    def __unicode__(self):
        return u'%s' % (self.user.name)





