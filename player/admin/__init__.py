from django.contrib.auth.models import User
from django.contrib import admin

from webdnd.player.admin.user import AccountAdmin
from webdnd.player.models.accounts import Preference
from webdnd.player.models.alignment import Alignment
from webdnd.player.models.campaigns import Campaign
from webdnd.player.models.players import Character
from webdnd.player.models.players import Player


# Adds user customizations
admin.site.unregister(User)
admin.site.register(User, AccountAdmin)

admin.site.register(Preference)
admin.site.register(Campaign)
admin.site.register(Player)
admin.site.register(Character)
admin.site.register(Alignment)

