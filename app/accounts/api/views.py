import secrets
from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.accounts.api.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer,
    UserProfileSerializer,
    UserActivitySerializer
)
from app.accounts.models import User, UserProfile, EmailVerification, PasswordResetToken, UserActivity


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # UserProfile is automatically created by signals
            # UserProfile.objects.create(user=user)

            # Create email verification token
            token = secrets.token_urlsafe(32)
            EmailVerification.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(hours=24)
            )

            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='REGISTRATION',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description='User registered successfully'
            )

            # TODO: Send verification email

            resp = {
                'status': 'true',
                'message': 'User registered successfully. Please verify your email.',
                'payload': {
                    'user': UserSerializer(user).data,
                    'verification_token': token  # Remove in production
                }
            }
            return Response(data=resp, status=status.HTTP_201_CREATED)

        resp = {
            'status': 'false',
            'message': 'Registration failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate user
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if not user.is_active:
                    resp = {
                        'status': 'false',
                        'message': 'Account is deactivated',
                        'payload': {}
                    }
                    return Response(data=resp, status=status.HTTP_403_FORBIDDEN)

                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)

                # Log activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='LOGIN',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    description='User logged in successfully'
                )

                resp = {
                    'status': 'true',
                    'message': 'Login successful',
                    'payload': {
                        'user': UserSerializer(user).data,
                        'tokens': {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                        }
                    }
                }
                return Response(data=resp, status=status.HTTP_200_OK)
            else:
                resp = {
                    'status': 'false',
                    'message': 'Invalid email or password',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_401_UNAUTHORIZED)

        resp = {
            'status': 'false',
            'message': 'Login failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')

            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            # Log activity
            UserActivity.objects.create(
                user=request.user,
                activity_type='LOGOUT',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description='User logged out successfully'
            )

            resp = {
                'status': 'true',
                'message': 'Logout successful',
                'payload': {}
            }
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            resp = {
                'status': 'false',
                'message': 'Logout failed',
                'payload': {'error': str(e)}
            }
            return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        resp = {
            'status': 'true',
            'message': 'Profile retrieved successfully',
            'payload': serializer.data
        }
        return Response(data=resp, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='PROFILE_UPDATE',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description='User updated profile'
            )

            resp = {
                'status': 'true',
                'message': 'Profile updated successfully',
                'payload': UserSerializer(user).data
            }
            return Response(data=resp, status=status.HTTP_200_OK)

        resp = {
            'status': 'false',
            'message': 'Profile update failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
            serializer = UserProfileSerializer(profile)

            resp = {
                'status': 'true',
                'message': 'Profile details retrieved successfully',
                'payload': serializer.data
            }
            return Response(data=resp, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            resp = {
                'status': 'false',
                'message': 'Profile not found',
                'payload': {}
            }
            return Response(data=resp, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            resp = {
                'status': 'true',
                'message': 'Profile details updated successfully',
                'payload': serializer.data
            }
            return Response(data=resp, status=status.HTTP_200_OK)

        resp = {
            'status': 'false',
            'message': 'Profile details update failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user

            # Check old password
            if not user.check_password(serializer.validated_data['old_password']):
                resp = {
                    'status': 'false',
                    'message': 'Old password is incorrect',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)

            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Log activity
            UserActivity.objects.create(
                user=user,
                activity_type='PASSWORD_CHANGE',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description='User changed password'
            )

            resp = {
                'status': 'true',
                'message': 'Password changed successfully',
                'payload': {}
            }
            return Response(data=resp, status=status.HTTP_200_OK)

        resp = {
            'status': 'false',
            'message': 'Password change failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            try:
                user = User.objects.get(email=email)

                # Create reset token
                token = secrets.token_urlsafe(32)
                PasswordResetToken.objects.create(
                    user=user,
                    token=token,
                    expires_at=timezone.now() + timedelta(hours=2)
                )

                # Log activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='PASSWORD_RESET_REQUEST',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    description='User requested password reset'
                )

                # TODO: Send reset email

                resp = {
                    'status': 'true',
                    'message': 'Password reset email sent successfully',
                    'payload': {
                        'reset_token': token  # Remove in production
                    }
                }
                return Response(data=resp, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                # Don't reveal if email exists or not
                resp = {
                    'status': 'true',
                    'message': 'If email exists, password reset email will be sent',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_200_OK)

        resp = {
            'status': 'false',
            'message': 'Invalid request',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                reset_token = PasswordResetToken.objects.get(
                    token=token,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )

                user = reset_token.user
                user.set_password(new_password)
                user.save()

                # Mark token as used
                reset_token.is_used = True
                reset_token.save()

                # Log activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='PASSWORD_RESET',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    description='User reset password'
                )

                resp = {
                    'status': 'true',
                    'message': 'Password reset successfully',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_200_OK)
            except PasswordResetToken.DoesNotExist:
                resp = {
                    'status': 'false',
                    'message': 'Invalid or expired reset token',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)

        resp = {
            'status': 'false',
            'message': 'Password reset failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data['token']

            try:
                verification = EmailVerification.objects.get(
                    token=token,
                    is_used=False,
                    expires_at__gt=timezone.now()
                )

                user = verification.user
                user.is_email_verified = True
                user.save()

                # Mark token as used
                verification.is_used = True
                verification.save()

                # Log activity
                UserActivity.objects.create(
                    user=user,
                    activity_type='EMAIL_VERIFICATION',
                    ip_address=request.META.get('REMOTE_ADDR'),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    description='User verified email'
                )

                resp = {
                    'status': 'true',
                    'message': 'Email verified successfully',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_200_OK)
            except EmailVerification.DoesNotExist:
                resp = {
                    'status': 'false',
                    'message': 'Invalid or expired verification token',
                    'payload': {}
                }
                return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)

        resp = {
            'status': 'false',
            'message': 'Email verification failed',
            'payload': serializer.errors
        }
        return Response(data=resp, status=status.HTTP_400_BAD_REQUEST)


class UserActivityListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        activities = UserActivity.objects.filter(user=request.user)[:20]  # Last 20 activities
        serializer = UserActivitySerializer(activities, many=True)

        resp = {
            'status': 'true',
            'message': 'Activities retrieved successfully',
            'payload': serializer.data
        }
        return Response(data=resp, status=status.HTTP_200_OK)
