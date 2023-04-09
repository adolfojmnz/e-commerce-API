from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = [
        'username', 'email', 'first_name', 'last_name', 'bio', 'birthdate',
        'password', 'group', 'user_permissions', 'is_staff', 'is_active',
        'is_superuser', 'last_login', 'date_joined',
    ]


admin.site.register(User)
