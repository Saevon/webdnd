from django.db import models
from django.conf import settings

from player.models.abstract import AbstractPlayerModel
from player.models.accounts import AccountProfile
from player.models.campaigns import Campaign


class Player(AbstractPlayerModel):
    """
    A User to Campaign mapping
    """

    class Meta(AbstractPlayerModel.Meta):
        unique_together = ('account', 'campaign')

    # M2M Mapping
    account = models.ForeignKey(
        AccountProfile,
        related_name='campaigns',
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

