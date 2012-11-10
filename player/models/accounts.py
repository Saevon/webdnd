from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from webdnd.player.models.abstract import AbstractPlayerModel
from shared.views import ModelMixin

class UserMixin(ModelMixin):
    """
    Adds new fields to the Django user
    """
    model = User

    friends = models.ManyToManyField(
        'self',
        symmetrical=True,
        blank=True,
        null=False
    )

    @property
    def name(self):
        if not self.last_name and not self.first_name:
            return unicode(self.username)
        return u'%s %s' % (self.last_name, self.first_name)


class TypeManager(models.Manager):
    '''
    A Manager that returns only objects of the given type
    '''

    def __init__(self, *args, **kwargs):
        self.type = kwargs.pop('type', None)
        super(TypeManager, self).__init__(*args, **kwargs)

    def get_query_set(self):
        qs = super(TypeManager, self).get_query_set()
        if not self.type is None:
            qs = qs.filter(type=self.type)

        return qs


class BasePreference(AbstractPlayerModel):
    '''
    A Preference for any object
    '''

    class Meta(AbstractPlayerModel.Meta):
        unique_together = ('owner', 'type', 'preference')
        db_table = 'player_preference'
        # Make sure this doesn't try to make a table
        abstract = True

    TYPES = []
    TYPES_TO_CLASS = {}

    value = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )

    type = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=TYPES,
        blank=False,
        null=False
    )


    # See this method for the other model fields
    @staticmethod
    def generate_fk_class(model, preferences, main=False):
        '''
        Used to generate wrapper classes for different preference owner TYPES
            NOTE: add the class_name as a str to the TYPES tuple
        '''
        BasePreference.TYPES.append((model.__name__.lower(), model.__name__))

        BasePreference.TYPES_TO_CLASS[model.__name__.lower()] = model

        Pref = type(model.__name__ + 'Preference', (BasePreference,), {
            'Meta': type('Meta', (BasePreference.Meta, object,), {'managed': main}),
            '__module__': BasePreference.__module__,

            # Ensuring that the type is used properly
            'TYPE': model.__name__.lower(),
            'TYPE_DISPLAY': model.__name__,
            'objects': TypeManager(type=model.__name__.lower()),

            # Fields
            'PREFERENCES': preferences,
            'PREF_TO_DISPLAY': dict(preferences),
            'preference': models.CharField(
                max_length=settings.STND_ID_CHAR_LIMIT,
                choices=preferences,
                blank=False,
                null=False
            ),
            'owner': models.ForeignKey(
                model,
                related_name='preferences',
                blank=False,
                null=False
            ),
        })

        return Pref

    def __unicode__(self):
        return u'(%s) %s' % (self.get_preference_display(), self.value)

    def get_preference_display(self):
        return self.PREF_TO_DISPLAY.get(self.preference, '?: ' + self.preference)

    def get_type_display(self):
        return self.TYPE_DISPLAY

    def save(self, *args, **kwargs):
        if not self.TYPE is None:
            self.type = self.TYPE

        return super(BasePreference, self).save(*args, **kwargs)


class FakeModel(AbstractPlayerModel):
    '''
    A Fake Model that is used to make Preference valid
    '''
    class Meta(AbstractPlayerModel.Meta):
        managed = False


# Wrapper to be able to get all preferences
# Also creates the table
Preference = BasePreference.generate_fk_class(FakeModel, tuple(), main=True)


USER_PREFERENCES = (
)
UserPreference = BasePreference.generate_fk_class(User, USER_PREFERENCES)

