from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'is_admin', 'is_attendee', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_attendee', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles', {'fields': ('is_admin', 'is_attendee')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)
    ordering = ('date',)

admin.site.register(CustomUser, CustomUserAdmin)
