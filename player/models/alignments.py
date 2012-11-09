from django.db import models
from django.conf import settings

from webdnd.player.models.abstract import AbstractPlayerModel


class Alignment(AbstractPlayerModel):

    # Both on a 0-100 scale
    align_moral = models.IntegerField(default=50, blank=False, null=False)
    align_order = models.IntegerField(default=50, blank=False, null=False)

    def __unicode__(self):
        return Alignment.to_str(self.align_moral, self.align_order)

    def set_str(self, string):
        '''
        Highly lossy, only use this for starting values, or when the user
        doesn't want the more percise alignment.
        '''
        self.align_moral, self.align_order = Alignment.to_tuple(string)

    @staticmethod
    def to_str(moral, order):
        if moral > 70:
            if order > 70:
                return u'Lawful Good'
            elif order < 70:
                return u'Chaotic Good'
            else:
                return u'True Good'
        elif moral < 30:
            if order > 70:
                return u'Lawful Evil'
            elif order < 70:
                return u'Chaotic Evil'
            else:
                return u'True Evil'
        else:
            if order > 70:
                return u'True Lawful'
            elif order < 70:
                return u'True Chaotic'
            else:
                return u'True Neutral'

    @staticmethod
    def to_tuple(string):
        string = string.lower()
        order = 50
        moral = 50

        if u'good' in string:
            moral = 70
        elif u'evil' in string:
            moral = 30

        if u'lawful' in string:
            order = 70
        elif u'chaotic' in string:
            order = 30

        # True/Neutral keeps the value at 50 .: no change

        return (moral, order)
        
