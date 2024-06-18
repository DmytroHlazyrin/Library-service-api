from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
)
from rest_framework import status


borrowing_list_create_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve a list of borrowings. Staff can filter by user ID and active status.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                description="Filter by user ID (staff only)",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="is_active",
                description="Filter by active borrowings (true/false)",
                required=False,
                type=str
            ),
        ],
        responses={status.HTTP_200_OK: BorrowingSerializer(many=True)},
    ),
    post=extend_schema(
        description="Create a new borrowing record. User must not have any pending or expired payments.",
        request=BorrowingCreateSerializer,
        responses={
            status.HTTP_201_CREATED: BorrowingCreateSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Book not found or not available"),
        },
    )
)

borrowing_detail_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve details of a specific borrowing.",
        responses={
            status.HTTP_200_OK: BorrowingDetailSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Borrowing not found"),
        },
    )
)

return_borrowing_schema = extend_schema(
    description="Return a borrowed book. If the actual return date is after the expected return date, a fine will be calculated.",
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Return date set and inventory updated"),
        status.HTTP_303_SEE_OTHER: OpenApiResponse(description="Redirect to Stripe session for fine payment"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request or borrowing already returned"),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Borrowing not found"),
    },
)
