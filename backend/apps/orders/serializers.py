from rest_framework import serializers
from .models import Order, Delivery
from plans.models import TiffinPlan
from plans.serializers import TiffinPlanSerializer
from accounts.serializers import UserSerializer


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['id', 'date', 'status']


class OrderSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    userId = UserSerializer(source='user', read_only=True)
    planId = TiffinPlanSerializer(source='plan', read_only=True)
    paymentStatus = serializers.CharField(source='payment_status')
    orderStatus = serializers.CharField(source='order_status')
    deliveries = DeliverySerializer(many=True, read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            '_id',
            'userId',
            'planId',
            'payment_status',
            'paymentStatus',
            'order_status',
            'orderStatus',
            'razorpay_order_id',
            'razorpay_payment_id',
            'deliveries',
            'createdAt',
            'updatedAt',
        ]

    def get__id(self, obj):
        return str(obj.id)


class OrderCreateSerializer(serializers.Serializer):
    planId = serializers.CharField(required=False)
    plan_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        raw_id = attrs.get('planId') or attrs.get('plan_id')
        if not raw_id:
            raise serializers.ValidationError("planId is required")
        try:
            plan = TiffinPlan.objects.get(pk=int(raw_id), is_active=True)
        except (ValueError, TiffinPlan.DoesNotExist):
            raise serializers.ValidationError("Selected meal plan does not exist or is inactive.")
        attrs['plan'] = plan
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        plan = validated_data['plan']

        order = Order.objects.create(
            user=user,
            plan=plan,
            payment_status='Pending',
            order_status='Placed'
        )
        order.generate_deliveries()
        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    orderStatus = serializers.CharField(required=False)
    order_status = serializers.CharField(required=False)

    def validate(self, attrs):
        status_value = attrs.get('orderStatus') or attrs.get('order_status')
        valid_statuses = [c[0] for c in Order.ORDER_STATUS_CHOICES]
        if status_value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status '{status_value}'. Valid choices are: {', '.join(valid_statuses)}")
        attrs['clean_status'] = status_value
        return attrs
