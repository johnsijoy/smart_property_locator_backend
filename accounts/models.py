from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# -----------------------------
# Custom User Manager
# -----------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        """
        Create and save a regular User with email, optional username, and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)

        # Allow username to be optional for existing users
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        """
        Create and save a SuperUser with email, optional username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password=password, username=username, **extra_fields)

# -----------------------------
# Custom User Model
# -----------------------------
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, default='buyer')
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # keep empty to avoid breaking existing data

    def __str__(self):
        return self.email

# -----------------------------
# Contact Model
# -----------------------------
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
