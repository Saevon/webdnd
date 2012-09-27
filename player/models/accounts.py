from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from player.constants.account import PREFERENCES
from player.models.abstract import AbstractPlayerModel
from shared.views import ModelMixin


class UserMixin(ModelMixin):
    """
    Adds new fields to the Django user
    """
    model = User

    friends = models.ManyToManyField(
        'self',
        blank=False,
        null=False
    )
    desc = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )

    @property
    def name(self):
        return unicode(self)


class Preference(AbstractPlayerModel):
    """
    A Preference for a webdnd Account
    """

    class Meta(AbstractPlayerModel.Meta):
        unique_together = ('user', 'preference')

    preference = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=PREFERENCES,
        blank=False,
        null=False
    )
    value = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )
    user = models.ForeignKey(
        User,
        related_name='preferences',
        blank=False,
        null=False
    )


