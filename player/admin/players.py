from django.contrib import admin

from webdnd.player.models.players import Player
from webdnd.shared.admin import fk_link


class PlayerAdmin(admin.ModelAdmin):
    model = Player 
    fields = ('user', 'campaign', 'cur_char', 'can_dm', 'is_spectator', 'color',)

    list_display = ('campaign', fk_link('user'), 'can_dm', 'is_spectator',)
    list_filter = ('user', 'campaign',)

    search_fields = ('campaign__name', 'user__username', 'user__first_name', 'user__last_name',)
    ordering = ('campaign', 'user',)


