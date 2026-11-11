from django.urls import path
from .views import lab_demo_home

urlpatterns = [
    path('', lab_demo_home, name='lab-demo-home'),
]
