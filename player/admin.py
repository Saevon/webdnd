from django.contrib import admin

from player.models.account import AccountProfile
from player.models.account import Preference
from player.models.campaign import Campaign
from player.models.players import Player


admin.site.register(AccountProfile)
admin.site.register(Preference)
admin.site.register(Campaign)
admin.site.register(Player)

