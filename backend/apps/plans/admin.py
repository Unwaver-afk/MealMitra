from django.contrib import admin
from .models import TiffinPlan, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TiffinPlan)
class TiffinPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'meal_type', 'duration', 'price', 'is_active', 'created_at')
    list_filter = ('meal_type', 'duration', 'is_active', 'tags')
    search_fields = ('title', 'description')
    ordering = ('meal_type', 'price')
    filter_horizontal = ('tags',)
