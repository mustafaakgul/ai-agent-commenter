from django.contrib.auth.models import AbstractUser
from django.db import models

from app.core.models.base_model import BaseModel


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    is_email_verified = models.BooleanField(default=False, verbose_name="Email Verified")
    is_phone_verified = models.BooleanField(default=False, verbose_name="Phone Verified")

    # Make email the primary login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def __str__(self):
        return self.email


class UserProfile(BaseModel):
    """
    Extended user profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biography")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    company = models.CharField(max_length=100, blank=True, verbose_name="Company")
    job_title = models.CharField(max_length=100, blank=True, verbose_name="Job Title")
    website = models.URLField(blank=True, verbose_name="Website")
    location = models.CharField(max_length=100, blank=True, verbose_name="Location")

    # Social media links
    twitter = models.URLField(blank=True, verbose_name="Twitter Profile")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn Profile")
    github = models.URLField(blank=True, verbose_name="GitHub Profile")

    # Preferences
    language = models.CharField(max_length=10, default='en', verbose_name="Preferred Language")
    timezone = models.CharField(max_length=50, default='UTC', verbose_name="Timezone")
    receive_notifications = models.BooleanField(default=True, verbose_name="Receive Notifications")
    receive_newsletter = models.BooleanField(default=False, verbose_name="Receive Newsletter")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile of {self.user.email}"


class EmailVerification(BaseModel):
    """
    Email verification token management
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.CharField(max_length=255, unique=True, verbose_name="Verification Token")
    is_used = models.BooleanField(default=False, verbose_name="Is Used")
    expires_at = models.DateTimeField(verbose_name="Expiration Time")

    class Meta:
        verbose_name = "Email Verification"
        verbose_name_plural = "Email Verifications"
        ordering = ['-created']

    def __str__(self):
        return f"Email verification for {self.user.email}"


class PasswordResetToken(BaseModel):
    """
    Password reset token management
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True, verbose_name="Reset Token")
    is_used = models.BooleanField(default=False, verbose_name="Is Used")
    expires_at = models.DateTimeField(verbose_name="Expiration Time")

    class Meta:
        verbose_name = "Password Reset Token"
        verbose_name_plural = "Password Reset Tokens"
        ordering = ['-created']

    def __str__(self):
        return f"Password reset for {self.user.email}"


class UserActivity(BaseModel):
    """
    Track user activities and login history
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, verbose_name="Activity Type")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    description = models.TextField(blank=True, verbose_name="Description")

    class Meta:
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"
        ordering = ['-created']

    def __str__(self):
        return f"{self.user.email} - {self.activity_type}"
