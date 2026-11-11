from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class AuthAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register'
        self.login_url = '/api/auth/login'
        self.profile_url = '/api/auth/profile'

    def test_user_registration(self):
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], "testuser@example.com")
        self.assertTrue(User.objects.filter(email="testuser@example.com").exists())

    def test_user_login(self):
        User.objects.create_user(
            email="loginuser@example.com",
            password="securePassword123",
            name="Login User"
        )
        data = {
            "email": "loginuser@example.com",
            "password": "securePassword123"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["user"]["email"], "loginuser@example.com")

    def test_profile_authenticated(self):
        user = User.objects.create_user(
            email="profile@example.com",
            password="securePassword123",
            name="Profile User"
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "profile@example.com")

    def test_profile_unauthenticated(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
