from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to authenticated users,
    and full access to admin users.

    Attributes:
        SAFE_METHODS (tuple): Tuple of HTTP methods considered safe.
    """

    def has_permission(self, request, view) -> bool:
        """
        Check if the requesting user has permission to access the view.

        Args:
            request (HttpRequest): The incoming request object.
            view (APIView): The view instance handling the request.

        Returns:
            bool: True if the user is authenticated for safe methods or is an admin, False otherwise.
        """
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
