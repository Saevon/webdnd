from django.contrib import admin

from webdnd.alerts.models import Alert


class AlertAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Message', {'fields': ('title', 'level', 'prefix', 'text')}),
        ('Options', {'fields': ('owner',)}),
    )

    list_display = ('title', 'level', 'text', 'owner')
    list_display_links = ('owner', 'title')

    search_fields = ('title', 'prefix', 'text')
    list_filter = ('owner', 'level')
    ordering = ('owner', 'level')

    list_select_related = True
    save_as = True

    class Media:
        css = {
            "all": ("bonus.css",)
        }
        js = ("bonus.js",)

    # TODO: mass changes for:
    #       level and owner
    # Mass message creation, e.g new message per user

admin.site.register(Alert, AlertAdmin)
