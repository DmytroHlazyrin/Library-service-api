from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
)

from user.serializers import UserSerializer


create_user_view_schema = extend_schema_view(
    post=extend_schema(
        description="Create a new user.",
        request=UserSerializer,
        responses={201: UserSerializer},
    )
)

manage_user_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve information about the current user.",
        responses={200: UserSerializer},
    ),
    put=extend_schema(
        description="Update information about the current user.",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    patch=extend_schema(
        description="Partially update information about the current user.",
        request=UserSerializer,
        responses={200: UserSerializer},
    )
)
