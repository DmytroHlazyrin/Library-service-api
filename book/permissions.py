from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow all users to list and retrieve books,
    but only admins can add, edit, or delete books.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the request should be granted permission.

        Returns:
            True if the request is a safe method or the user is an admin,
            False otherwise.
        """
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
