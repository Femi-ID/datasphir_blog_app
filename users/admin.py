from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'username', 'is_active', 'email', 'phone_number', 'created_at')
    list_filter = ('first_name', 'last_name', 'username', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')