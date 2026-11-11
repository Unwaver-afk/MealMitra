from rest_framework import serializers
from .models import TiffinPlan, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'description']


class TiffinPlanSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    meal_type = serializers.CharField(required=False)
    mealType = serializers.CharField(source='meal_type', required=False)
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        source='tags',
        write_only=True,
        required=False
    )
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)

    class Meta:
        model = TiffinPlan
        fields = [
            'id',
            '_id',
            'title',
            'description',
            'meal_type',
            'mealType',
            'duration',
            'price',
            'tags',
            'tag_ids',
            'is_active',
            'createdAt',
            'updatedAt'
        ]

    def get__id(self, obj):
        return str(obj.id)

    def validate(self, attrs):
        # Support mealType or meal_type
        if 'meal_type' not in attrs:
            val = self.initial_data.get('mealType') or self.initial_data.get('meal_type')
            if not val:
                raise serializers.ValidationError({"mealType": "This field is required."})
            attrs['meal_type'] = val
        return attrs
