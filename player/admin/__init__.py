from django.contrib import admin

from player.models.accounts import Preference
from player.models.campaigns import Campaign
from player.models.players import Player


admin.site.register(Preference)
admin.site.register(Campaign)
admin.site.register(Player)
