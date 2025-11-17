from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Contact

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')
    ordering = ('-created_at',)

    def has_delete_permission(self, request, obj=None):
        return True
