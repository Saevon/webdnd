from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms

from webdnd.player.models.accounts import Preference


class PreferenceInline(admin.TabularInline):
    model = Preference

    fields = ('preference', 'value')
    ordering = ('preference',)
    fk_name = 'user'

    max_num = 1000
    extra = 1

class AccountAdmin(UserAdmin):
    UserAdmin.form.base_fields['friends'] = forms.ModelMultipleChoiceField(
        queryset=User.objects.all()
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Friends', {'fields': ('friends',)}),
    )
    filter_horizontal = ('friends',)

    inlines = [PreferenceInline,]

