from django.test import TestCase, Client
from django.urls import reverse
from plans.models import TiffinPlan, Tag
from accounts.models import User


class LabDemoViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.tag = Tag.objects.create(name="LabDemoTag")
        self.plan = TiffinPlan.objects.create(
            title="Lab Test Plan",
            description="Created for testing Django templates",
            meal_type="Lunch",
            duration="Daily",
            price=120
        )
        self.plan.tags.add(self.tag)

    def test_lab_demo_home_view(self):
        response = self.client.get(reverse('lab-demo-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'lab_demo/home.html')
        self.assertContains(response, "Django Full Stack Lab Demonstration")

    def test_lab_demo_plans_view(self):
        response = self.client.get(reverse('lab-demo-plans'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lab_demo/plans_list.html')
        self.assertContains(response, "Lab Test Plan")
        self.assertContains(response, "LabDemoTag")

    def test_lab_demo_plan_create_modelform(self):
        post_data = {
            'title': 'New ModelForm Plan',
            'meal_type': 'Dinner',
            'duration': 'Weekly',
            'price': '850.00',
            'tags': [self.tag.id],
            'description': 'A delicious test dinner created using Django ModelForm.'
        }
        response = self.client.post(reverse('lab-demo-plan-create'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirects on success
        self.assertTrue(TiffinPlan.objects.filter(title="New ModelForm Plan").exists())

    def test_lab_demo_relationships_view(self):
        response = self.client.get(reverse('lab-demo-relationships'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lab_demo/relationships.html')
        self.assertContains(response, "1:1 One-to-One")
        self.assertContains(response, "N:M Many-to-Many")

    def test_lab_demo_search_view(self):
        response = self.client.get(reverse('lab-demo-search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lab_demo/search.html')
        self.assertContains(response, "Asynchronous Real-Time AJAX Search")
