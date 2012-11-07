from django.contrib import admin

from webdnd.player.admin.alignments import AlignmentMoralListFilter, AlignmentOrderListFilter
from webdnd.player.admin.alignments import AlignmentWidget
from webdnd.player.models.characters import Character
from webdnd.player.models.alignments import AlignmentField
from webdnd.shared.admin import fk_link



class CharacterAdmin(admin.ModelAdmin):
    model = Character
    fieldsets = (
        ('Identity', {'fields': ('user', 'name', 'nick', 'status')}),
        ('Description', {'fields': ('description', 'age', 'eye_color', 'hair_color', 'gender', 'weight')}),
        ('Personality', {'fields': ('alignment', 'persoa_id')})
    )
    formfield_overrides = {
        AlignmentField: {'widget': AlignmentWidget},
    }

    list_display = ('name', 'status', 'nick', 'alignment', fk_link('user'))
    list_filter = ('user', 'status', AlignmentMoralListFilter, AlignmentOrderListFilter)
    list_editable = ('status',)

    search_fields = ('user', 'name', 'nick', 'status', 'alignment')

