from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import TiffinPlan, Tag

User = get_user_model()


class PlanAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_superuser(
            email="admin@test.com",
            password="adminpassword123",
            name="Admin"
        )
        self.user = User.objects.create_user(
            email="user@test.com",
            password="userpassword123",
            name="Normal User"
        )
        self.tag = Tag.objects.create(name="Healthy")
        self.plan = TiffinPlan.objects.create(
            title="Healthy Poha",
            description="Fresh poha with peas and sprouts",
            meal_type="Breakfast",
            duration="Daily",
            price=75
        )
        self.plan.tags.add(self.tag)

    def test_get_plans_public(self):
        response = self.client.get('/api/plans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Healthy Poha")
        self.assertEqual(response.data[0]["mealType"], "Breakfast")
        self.assertEqual(response.data[0]["_id"], str(self.plan.id))

    def test_create_plan_admin_only(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "title": "Paneer Thali",
            "description": "Rich paneer thali with dal and roti",
            "mealType": "Lunch",
            "duration": "Weekly",
            "price": 899
        }
        # Non-admin should be forbidden
        response = self.client.post('/api/plans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin should succeed
        self.client.force_authenticate(user=self.admin)
        response = self.client.post('/api/plans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TiffinPlan.objects.count(), 2)

    def test_ajax_search(self):
        response = self.client.get('/api/plans/search?q=poha')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Healthy Poha")
