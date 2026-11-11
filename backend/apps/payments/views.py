from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from orders.models import Order


class CreateOrderView(APIView):
    """
    POST /api/payment/create-order
    Simulated Razorpay order creation for College Lab Demonstration.
    No actual transactions or external Razorpay API calls are made.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('orderId')
        if not order_id:
            return Response({"message": "orderId is required"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        if order.user != request.user and not request.user.is_admin_user:
            return Response({"message": "Not authorized to access this order"}, status=status.HTTP_403_FORBIDDEN)

        amount_in_paise = int(order.plan.price * 100)
        simulated_order_id = f"order_simulated_{order.id}_{int(timezone.now().timestamp())}"
        order.razorpay_order_id = simulated_order_id
        order.save(update_fields=['razorpay_order_id', 'updated_at'])

        return Response({
            "key": "rzp_test_mock_mealmitra_lab",
            "amount": amount_in_paise,
            "currency": "INR",
            "razorpayOrderId": simulated_order_id,
            "isSimulated": True,
            "demoNotice": "Demonstration mode: No real payment processed."
        }, status=status.HTTP_200_OK)


class VerifyPaymentView(APIView):
    """
    POST /api/payment/verify
    Simulated Razorpay payment verification.
    Marks the order as 'Paid' and records simulated transaction IDs.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('orderId')
        if not order_id:
            return Response({"message": "orderId is required"}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, pk=order_id)
        if order.user != request.user and not request.user.is_admin_user:
            return Response({"message": "Not authorized to access this order"}, status=status.HTTP_403_FORBIDDEN)

        payment_id = request.data.get('razorpay_payment_id') or f"pay_simulated_{order.id}_{int(timezone.now().timestamp())}"
        order.payment_status = 'Paid'
        order.razorpay_payment_id = payment_id
        order.save(update_fields=['payment_status', 'razorpay_payment_id', 'updated_at'])

        return Response({
            "success": True,
            "message": "Payment verified successfully (Simulated Demonstration)",
            "paymentId": payment_id
        }, status=status.HTTP_200_OK)
