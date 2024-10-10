from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SpamEmail

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)
    search_fields = ('username', 'email', 'first_name', 'last_name')

    # Define fieldsets without duplicating fields from UserAdmin
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    
    # Add additional fields as needed, ensuring there are no duplicates
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')}),
    )

class SpamEmailAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'subject', 'detected_on')
    list_filter = ('detected_on', 'sender')
    search_fields = ('sender', 'subject')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SpamEmail, SpamEmailAdmin)
