from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer
)
from accounts.permissions import IsAdminRole


class OrderCreateView(APIView):
    """
    POST /api/orders
    Creates a new meal subscription order for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response({
                "message": "Order created successfully",
                "order": OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyOrdersView(APIView):
    """
    GET /api/orders/my
    Returns orders belonging to the authenticated customer, populated with plan details.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).select_related('plan', 'user').prefetch_related('deliveries').order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllOrdersView(APIView):
    """
    GET /api/orders/all
    Returns all orders for administration, populated with user and plan details.
    """
    permission_classes = [IsAdminRole]

    def get(self, request):
        orders = Order.objects.all().select_related('plan', 'user').prefetch_related('deliveries').order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailUpdateView(APIView):
    """
    PUT /api/orders/<id>
    Updates the status of an order (Admin only).
    """
    permission_classes = [IsAdminRole]

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['clean_status']
            order.order_status = new_status
            order.save(update_fields=['order_status', 'updated_at'])

            # If order is Delivered or Cancelled, update unfinished deliveries
            if new_status in ['Delivered', 'Cancelled']:
                order.deliveries.all().update(status=new_status)

            return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
