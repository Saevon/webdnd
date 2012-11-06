from django.db import models
from django.conf import settings

from webdnd.player.models.abstract import AbstractPlayerModel
from webdnd.player.models.alignment import Alignment
from webdnd.player.models.campaign import Player


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
    # Nickname, what to actually show on the chat
    nick = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )

    STATUSES = (
        ('main', 'Main'),
        ('dead', 'Dead'),
        ('unsd', 'Unused'),
        ('comp', 'Companion'),
    )
    status = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=STATUSES,
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


    def __unicode__(self):
        return self.name






