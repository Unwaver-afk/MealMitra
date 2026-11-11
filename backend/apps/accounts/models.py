from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    """Custom user manager where email is the unique identifier for auth."""

    def create_user(self, email, password=None, name='', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name='Admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, name=name, **extra_fields)


class User(AbstractUser):
    """
    Custom user model representing MealMitra customers and administrators.
    Replaces MongoDB User schema.
    """
    username = None  # Remove username field, use email instead
    email = models.EmailField('Email Address', unique=True, max_length=254)
    name = models.CharField('Full Name', max_length=80)

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    auth_version = models.PositiveIntegerField(default=0)

    # Password reset fields (matching Express implementation)
    password_reset_token = models.CharField(max_length=128, blank=True, null=True)
    password_reset_expires = models.DateTimeField(blank=True, null=True)
    password_reset_requested_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser or self.is_staff

    def increment_auth_version(self):
        self.auth_version += 1
        self.save(update_fields=['auth_version', 'updated_at'])


class UserProfile(models.Model):
    """
    Demonstrates a One-to-One relationship with User.
    Stores customer preferences, delivery address, and contact info.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=100, blank=True, default='')
    pincode = models.CharField(max_length=10, blank=True, default='')
    dietary_preference = models.CharField(
        max_length=50,
        choices=[('Vegetarian', 'Vegetarian'), ('Non-Vegetarian', 'Non-Vegetarian'), ('Vegan', 'Vegan'), ('All', 'All')],
        default='Vegetarian'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.email}"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """Automatically create or update the profile when a user is saved."""
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
