from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from webdnd.player.models.accounts import Preference
from webdnd.shared.admin import fk_link


class PreferenceInline(admin.TabularInline):
    model = Preference

    fields = ('preference', 'value')
    ordering = ('preference',)
    fk_name = 'user'

    max_num = 1000
    extra = 1

class PreferenceAdmin(admin.ModelAdmin):
    model = Preference
    fields = ('user', 'preference', 'value')

    list_display = ('preference', 'value', fk_link('user'))
    list_editable = ('value',)
    list_filter = ('preference', 'user')

    save_as = True

    search_fields = ('preference', 'user__username', 'user__first_name', 'user__last_name', 'value')
    ordering = ('user',)


class AccountAdmin(UserAdmin):
    UserAdmin.form.base_fields['friends'] = forms.ModelMultipleChoiceField(
        queryset=User.objects.all()
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Friends', {'fields': ('friends',)}),
    )
    filter_horizontal = ('friends',)

    inlines = (PreferenceInline,)

