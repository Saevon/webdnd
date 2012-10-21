from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from webdnd.player.models.abstract import AbstractPlayerModel
from webdnd.player.models.alignment import Alignment
from webdnd.player.models.campaigns import Campaign
from webdnd.player.constants.constants import CHARACTER_STATUSES


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

    # The current character you are playing
    cur_char = models.ForeignKey(
        'Character',
        # TODO: does this mean it is disabled?? it should be
        related_name='-',
        blank=True,
        null=True
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

class Character(AbstractPlayerModel):
    '''
    A character in a campaign, contains any non-system specific details
    that a character requires.
    '''

    player = models.ForeignKey(
        Player,
        related_name='characters',
        blank=False,
        null=False
    )

    name = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )

    status = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=CHARACTER_STATUSES,
        blank=False,
        null=False
    )

    ##############################################
    # Description and Backstory
    ##############################################
    backstory = models.TextField(blank=True, null=False)
    deity = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=True,
        null=False
    )
    age = models.PositiveIntegerField(blank=True, null=True)

    description = models.TextField(blank=True, null=False)
    eye_color = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=True,
        null=False
    )
    hair_color = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=True,
        null=False
    )
    gender = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=True,
        null=False
    )
    # in what measurement?
    weight = models.PositiveIntegerField(blank=True, null=True)

    # Optional id that lets you store a personality (through PersOA)
    # NULL means you're not using it, and its disabled by default
    persoa_id = models.PositiveIntegerField(blank=True, null=True)

    alignment = models.OneToOneField(
        Alignment,
        related_name='character',
        blank=False,
        null=False
    )







