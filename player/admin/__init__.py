from django.contrib.auth.models import User
from django.contrib import admin

from player.admin.user import AccountAdmin
from player.models.accounts import Preference
from player.models.campaigns import Campaign
from player.models.players import Player


# Adds user customizations
admin.site.unregister(User)
admin.site.register(User, AccountAdmin)

admin.site.register(Preference)
admin.site.register(Campaign)
admin.site.register(Player)


