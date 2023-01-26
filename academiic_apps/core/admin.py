from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from academiic_apps.core.models import Staff
from .models import *


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_faculty')
    search_fields = ('email', )
    ordering = ('email',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Staff, AccountAdmin)

