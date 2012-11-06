from django.contrib import admin

from webdnd.player.models.campaigns import Campaign
from webdnd.player.models.campaigns import Player
from webdnd.shared.admin import fk_link


class CampaignAdmin(admin.ModelAdmin):
    model = Campaign
    fields = ('owner', 'name', 'rp_system')

    list_display = ('name', 'rp_system', fk_link('owner'))
    list_filter = ('rp_system', 'owner')

    search_fields = ('name', 'owner__username', 'owner__first_name', 'owner__last_name', 'rp_system')
    ordering = ('name',)


class PlayerAdmin(admin.ModelAdmin):
    model = Player
    fieldsets = (
        ('Mapping', {'fields': ('user', 'campaign')}),
        ('Options', {'fields': ('can_dm', 'is_spectator', 'color')}),
        ('Characters', {'fields': ('characters',)}),
    )

    list_display = ('__unicode__', fk_link('campaign'), fk_link('user'), 'can_dm', 'is_spectator',)
    list_filter = ('user', 'campaign',)

    search_fields = ('campaign__name', 'user__username', 'user__first_name', 'user__last_name',)
    ordering = ('campaign', 'user',)
