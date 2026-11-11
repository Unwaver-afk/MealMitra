from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from plans.models import TiffinPlan
from orders.models import Order

User = get_user_model()


class PaymentAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="payuser@test.com",
            password="paypassword123",
            name="Payment User"
        )
        self.plan = TiffinPlan.objects.create(
            title="Dinner Plan",
            description="Homestyle delicious dinner",
            meal_type="Dinner",
            duration="Weekly",
            price=699
        )
        self.order = Order.objects.create(
            user=self.user,
            plan=self.plan,
            payment_status="Pending"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_payment_order(self):
        response = self.client.post('/api/payment/create-order/', {"orderId": self.order.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("razorpayOrderId", response.data)
        self.assertEqual(response.data["amount"], 69900)
        self.assertTrue(response.data["isSimulated"])

    def test_verify_payment(self):
        response = self.client.post('/api/payment/verify/', {
            "orderId": self.order.id,
            "razorpay_order_id": "order_simulated_test",
            "razorpay_payment_id": "pay_simulated_test",
            "razorpay_signature": "mock_signature"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.order.refresh_from_db()
        self.assertEqual(self.order.payment_status, "Paid")
