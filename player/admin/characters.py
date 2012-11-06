from django.contrib import admin

from webdnd.player.models.characters import Character
from webdnd.shared.admin import fk_link



class CharacterAdmin(admin.ModelAdmin):
    model = Character
    fieldsets = (
        ('Identity', {'fields': ('user', 'name', 'nick', 'status')}),
        ('Description', {'fields': ('description', 'age', 'eye_color', 'hair_color', 'gender', 'weight')}),
        ('Personality', {'fields': ('alignment', 'persoa_id')})
    )

    list_display = ('name', 'status', 'nick', 'alignment', fk_link('user'))
    list_filter = ('user', 'status', 'alignment')
    list_editable = ('status',)

    search_fields = ('user', 'name', 'nick', 'status', 'alignment')
