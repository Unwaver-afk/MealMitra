from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User representation matching Express response format."""
    _id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', '_id', 'name', 'email', 'role', 'created_at']
        read_only_fields = ['id', '_id', 'role', 'created_at']

    def get__id(self, obj):
        return str(obj.id)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)
    name = serializers.CharField(min_length=2, max_length=80)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

    def validate_email(self, value):
        normalized_email = value.lower().strip()
        if User.objects.filter(email=normalized_email).exists():
            raise serializers.ValidationError("An account with this email already exists.")
        return normalized_email

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name'].strip(),
            role='user'
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom SimpleJWT serializer that returns user details along with tokens."""
    username_field = 'email'

    def validate(self, attrs):
        # Allow case-insensitive email matching
        if 'email' in attrs:
            attrs['email'] = attrs['email'].lower().strip()
        elif 'username' in attrs:
            attrs['username'] = attrs['username'].lower().strip()

        data = super().validate(attrs)
        data['token'] = data['access']  # Express frontend uses 'token'
        data['user'] = {
            'id': self.user.id,
            '_id': str(self.user.id),
            'name': self.user.name,
            'email': self.user.email,
            'role': self.user.role,
        }
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=128)

