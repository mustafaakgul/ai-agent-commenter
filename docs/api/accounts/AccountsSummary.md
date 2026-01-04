# Accounts App - API Documentation

## Overview
Complete authentication and user management system with REST API endpoints.

## Features

### ✅ Implemented Features
1. **User Registration & Authentication**
   - User registration with email verification
   - Login with JWT tokens
   - Logout with token blacklisting
   - Token refresh mechanism

2. **User Profile Management**
   - View and update user profile
   - Extended profile with additional fields
   - Avatar upload support
   - Social media links

3. **Password Management**
   - Change password (authenticated users)
   - Password reset request (forgot password)
   - Password reset confirmation with tokens

4. **Email Verification**
   - Email verification with tokens
   - Token expiration (24 hours)

5. **User Activity Tracking**
   - Login/logout tracking
   - Profile updates
   - Password changes
   - IP address and user agent logging

## Models

### User (Custom User Model)
- Extends Django's AbstractUser
- Email as primary login field
- Email and phone verification flags
- Additional fields: phone_number, date_of_birth

### UserProfile
- One-to-one relationship with User
- Bio, avatar, company, job title
- Location, website
- Social media links (Twitter, LinkedIn, GitHub)
- Preferences (language, timezone, notifications)

### EmailVerification
- Token-based email verification
- Expiration time (24 hours)
- Used flag

### PasswordResetToken
- Token-based password reset
- Expiration time (2 hours)
- Used flag

### UserActivity
- Activity type tracking
- IP address and user agent
- Timestamp and description

## API Endpoints

### Authentication Endpoints

#### 1. Register
```http
POST /api/v1/accounts/register
```

**Request:**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890"
}
```

**Response (201):**
```json
{
  "status": "true",
  "message": "User registered successfully. Please verify your email.",
  "payload": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "is_email_verified": false
    },
    "verification_token": "token_here"
  }
}
```

#### 2. Login
```http
POST /api/v1/accounts/login
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "status": "true",
  "message": "Login successful",
  "payload": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "johndoe"
    },
    "tokens": {
      "refresh": "refresh_token_here",
      "access": "access_token_here"
    }
  }
}
```

#### 3. Logout
```http
POST /api/v1/accounts/logout
Headers: Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "refresh_token": "refresh_token_here"
}
```

#### 4. Token Refresh
```http
POST /api/v1/accounts/token/refresh
```

**Request:**
```json
{
  "refresh": "refresh_token_here"
}
```

### Profile Endpoints

#### 5. Get Profile
```http
GET /api/v1/accounts/profile
Headers: Authorization: Bearer <access_token>
```

#### 6. Update Profile
```http
PUT /api/v1/accounts/profile
Headers: Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe Updated",
  "phone_number": "+1234567890",
  "date_of_birth": "1990-01-01"
}
```

#### 7. Get Profile Details
```http
GET /api/v1/accounts/profile/detail
Headers: Authorization: Bearer <access_token>
```

#### 8. Update Profile Details
```http
PUT /api/v1/accounts/profile/detail
Headers: Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "bio": "Software developer passionate about AI",
  "company": "Tech Company",
  "job_title": "Senior Developer",
  "location": "San Francisco, CA",
  "website": "https://example.com",
  "twitter": "https://twitter.com/johndoe",
  "linkedin": "https://linkedin.com/in/johndoe",
  "github": "https://github.com/johndoe",
  "language": "en",
  "timezone": "America/Los_Angeles",
  "receive_notifications": true,
  "receive_newsletter": false
}
```

### Password Management

#### 9. Change Password
```http
POST /api/v1/accounts/password/change
Headers: Authorization: Bearer <access_token>
```

**Request:**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewSecurePass456!",
  "new_password_confirm": "NewSecurePass456!"
}
```

#### 10. Password Reset Request
```http
POST /api/v1/accounts/password/reset/request
```

**Request:**
```json
{
  "email": "user@example.com"
}
```

#### 11. Password Reset Confirm
```http
POST /api/v1/accounts/password/reset/confirm
```

**Request:**
```json
{
  "token": "reset_token_here",
  "new_password": "NewSecurePass789!",
  "new_password_confirm": "NewSecurePass789!"
}
```

### Email Verification

#### 12. Verify Email
```http
POST /api/v1/accounts/email/verify
```

**Request:**
```json
{
  "token": "verification_token_here"
}
```

### Activity Tracking

#### 13. Get User Activities
```http
GET /api/v1/accounts/activity
Headers: Authorization: Bearer <access_token>
```

**Response:**
```json
{
  "status": "true",
  "message": "Activities retrieved successfully",
  "payload": [
    {
      "id": 1,
      "user_email": "user@example.com",
      "activity_type": "LOGIN",
      "ip_address": "192.168.1.1",
      "user_agent": "Mozilla/5.0...",
      "description": "User logged in successfully",
      "created": "2026-01-04T10:30:00Z"
    }
  ]
}
```

## Activity Types
- `REGISTRATION` - User registered
- `LOGIN` - User logged in
- `LOGOUT` - User logged out
- `PROFILE_UPDATE` - User updated profile
- `PASSWORD_CHANGE` - User changed password
- `PASSWORD_RESET_REQUEST` - User requested password reset
- `PASSWORD_RESET` - User reset password
- `EMAIL_VERIFICATION` - User verified email

## Serializers (10 Serializers)
- ✅ UserRegistrationSerializer
- ✅ UserLoginSerializer
- ✅ UserSerializer
- ✅ UserUpdateSerializer
- ✅ UserProfileSerializer
- ✅ ChangePasswordSerializer
- ✅ PasswordResetRequestSerializer
- ✅ PasswordResetConfirmSerializer
- ✅ EmailVerificationSerializer
- ✅ UserActivitySerializer

## Admin Panel
- ✅ Custom User Admin
- ✅ User Profile Admin
- ✅ Email Verification Admin
- ✅ Password Reset Token Admin
- ✅ User Activity Admin (read-only)

## Security Features
- ✅ JWT Authentication
- ✅ Token Blacklisting (logout)
- ✅ Token Rotation
- ✅ Password Validation
- ✅ Secure Token Generation
- ✅ Activity Logging (IP + User Agent)

## Installation & Setup

### 1. Create migrations
```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### 2. Create superuser
```bash
python manage.py createsuperuser
```

### 3. Run server
```bash
python manage.py runserver
```

## Usage Examples

### Python (requests)
```python
import requests

BASE_URL = 'http://localhost:8000/api/v1/accounts'

# Register
response = requests.post(f'{BASE_URL}/register', json={
    'email': 'user@example.com',
    'username': 'johndoe',
    'password': 'SecurePass123!',
    'password_confirm': 'SecurePass123!',
    'first_name': 'John',
    'last_name': 'Doe'
})

# Login
response = requests.post(f'{BASE_URL}/login', json={
    'email': 'user@example.com',
    'password': 'SecurePass123!'
})
tokens = response.json()['payload']['tokens']

# Get Profile
headers = {'Authorization': f'Bearer {tokens["access"]}'}
response = requests.get(f'{BASE_URL}/profile', headers=headers)
profile = response.json()
```

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/v1/accounts/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/accounts/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

### 3. View Profile
```bash
curl -X GET http://localhost:8000/api/v1/accounts/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### JavaScript (Fetch)
```javascript
const BASE_URL = 'http://localhost:8000/api/v1/accounts';

// Register
const register = async (userData) => {
  const response = await fetch(`${BASE_URL}/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  return response.json();
};

// Login
const login = async (email, password) => {
  const response = await fetch(`${BASE_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.payload.tokens.access);
  localStorage.setItem('refresh_token', data.payload.tokens.refresh);
  return data;
};

// Get Profile
const getProfile = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${BASE_URL}/profile`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return response.json();
};
```

## Security Features

1. **Password Validation**
   - Minimum length requirement
   - Common password check
   - Numeric password prevention
   - User attribute similarity check

2. **Token Security**
   - JWT tokens with expiration
   - Token blacklisting on logout
   - Token rotation on refresh
   - Secure token generation (secrets module)

3. **Activity Tracking**
   - IP address logging
   - User agent tracking
   - Activity timestamp
   - Audit trail

## TODO / Future Enhancements

- [ ] Email sending integration (SMTP/SendGrid)
- [ ] Phone number verification (SMS/OTP)
- [ ] Two-factor authentication (2FA)
- [ ] Social authentication (Google, Facebook, GitHub)
- [ ] Rate limiting for sensitive endpoints
- [ ] Account deletion/deactivation
- [ ] Session management
- [ ] API key management
- [ ] Team/Organization support
- [ ] Role-based permissions

## Testing

```bash
# Run all tests
python manage.py test app.accounts

# Run specific test
python manage.py test app.accounts.tests.TestUserRegistration
```

## Notes

- Email verification tokens expire after 24 hours
- Password reset tokens expire after 2 hours
- JWT access tokens expire after 1 hour
- JWT refresh tokens expire after 7 days
- User activities are limited to last 20 records per request

## 📊 Project Structure

```
app/accounts/
├── __init__.py
├── admin.py              # Admin panel configuration
├── apps.py
├── models.py             # 5 models (User, Profile, etc.)
├── tests.py
├── views.py
├── README.md             # Detailed documentation
├── api/
│   ├── __init__.py
│   ├── serializers.py    # 10 serializers
│   ├── urls.py           # 13 endpoints
│   └── views.py          # 10 API views
└── migrations/
    └── __init__.py
```



---

## 💡 Recommendations

### 1. **Add Email Service**
Create a service for email sending:
```python
# app/accounts/services/email_service.py
class EmailService:
    @staticmethod
    def send_verification_email(user, token):
        # Send email via SendGrid or SMTP
        pass
```

### 2. **Add Permissions**
Create custom permission classes:
```python
# app/accounts/api/permissions.py
class IsEmailVerified(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_email_verified
```

### 3. **Add Throttling**
Create throttle classes for rate limiting:
```python
# app/accounts/api/throttles.py
class RegisterThrottle(AnonRateThrottle):
    rate = '5/hour'
```

### 4. **Write Tests**
Comprehensive test coverage:
```python
# app/accounts/tests.py
class TestUserRegistration(TestCase):
    def test_register_success(self):
        # Test implementation
        pass
```

### 5. **Add Signals**
Automatic operations with model signals:
```python
# app/accounts/signals.py
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
```
