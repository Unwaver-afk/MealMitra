from django.urls import path
from .views import (
    PlanListCreateView,
    PlanDetailUpdateDeleteView,
    PlanAjaxSearchView
)

urlpatterns = [
    path('', PlanListCreateView.as_view(), name='plan-list-create'),
    path('search', PlanAjaxSearchView.as_view(), name='plan-ajax-search'),
    path('search/', PlanAjaxSearchView.as_view(), name='plan-ajax-search-slash'),
    path('<int:pk>', PlanDetailUpdateDeleteView.as_view(), name='plan-detail-update-delete'),
    path('<int:pk>/', PlanDetailUpdateDeleteView.as_view(), name='plan-detail-update-delete-slash'),
]
