from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from webdnd.player.models.accounts import UserPreference
from webdnd.shared.admin import fk_link


class PreferenceInline(admin.TabularInline):
    fields = ('preference', 'value')
    ordering = ('preference',)
    fk_name = 'owner'

    max_num = 1000
    extra = 1


class PreferenceAdmin(admin.ModelAdmin):
    fields = ('owner', 'preference', 'value')

    list_display = ('preference', 'value', fk_link('owner'))
    list_editable = ('value',)
    list_filter = ('preference', 'owner')

    save_as = True

    search_fields = ('preference', 'owner', 'value')
    ordering = ('owner',)


class UserPreferenceAdmin(PreferenceAdmin):
    model = UserPreference


class AccountAdmin(UserAdmin):
    UserAdmin.form.base_fields['friends'] = forms.ModelMultipleChoiceField(
        queryset=User.objects.all()
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Friends', {'fields': ('friends',)}),
    )
    filter_horizontal = ('friends',)

    class UserPreferenceInline(PreferenceInline):
        model = UserPreference

    inlines = (UserPreferenceInline,)

