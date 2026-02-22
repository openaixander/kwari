from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # We tell Django to use email for ordering and searching
    ordering = ('email',)
    list_display = (
        'email',
        'display_name',
        'is_active',
        'is_staff',
        )
    search_fields = ('email', 'display_name',)



    # Fieldsets control how the "Edit User" page looks
    # we remove 'username' and add 'display_name'

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('display_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'display_name', 'password', 'is_active', 'is_staff'),
        }),
    )