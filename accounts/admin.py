from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Contact  # Only import if it exists

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

# Only register Contact if you have it
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'created_at')
    ordering = ('-created_at',)

    def has_delete_permission(self, request, obj=None):
        return True
