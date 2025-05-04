from django.contrib import admin
from .models import Users
from django.contrib.auth.admin import UserAdmin



@admin.register(Users)
class UserSite(UserAdmin):
    list_display = ['first_name', 'last_name', 'email', 'username', 'usertype', 'is_staff', 'is_superuser']
    list_display_links = ['first_name', 'last_name', 'email', 'username']
    list_per_page = 25
    search_fields = [
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__username",
    ]
    list_filter = ['email', 'username', 'is_staff', 'is_active']
    fieldsets = (
        
        ('User-info', {
            'fields': ('first_name', 'last_name', 'email', 'username', 'profile')
        }),
        
        ('User-permissions', {
            'fields': ('usertype', 'is_staff', 'is_superuser', 'is_active'),
        }),
        
        ('User-authentication', {
            'fields': ('password', 'reset_password'),
        }),
        ('others', {
            'fields': ('last_login', 'created_at', 'updated_at'),
        }),
    )


