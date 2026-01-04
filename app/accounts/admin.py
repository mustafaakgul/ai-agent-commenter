from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from app.accounts.models import User, UserProfile, EmailVerification, PasswordResetToken, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_email_verified', 'is_active', 'date_joined']
    list_filter = ['is_email_verified', 'is_phone_verified', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth')}),
        ('Verification Status', {'fields': ('is_email_verified', 'is_phone_verified')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'job_title', 'location', 'language', 'created']
    list_filter = ['language', 'receive_notifications', 'receive_newsletter', 'created']
    search_fields = ['user__email', 'user__username', 'company', 'job_title', 'location']
    raw_id_fields = ['user']

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Profile Information', {'fields': ('bio', 'avatar', 'company', 'job_title', 'location', 'website')}),
        ('Social Media', {'fields': ('twitter', 'linkedin', 'github')}),
        ('Preferences', {'fields': ('language', 'timezone', 'receive_notifications', 'receive_newsletter')}),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_used', 'expires_at', 'created']
    list_filter = ['is_used', 'created', 'expires_at']
    search_fields = ['user__email', 'token']
    raw_id_fields = ['user']
    readonly_fields = ['token', 'created', 'updated']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_used', 'expires_at', 'created']
    list_filter = ['is_used', 'created', 'expires_at']
    search_fields = ['user__email', 'token']
    raw_id_fields = ['user']
    readonly_fields = ['token', 'created', 'updated']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'ip_address', 'created']
    list_filter = ['activity_type', 'created']
    search_fields = ['user__email', 'activity_type', 'ip_address', 'description']
    raw_id_fields = ['user']
    readonly_fields = ['created', 'updated']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
