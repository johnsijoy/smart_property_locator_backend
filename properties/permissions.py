from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Anyone can view (GET, HEAD, OPTIONS)
    - Only admin users can create or edit (POST, PUT, DELETE)
    """

    def has_permission(self, request, view):
        # Allow safe (read-only) methods for everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allow write methods only for admins
        return request.user and request.user.is_staff
