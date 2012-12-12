from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User

from webdnd.player.models.abstract import AbstractPlayerModel
from webdnd.shared.forms import AlignmentField
from webdnd.player.modifier_obj import ModField, ReadOnlyModField, NumModField, FilteredModField
from webdnd.shared.utils.decorators import dirty_cache


class CharactersManager(models.Manager):
    '''
    A Manager that returns only objects of the given type
    '''

    def visible(self, user):
        '''
        Returns any characters that the given user can see
        '''
        qs = super(CharactersManager, self).get_query_set()
        return qs.filter(
            Q(players__campaign__owner=user)
            | Q(players__can_dm=True, players__user=user)
        )


class Character(AbstractPlayerModel):
    '''
    A character, contains any non-system specific details
    that a character requires.
    '''

    objects = CharactersManager()

    user = models.ForeignKey(
        User,
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

    alignment = AlignmentField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self._calculate_dirty = True
        if self.alignment:
            self.alignment_id = self.alignment.id
        return super(Character, self).save(*args, **kwargs)

    def mod_field(self):
        return {
            # Identity
            'name': ReadOnlyModField(self.name),
            'nick': ReadOnlyModField(self.nick),
            'status': ModField(self.status),

            # Description
            'age': NumModField(self.age),
            'backstory': ReadOnlyModField(self.backstory),
            'deity': ReadOnlyModField(self.deity),
            'description': ReadOnlyModField(self.description),
            'gender': ModField(self.gender),
            'hair_color': ModField(self.hair_color),
            'weight': NumModField(self.weight),

            # Alignment
            'align_moral': NumModField(self.alignment.align_moral),
            'align_order': NumModField(self.alignment.align_order),
        }

    @dirty_cache
    def calculate(self):
        '''
        Applies any modifiers to the character returning the final values
        '''
        # TODO: no actual modifiers to use right now
        return self.mod_field()




