from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from webdnd.player.models.abstract import AbstractPlayerModel
from webdnd.player.models.campaigns import Campaign
from webdnd.player.constants.constants import TERMINAL_MAX_HIST_LEN


class HistoryLog(AbstractPlayerModel):

    class Meta(AbstractPlayerModel.Meta):
        unique_together = ('cmd', 'user', 'campaign',)
        ordering = ('updated',)

    counter = models.PositiveIntegerField(blank=False, null=False, default=0)
    updated = models.DateTimeField(auto_now=True)
    
    cmd = models.CharField(
        max_length=TERMINAL_MAX_HIST_LEN,
        blank=False,
        null=False
    )

    user = models.ForeignKey(
        User,
        related_name='history_cmd',
        blank=False,
        null=False
    )
    # NULL campaign == user global history
    campaign = models.ForeignKey(
        Campaign,
        related_name='history_cmd',
        blank=True,
        null=True
    )

    @staticmethod
    def get_cmds(uid, cid=None, limit=None):
        logs = HistoryLog.objects.filter(user__id=uid)
        if not cid is None:
            logs = logs.filter(campaign__id=cid)

        logs = logs.order_by('updated')

        if not limit is None:
            logs = logs[:limit]
        return logs.all()

    @staticmethod
    def new(cmd, uid, cid=None):
        args = {
            'cmd': cmd,
            'user__id': uid,
        }
        defaults = {
            'cmd': cmd,
            'user_id': uid,
            'campaign_id': cid,
        }
        if not cid is None:
            log, created = HistoryLog.objects.get_or_create(campaign__id=cid, defaults=defaults, **args)
            log.counter += 1
            log.save()

        # always make sure to update the global list
        log, created = HistoryLog.objects.get_or_create(defaults=defaults, **args)
        log.counter += 1
        log.save()

        return log




