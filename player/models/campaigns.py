from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from webdnd.player.constants.campaign import ROLEPLAYING_SYSTEMS
from webdnd.player.models.abstract import AbstractPlayerModel
import random
import string


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

    rp_system = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=ROLEPLAYING_SYSTEMS,
        blank=False,
        null=False
    )

    def __unicode__(self):
        return u'%s' % self.name


KEY_LENGTH = 64

class Game(models.Model):

    ALLOWED_CHARS = string.ascii_letters + string.digits + '~!@$%^*()_-,.:|{}[]'

    class Meta:
        app_label = 'player'
        unique_together = ('user', 'campaign')

    user = models.OneToOneField(
        User,
        related_name='game',
        blank=False,
        null=False
    )
    campaign = models.ForeignKey(
        Campaign,
        related_name='game',
        blank=False,
        null=False
    )
    key = models.CharField(
        max_length=KEY_LENGTH,
        blank=False,
        null=True
    )

    def new_key(self):
        self.key = ''.join([random.choice(Game.ALLOWED_CHARS) for i in range(KEY_LENGTH)])



