from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Custom permission to only allow administrators (matching Express isAdmin middleware).
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.role == 'admin' or request.user.is_staff or request.user.is_superuser)
        )
