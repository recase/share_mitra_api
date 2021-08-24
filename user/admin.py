from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'first_name',
         'middle_name', 'last_name', )}),
        ('permissions', {'fields': ('is_active',
         'role', 'user_permissions', 'groups')})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2')}),
        ('personnel', {'fields': ('first_name', 'middle_name', 'last_name')}),
        ('permissions', {'fields': ('role', 'user_permissions', 'groups')})
    )
    list_display = ('id', 'email', 'first_name',
                    'last_name', 'role', 'date_joined',)
    ordering = ('id', 'email', 'first_name', 'last_name',)
    list_filter = ('role',)
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(User, CustomUserAdmin)
