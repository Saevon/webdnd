from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from player.constants.account import PREFERENCES
from player.models.abstract import AbstractPlayerModel


class AccountProfile(AbstractPlayerModel):
    """
    A webdnd Account
    """
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.user.get_full_name();


class Preference(AbstractPlayerModel):
    """
    A Preference for a webdnd Account
    """

    class Meta(AbstractPlayerModel.Meta):
        unique_together = ('user', 'preference')

    preference = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=PREFERENCES,
        blank=False)
    value = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False)
    user = models.ForeignKey(
        AccountProfile,
        related_name='preferences',
        blank=False,
        null=False)



@receiver(post_save, sender=User)
def add_profile(sender, instance, created, raw, **kwargs):
    if created:
        AccountProfile.objects.create(user=instance)
