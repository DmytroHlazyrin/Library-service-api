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
        parameters=[
            OpenApiParameter(
                name="email",
                description="User's email address",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="password",
                description="User's password",
                required=True,
                type=str,
            ),
            OpenApiParameter(
                name="first_name",
                description="User's first name",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="last_name",
                description="User's last name",
                required=False,
                type=str,
            ),
        ],
        responses={201: UserSerializer},
    )
)


manage_user_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve information about the current user.",
        responses={200: UserSerializer},
        parameters=[
            OpenApiParameter(
                name="Authorization",
                description="Bearer token for authentication",
                required=True,
                type=str,
                location=OpenApiParameter.HEADER,
            )
        ],
    ),
    put=extend_schema(
        description="Update information about the current user.",
        request=UserSerializer,
        responses={200: UserSerializer},
        parameters=[
            OpenApiParameter(
                name="Authorization",
                description="Bearer token for authentication",
                required=True,
                type=str,
                location=OpenApiParameter.HEADER,
            )
        ],
    ),
    patch=extend_schema(
        description="Partially update information about the current user.",
        request=UserSerializer,
        responses={200: UserSerializer},
        parameters=[
            OpenApiParameter(
                name="Authorization",
                description="Bearer token for authentication",
                required=True,
                type=str,
                location=OpenApiParameter.HEADER,
            )
        ],
    )
)
