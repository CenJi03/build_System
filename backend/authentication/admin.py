from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, LoginAttempt, UserActivity, TOTPDevice

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser model
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_verified', 'two_factor_enabled')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 'two_factor_enabled')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Add two_factor_enabled to fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio', 'birth_date')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Authentication'), {'fields': ('is_verified', 'two_factor_enabled')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add fields for user creation in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    # Make email a required field in admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'email' in form.base_fields:
            form.base_fields['email'].required = True
        return form
    
@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """
    Admin configuration for LoginAttempt model
    """
    list_display = ('user', 'ip_address', 'successful', 'timestamp')
    list_filter = ('successful', 'timestamp')
    search_fields = ('user__username', 'ip_address')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserActivity model
    """
    list_display = ('user', 'activity_type', 'ip_address', 'timestamp')
    list_filter = ('activity_type', 'timestamp')
    search_fields = ('user__username', 'ip_address', 'activity_type')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # User activities should only be created through code, not admin
        return False

@admin.register(TOTPDevice)
class TOTPDeviceAdmin(admin.ModelAdmin):
    """
    Admin configuration for TOTPDevice model
    """
    list_display = ('user', 'name', 'confirmed', 'created_at', 'last_used')
    list_filter = ('confirmed', 'created_at')
    search_fields = ('user__username', 'name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    # Ensure security by not displaying the key in list view
    readonly_fields = ('key',)
