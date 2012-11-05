from django.contrib import admin

from webdnd.player.models.campaigns import Campaign
from webdnd.shared.admin import fk_link


class CampaignAdmin(admin.ModelAdmin):
    model = Campaign 
    fields = ('owner', 'name', 'rp_system')

    list_display = ('name', 'rp_system', fk_link('owner'))
    list_filter = ('rp_system', 'owner')

    search_fields = ('name', 'owner__username', 'owner__first_name', 'owner__last_name', 'rp_system')
    ordering = ('name',)
