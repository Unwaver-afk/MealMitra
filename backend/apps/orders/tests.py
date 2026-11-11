from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from plans.models import TiffinPlan
from .models import Order

User = get_user_model()


class OrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="orderuser@test.com",
            password="orderpassword123",
            name="Order User"
        )
        self.admin = User.objects.create_superuser(
            email="orderadmin@test.com",
            password="adminpassword123",
            name="Order Admin"
        )
        self.plan = TiffinPlan.objects.create(
            title="Weekly Lunch Thali",
            description="7 days of healthy homestyle lunches",
            meal_type="Lunch",
            duration="Weekly",
            price=749
        )

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/orders/', {"planId": self.plan.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order", response.data)
        self.assertEqual(response.data["order"]["paymentStatus"], "Pending")
        self.assertEqual(response.data["order"]["orderStatus"], "Placed")
        self.assertEqual(len(response.data["order"]["deliveries"]), 7)

    def test_my_orders(self):
        self.client.force_authenticate(user=self.user)
        # Create an order
        self.client.post('/api/orders/', {"planId": self.plan.id}, format='json')

        response = self.client.get('/api/orders/my')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["planId"]["title"], "Weekly Lunch Thali")

    def test_admin_update_order_status(self):
        # Create order as user
        order = Order.objects.create(
            user=self.user,
            plan=self.plan,
            payment_status="Paid",
            order_status="Placed"
        )
        order.generate_deliveries()

        # Update as admin
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(
            f'/api/orders/{order.id}/',
            {"orderStatus": "OutForDelivery"},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.order_status, "OutForDelivery")
