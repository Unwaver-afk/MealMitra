from django.urls import path
from .views import (
    lab_demo_home,
    lab_demo_plans,
    lab_demo_plan_create,
    lab_demo_relationships,
    lab_demo_search
)

urlpatterns = [
    path('', lab_demo_home, name='lab-demo-home'),
    path('plans/', lab_demo_plans, name='lab-demo-plans'),
    path('plans/create/', lab_demo_plan_create, name='lab-demo-plan-create'),
    path('relationships/', lab_demo_relationships, name='lab-demo-relationships'),
    path('search/', lab_demo_search, name='lab-demo-search'),
]
