from django.contrib import admin

from webdnd.player.models.players import Character
from webdnd.shared.admin import fk_link



class CharacterAdmin(admin.ModelAdmin):
    model = Character
    fieldsets = (
        ('Identity', {'fields': ('player', 'name', 'nick', 'status')}),
        ('Description', {'fields': ('description', 'age', 'eye_color', 'hair_color', 'gender', 'weight')}),
        ('Personality', {'fields': ('alignment', 'persoa_id')})
    )

    list_display = ('player', 'name', 'status', 'nick', 'alignment')
    list_filter = ('player', 'status', 'alignment')

    search_fields = ('player', 'name', 'nick', 'status', 'alignment')
