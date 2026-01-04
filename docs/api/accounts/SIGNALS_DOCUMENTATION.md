# Django Signals - Auto UserProfile Creation

## ✅ Problem Solved

Previously, when a User was created, UserProfile was NOT automatically created. 

**Now:** When a User is created, UserProfile is **automatically created** via Django signals! 🎉

---

## 📝 What Was Changed

### 1. Created `signals.py`
**File:** `/app/accounts/signals.py`

```python
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.accounts.models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile when a new User is created
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save UserProfile whenever User is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

### 2. Updated `apps.py`
**File:** `/app/accounts/apps.py`

Added `ready()` method to register signals:

```python
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app.accounts'

    def ready(self):
        import app.accounts.signals  # noqa
```

### 3. Updated `views.py`
**File:** `/app/accounts/api/views.py`

Removed manual UserProfile creation from RegisterAPIView:

```python
# BEFORE ❌
user = serializer.save()
UserProfile.objects.create(user=user)  # Manual creation

# AFTER ✅
user = serializer.save()
# UserProfile is automatically created by signals
```

---

## 🎯 How It Works

### Signal Flow:

```
1. User.objects.create() or user.save() is called
                ↓
2. post_save signal is triggered
                ↓
3. create_user_profile() receiver catches the signal
                ↓
4. If user is newly created (created=True):
                ↓
5. UserProfile.objects.create(user=instance) is called
                ↓
6. UserProfile is automatically created! ✅
```

---

## 🧪 Testing

### Test 1: User Registration via API
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

**Expected:** User AND UserProfile are both created automatically.

---

### Test 2: Create User Programmatically
```python
from app.accounts.models import User

# Create user
user = User.objects.create_user(
    email='new@example.com',
    username='newuser',
    password='pass123'
)

# Check if profile exists
print(user.profile)  # Should print: Profile of new@example.com
print(user.profile.id)  # Should print: UserProfile ID
```

**Expected:** UserProfile is automatically created.

---

### Test 3: Admin Panel
```python
# In Django admin or shell
from django.contrib.auth import get_user_model

User = get_user_model()

# Create user via admin
user = User.objects.create(
    email='admin@example.com',
    username='adminuser'
)
user.set_password('adminpass')
user.save()

# Check profile
user.profile  # Should exist automatically
```

**Expected:** UserProfile is automatically created.

---

### Test 4: Superuser Creation
```bash
python manage.py createsuperuser
```

**Expected:** When you create a superuser, UserProfile is automatically created.

---

## 🔍 Verification

### Check in Django Shell:
```bash
python manage.py shell
```

```python
from app.accounts.models import User, UserProfile

# Create test user
user = User.objects.create_user(
    email='verify@example.com',
    username='verifyuser',
    password='test123'
)

# Verify profile exists
print(f"User: {user}")
print(f"Profile exists: {hasattr(user, 'profile')}")
print(f"Profile: {user.profile}")
print(f"Profile ID: {user.profile.id}")

# Check database
print(f"Total Users: {User.objects.count()}")
print(f"Total Profiles: {UserProfile.objects.count()}")
# These should match! ✅
```

---

## 📊 Database Check

### Using Django Admin:
1. Go to http://localhost:8000/admin
2. Navigate to Users
3. Create a new user
4. Navigate to User Profiles
5. You should see a profile automatically created for that user ✅

### Using SQL:
```sql
-- Check users and profiles match
SELECT 
    COUNT(DISTINCT u.id) as user_count,
    COUNT(DISTINCT p.id) as profile_count
FROM accounts_user u
LEFT JOIN accounts_userprofile p ON p.user_id = u.id;
```

**Expected:** user_count = profile_count

---

## 🚨 Important Notes

### Signal Behavior:
1. **When triggered:** 
   - ✅ User.objects.create()
   - ✅ User.objects.create_user()
   - ✅ user.save() (first time)
   - ✅ Admin panel user creation
   - ✅ API registration

2. **What happens:**
   - `created=True` → Creates new UserProfile
   - `created=False` → Saves existing profile (if exists)

3. **Edge cases handled:**
   - If profile already exists, won't create duplicate
   - `hasattr(instance, 'profile')` check prevents errors
   - Signal only fires AFTER user is saved to database

---

## ✅ Benefits

1. **Automatic:** No need to manually create profiles
2. **Consistent:** Every user ALWAYS has a profile
3. **Clean Code:** No repetitive UserProfile.objects.create()
4. **Safe:** Handles edge cases automatically
5. **Django Best Practice:** Using signals is the recommended approach

---

## 🔧 Troubleshooting

### Issue: Profile not created
**Solution:** Make sure signals are imported in apps.py `ready()` method

### Issue: "User has no attribute 'profile'"
**Possible causes:**
1. Signals not registered (check apps.py)
2. User created before signals were set up
3. Need to run migrations

**Fix:**
```bash
# Re-run migrations
python manage.py migrate

# Recreate existing profiles
python manage.py shell
```

```python
from app.accounts.models import User, UserProfile

# Create profiles for users without one
for user in User.objects.all():
    if not hasattr(user, 'profile'):
        UserProfile.objects.create(user=user)
        print(f"Created profile for {user.email}")
```

---

## 📚 Related Files

- `app/accounts/signals.py` - Signal definitions
- `app/accounts/apps.py` - Signal registration
- `app/accounts/models.py` - User and UserProfile models
- `app/accounts/api/views.py` - API views (no longer manually creates profiles)

---

## 🎯 Summary

✅ **Before:** User created → Manual UserProfile.objects.create() needed
✅ **After:** User created → UserProfile automatically created via signals!

**No action needed from developers!** Just create the user, profile is handled automatically. 🎉

