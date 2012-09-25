from django.contrib import admin

from player.models.accounts import AccountProfile
from player.models.accounts import Preference
from player.models.campaigns import Campaign
from player.models.players import Player

class AccountProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)


admin.site.register(AccountProfile)
admin.site.register(Preference)
admin.site.register(Campaign)
admin.site.register(Player)
