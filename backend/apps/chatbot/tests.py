from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from plans.models import TiffinPlan


class ChatbotAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        TiffinPlan.objects.create(
            title="South Indian Breakfast",
            description="2 idlis with sambar and chutney",
            meal_type="Breakfast",
            duration="Daily",
            price=90
        )

    def test_chatbot_recommendation(self):
        response = self.client.post('/api/chatbot/', {"message": "Tell me about breakfast"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("text", response.data)
        self.assertIn("Breakfast", response.data["text"])
