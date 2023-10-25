from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'last_login', 'date_joined', 'is_active')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    list_display_links = ('id', 'email', 'first_name', 'last_name')


admin.site.register(Account, AccountAdmin)
