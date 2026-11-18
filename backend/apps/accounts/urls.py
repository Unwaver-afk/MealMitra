from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    ProfileView,
    ForgotPasswordView,
    ResetPasswordView
)

urlpatterns = [
    path('register', RegisterView.as_view(), name='auth-register'),
    path('register/', RegisterView.as_view(), name='auth-register-slash'),
    path('login', LoginView.as_view(), name='auth-login'),
    path('login/', LoginView.as_view(), name='auth-login-slash'),
    path('profile', ProfileView.as_view(), name='auth-profile'),
    path('profile/', ProfileView.as_view(), name='auth-profile-slash'),
    path('forgot-password', ForgotPasswordView.as_view(), name='auth-forgot-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='auth-forgot-password-slash'),
    path('reset-password/<str:token>', ResetPasswordView.as_view(), name='auth-reset-password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='auth-reset-password-slash'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]

