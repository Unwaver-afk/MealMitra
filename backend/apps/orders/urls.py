from django.urls import path
from .views import (
    OrderCreateView,
    MyOrdersView,
    AllOrdersView,
    OrderDetailUpdateView
)

urlpatterns = [
    path('', OrderCreateView.as_view(), name='order-create'),
    path('my', MyOrdersView.as_view(), name='orders-my'),
    path('my/', MyOrdersView.as_view(), name='orders-my-slash'),
    path('all', AllOrdersView.as_view(), name='orders-all'),
    path('all/', AllOrdersView.as_view(), name='orders-all-slash'),
    path('<int:pk>', OrderDetailUpdateView.as_view(), name='order-detail-update'),
    path('<int:pk>/', OrderDetailUpdateView.as_view(), name='order-detail-update-slash'),
]

