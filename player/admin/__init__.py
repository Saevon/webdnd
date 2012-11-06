from django.contrib.auth.models import User
from django.contrib import admin

from webdnd.player.admin.user import AccountAdmin, PreferenceAdmin
from webdnd.player.admin.campaigns import CampaignAdmin
from webdnd.player.admin.campaigns import PlayerAdmin
from webdnd.player.admin.characters import CharacterAdmin
from webdnd.player.models.accounts import Preference
from webdnd.player.models.alignment import Alignment
from webdnd.player.models.campaigns import Campaign
from webdnd.player.models.campaigns import Player
from webdnd.player.models.characters import Character



# Adds user customizations
admin.site.unregister(User)
admin.site.register(User, AccountAdmin)

admin.site.register(Preference, PreferenceAdmin)

admin.site.register(Campaign, CampaignAdmin)
admin.site.register(Player, PlayerAdmin)

admin.site.register(Character, CharacterAdmin)
admin.site.register(Alignment)

