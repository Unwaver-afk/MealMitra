from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)

User = get_user_model()


class RegisterView(APIView):
    """
    POST /api/auth/register
    Creates a new customer user account.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login
    Authenticates user and returns JWT access/refresh tokens plus user data.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    """
    GET /api/auth/profile
    Returns the authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """
    POST /api/auth/forgot-password
    Simulates sending a password reset email for security (avoids user enumeration).
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'].lower().strip()
            user = User.objects.filter(email=email).first()
            if user:
                token = get_random_string(length=64)
                user.password_reset_token = token
                user.password_reset_expires = timezone.now() + timedelta(minutes=15)
                user.password_reset_requested_at = timezone.now()
                user.save(update_fields=['password_reset_token', 'password_reset_expires', 'password_reset_requested_at'])
            return Response({
                "message": "If that email is registered, a password reset link has been sent."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    POST /api/auth/reset-password/<token>
    Resets the password with a valid reset token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(
            password_reset_token=token,
            password_reset_expires__gt=timezone.now()
        ).first()

        if not user:
            return Response({
                "message": "Password reset token is invalid or has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['password'])
        user.password_reset_token = None
        user.password_reset_expires = None
        user.increment_auth_version()
        user.save()

        return Response({
            "message": "Password reset successful"
        }, status=status.HTTP_200_OK)
