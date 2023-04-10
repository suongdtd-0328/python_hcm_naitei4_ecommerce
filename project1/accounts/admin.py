from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.translation import gettext as _


class AccountAdmin(UserAdmin):
    list_display = (_('email'), _('username'), _('first_name'),
                    _('last_name'), _('last_login'), _('date_joined'), _('is_active'))

    list_display_links = (_('email'), _('username'),
                          _('first_name'), _('last_name'))
    readonly_fields = (_('last_login'), _('date_joined'))
    ordering = (_('-date_joined'),)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
