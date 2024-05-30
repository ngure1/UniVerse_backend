from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access to everyone
        if request.method in SAFE_METHODS:
            return True

        # Only allow write access to admin users
        return request.user.is_superuser
