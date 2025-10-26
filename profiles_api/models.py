# Import Django's base model system (used to define database fields)
from django.db import models

# Gives core authentication features like password hashing & login
from django.contrib.auth.models import AbstractBaseUser

# Adds built-in Django permissions (is_superuser, groups, permissions)
from django.contrib.auth.models import PermissionsMixin

# Base class required to create our own user manager
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager to handle creating users and superusers"""

    def create_user(self, email, name, password=None):
        """
        Create and return a normal user.
        - Requires email.
        - Normalizes email.
        - Hashes password before saving.
        """
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(
            email)  # Converts email to lowercase, standard form
        user = self.model(email=email,
                          name=name)  # Create user object but not yet saved

        user.set_password(password)  # Hashes the password securely
        user.save(using=self._db)  # Saves user to the database

        return user

    def create_superuser(self, email, name, password):
        """
        Create and return a superuser.
        - Uses create_user().
        - Adds admin permissions (is_superuser & is_staff).
        """
        user = self.create_user(email, name, password)

        user.is_superuser = True  # From PermissionsMixin (admin access)
        user.is_staff = True  # Can access Django admin panel
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email instead of username"""

    email = models.EmailField(max_length=255,
                              unique=True)  # Login email, must be unique
    name = models.CharField(max_length=255)  # User's full name
    is_active = models.BooleanField(
        default=True)  # If false → user cannot login
    is_staff = models.BooleanField(
        default=False)  # Allows access to admin site

    objects = UserProfileManager()  # Connects model with our custom manager

    USERNAME_FIELD = 'email'  # Use email to log in
    REQUIRED_FIELDS = [
        'name'
    ]  # Extra required fields when creating superuser using CLI

    def get_full_name(self):
        """Return user's full name"""
        return self.name

    def get_short_name(self):
        """Return short display name"""
        return self.name

    def __str__(self):
        """String shown in admin site & shell"""
        return self.email
