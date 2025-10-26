# Import Django's base model class to create database models
from django.db import models

# AbstractBaseUser gives core authentication functionality (password, login)
from django.contrib.auth.models import AbstractBaseUser

# PermissionsMixin adds fields & methods for Django's permission system
from django.contrib.auth.models import PermissionsMixin

from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager user profile"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and savea new super user wiht give detail"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""

    # Email field for login instead of username
    email = models.EmailField(
        max_length=255, unique=True)  # Unique ensures no duplicate emails

    # Name field (full name of the user)
    name = models.CharField(max_length=255)

    # If the user account is active or not (used to disable users)
    is_active = models.BooleanField(default=True)

    # Determines if the user can access Django admin site
    is_staff = models.BooleanField(default=False)

    # Manager used to handle user creation (you should define UserProfileManager separately)
    objects = UserProfileManager()

    # This field will be used for authentication instead of default "username"
    USERNAME_FIELD = 'email'

    # Additional required fields when creating a superuser from the command line
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Returns the full name of the user"""
        return self.name

    def get_short_name(self):
        """Returns a short/display name of the user"""
        return self.name

    def __str__(self):
        """String representation of the user (shown in admin panel, shell, etc.)"""
        return self.email
