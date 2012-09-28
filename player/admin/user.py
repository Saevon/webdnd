from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from player.models.accounts import Preference

class PreferenceInline(admin.TabularInline):
    model = Preference

    fields = ('preference', 'value')
    ordering = ('preference',)
    fk_name = 'user'

    max_num = 1000
    extra = 1

class AccountAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('friends',)
    inlines = [PreferenceInline,]

