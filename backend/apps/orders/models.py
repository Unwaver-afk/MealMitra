from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone


class Order(models.Model):
    """
    Represents customer meal subscriptions.
    Replaces MongoDB Order schema.
    Demonstrates Many-to-One relationships with User and TiffinPlan.
    """
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
    )
    ORDER_STATUS_CHOICES = (
        ('Placed', 'Placed'),
        ('Preparing', 'Preparing'),
        ('OutForDelivery', 'OutForDelivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    # Many-to-One relationships
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    plan = models.ForeignKey(
        'plans.TiffinPlan',
        on_delete=models.CASCADE,
        related_name='orders'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    order_status = models.CharField(
        max_length=30,
        choices=ORDER_STATUS_CHOICES,
        default='Placed'
    )

    # Simulated payment tracking
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True, default=None)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} ({self.plan.title} - {self.order_status})"

    def generate_deliveries(self):
        """
        Generates individual delivery schedules based on plan duration.
        1 delivery for Daily, 7 for Weekly, 30 for Monthly.
        """
        days_map = {
            'Daily': 1,
            'Weekly': 7,
            'Monthly': 30,
        }
        total_days = days_map.get(self.plan.duration, 1)
        base_date = timezone.now().date()

        deliveries_to_create = []
        for i in range(total_days):
            delivery_date = base_date + timedelta(days=i)
            deliveries_to_create.append(
                Delivery(
                    order=self,
                    date=delivery_date,
                    status=self.order_status
                )
            )
        Delivery.objects.bulk_create(deliveries_to_create)


class Delivery(models.Model):
    """
    Demonstrates One-to-Many relationship (one Order has many Deliveries).
    Replaces MongoDB embedded deliveries array.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='deliveries'
    )
    date = models.DateField()
    status = models.CharField(
        max_length=30,
        choices=Order.ORDER_STATUS_CHOICES,
        default='Placed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'
        ordering = ['date']

    def __str__(self):
        return f"Delivery for Order #{self.order_id} on {self.date} ({self.status})"
