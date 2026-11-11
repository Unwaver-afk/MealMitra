from django.contrib import admin
from .models import Order, Delivery


class DeliveryInline(admin.TabularInline):
    model = Delivery
    extra = 0
    fields = ('date', 'status', 'created_at')
    readonly_fields = ('created_at',)
    can_delete = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'payment_status', 'order_status', 'created_at')
    list_filter = ('order_status', 'payment_status', 'created_at', 'plan__meal_type', 'plan__duration')
    search_fields = ('user__name', 'user__email', 'plan__title', 'razorpay_order_id', 'razorpay_payment_id')
    ordering = ('-created_at',)
    inlines = [DeliveryInline]
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('order__user__name', 'order__user__email')
    ordering = ('-date',)
