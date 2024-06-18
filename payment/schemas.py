from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from payment.serializers import (
    PaymentSerializer,
    PaymentListSerializer,
)
from rest_framework import status


payment_list_create_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve a list of payments. Staff can filter by borrowing ID and status.",
        parameters=[
            OpenApiParameter(
                name="borrowing_id",
                description="Filter by borrowing ID",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="status",
                description="Filter by payment status (PENDING, PAID, EXPIRED)",
                required=False,
                type=str
            ),
        ],
        responses={status.HTTP_200_OK: PaymentListSerializer(many=True)},
    ),
    post=extend_schema(
        description="Create a new payment record.",
        request=PaymentSerializer,
        responses={
            status.HTTP_201_CREATED: PaymentSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request"),
        },
    )
)

payment_detail_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve details of a specific payment.",
        responses={
            status.HTTP_200_OK: PaymentSerializer,
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Payment not found"),
        },
    )
)

payment_success_view_schema = extend_schema(
    description="Verify payment status and update the payment record.",
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Payment was successful"),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="Bad request or payment failed"),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Payment not found"),
    },
)

payment_cancel_view_schema = extend_schema(
    description="Inform the user that the payment was canceled and can be retried later.",
    responses={
        status.HTTP_200_OK: OpenApiResponse(description="Payment canceled"),
    },
)
