from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.accounts.api.views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserProfileAPIView,
    UserProfileDetailAPIView,
    ChangePasswordAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    EmailVerificationAPIView,
    UserActivityListAPIView
)


app_name = 'accounts'


urlpatterns = [
    # Authentication
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('profile', UserProfileAPIView.as_view(), name='profile'),
    path('profile/detail', UserProfileDetailAPIView.as_view(), name='profile_detail'),

    # Password Management
    path('password/change', ChangePasswordAPIView.as_view(), name='change_password'),
    path('password/reset/request', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password/reset/confirm', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),

    # Email Verification
    path('email/verify', EmailVerificationAPIView.as_view(), name='email_verify'),

    # Activity
    path('activity', UserActivityListAPIView.as_view(), name='activity'),
]
