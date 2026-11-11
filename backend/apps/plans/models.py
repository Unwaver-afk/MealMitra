from django.db import models
from django.utils.text import slugify


class Tag(models.Model):
    """
    Demonstrates Many-to-Many relationship with TiffinPlan.
    Used for categorizing and filtering plans (e.g., Healthy, North Indian, Popular).
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    description = models.CharField(max_length=200, blank=True, default='')

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class TiffinPlan(models.Model):
    """
    Represents meal subscription plans.
    Replaces MongoDB TiffinPlan schema.
    """
    MEAL_CHOICES = (
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    )
    DURATION_CHOICES = (
        ('Daily', 'Daily'),
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Many-to-Many relationship
    tags = models.ManyToManyField(Tag, related_name='plans', blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tiffin Plan'
        verbose_name_plural = 'Tiffin Plans'
        ordering = ['meal_type', 'price']

    def __str__(self):
        return f"{self.title} ({self.meal_type} · {self.duration}) - ₹{self.price}"
