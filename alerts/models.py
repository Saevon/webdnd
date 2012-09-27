from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from django.db import models

import datetime


class Alert(models.Model):
    """
    A session based alert, this follows any logged in or logged out user
    """

    class Meta:
        app_label = 'alerts'

    owner = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )
    expiry = models.DateTimeField(blank=False, null=False);
    closable = models.BooleanField(
        default=False,
        blank=False,
        null=False
    )

    # Actual message details
    title = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=True,
        null=False
    )
    prefix = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=True,
        null=False
    )
    text = models.TextField(
        verbose_name='message',
        blank=True,
        null=False
    )
    level = models.CharField(
        max_length=settings.STND_ID_CHAR_LIMIT,
        choices=settings.ALERT_LEVELS,
        default=settings.ALERT_DEFAULT_LEVEL,
        blank=False,
        null=False
    )

    @staticmethod
    def clear(owner):
        """
        Removes all the alerts for the given owner
        """
        Alert.objects.filter(owner=owner).delete()

    @staticmethod
    def get_alerts(owner):
        """
        Deletes all the alerts for the owner, returning them
          If you only wish to see a list of the alerts the owner has
          do NOT use this function. Only use this if you are consuming
          the alerts.
        """
        alerts = Alert.objects.filter(owner=owner)
        showing = [alert.copy() for alert in alerts]
        alerts.delete()

        return showing

    def __unicode__(self):
        """
        Returns a string representation of the alert
        """
        return '%s %s%s' % (
            self.title or self.prefix,
            '~ ' if self.text else '',
            self.text
        )

    def save(self, *args, **kwargs):
        """
        Saves the current model, expiry is automatically passed in as *now*
        you cannot pass it in yourself.
        """
        self.expiry = datetime.datetime.now() + datetime.timedelta(
            # Days then seconds
            0, settings.SESSION_COOKIE_AGE
        )
        return super(Alert, self).save(*args, **kwargs)

    def copy(self):
        """
        Returns a new Alert that is a copy of self
        """
        return Alert(
            owner=self.owner,
            title=self.title,
            prefix=self.prefix,
            text=self.text,
            level=self.level,
            closable=self.closable,
        )

    def details(self):
        """
        Returns the details needed to show this alert
        """
        return {
            'title': self.title,
            'prefix': self.prefix,
            'text': self.text,
            'level': self.level,
            'closable': self.closable,
        }


