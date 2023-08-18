from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'last_login',
        'is_active',
        'is_staff',
    )
    ordering = ('date_joined',)
    search_fields = ('email',)
