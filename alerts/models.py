from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, AnonymousUser

import datetime

class Alert(models.Model):

    class Meta:
        app_label = 'alerts'

    owner = models.CharField(
        max_length=settings.STND_CHAR_LIMIT,
        blank=False,
        null=False
    )
    expiry = models.DateTimeField(blank=False, null=False);

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
        Alert.objects.filter(owner=owner).delete()

    @staticmethod
    def show_all(owner):
        alerts = Alert.objects.filter(owner=owner)

    @staticmethod
    def get_alerts(owner):
        alerts = Alert.objects.filter(owner=owner)
        showing = [alert.copy() for alert in alerts]
        alerts.delete()

        return showing

    def save(self, *args, **kwargs):
        self.expiry = datetime.datetime.now() + datetime.timedelta(
            # Days then seconds
            0, settings.SESSION_COOKIE_AGE
        )
        return super(Alert, self).save(*args, **kwargs)

    def copy(self):
        return Alert(
            owner=self.owner,
            title=self.title,
            prefix=self.prefix,
            text=self.text,
            level=self.level
        )

    def __unicode__(self):
        return '%s %s%s' % (
            self.title or self.prefix,
            '~ ' if self.text else '',
            self.text
        )

    def details(self):
        return {
            'title': self.title,
            'prefix': self.prefix,
            'text': self.text,
            'level': self.level,
        }


