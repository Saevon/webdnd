from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from webdnd.player.models.abstract import AbstractPlayerModel
from webdnd.player.models.characters import Character
from webdnd.shared.forms import ColorField


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

    characters = models.ManyToManyField(
        Character,
        related_name='players',
        blank=True,
        null=True
    )

    # To permit another player to DM for you
    can_dm = models.BooleanField(default=False)

    # For people to spectate
    is_spectator = models.BooleanField(default=False)

    # Color for this user
    color = ColorField(blank=True, null=True)

    @property
    def name(self):
        return u'%s' % (self.user.name)

    def __unicode__(self):
        return u'(%s) %s' % (self.campaign, self.user.name)


