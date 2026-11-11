from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from plans.models import TiffinPlan
from orders.models import Order

User = get_user_model()


class ReportsAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="reportadmin@test.com",
            password="adminpassword123",
            name="Report Admin"
        )
        self.user = User.objects.create_user(
            email="reportuser@test.com",
            password="userpassword123",
            name="Report User"
        )
        self.plan = TiffinPlan.objects.create(
            title="Classic Lunch",
            description="Daily lunch",
            meal_type="Lunch",
            duration="Daily",
            price=120
        )
        self.order = Order.objects.create(
            user=self.user,
            plan=self.plan,
            payment_status="Paid",
            order_status="Placed"
        )
        self.client.force_authenticate(user=self.admin)

    def test_export_orders_csv(self):
        response = self.client.get('/api/reports/orders/csv/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn("Classic Lunch", response.content.decode('utf-8'))

    def test_export_orders_pdf(self):
        response = self.client.get('/api/reports/orders/pdf/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(response.content.startswith(b'%PDF'))
