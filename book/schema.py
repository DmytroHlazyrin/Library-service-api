from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    extend_schema_view
)

from book.serializers import BookSerializer


book_list_view_schema = extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                "title",
                OpenApiTypes.STR,
                description="Filter by title of the book."
            ),
            OpenApiParameter(
                "author",
                OpenApiTypes.STR,
                description="Filter by author of the book."
            ),
        ],
        description="Retrieve a list of books with optional "
                    "filtering by title and author."
    ),
    post=extend_schema(
        request=BookSerializer,
        responses={201: BookSerializer},
        parameters=[
            OpenApiParameter(
                "title",
                OpenApiTypes.STR,
                description="Title of the book.",
                required=True,
            ),
            OpenApiParameter(
                "author",
                OpenApiTypes.STR,
                description="Author of the book.",
                required=True,
            ),
            OpenApiParameter(
                "cover",
                OpenApiTypes.STR,
                description="Cover type of the book.",
                required=True,
            ),
            OpenApiParameter(
                "inventory",
                OpenApiTypes.INT,
                description="Inventory count of the book.",
                required=True,
            ),
            OpenApiParameter(
                "daily_fee",
                OpenApiTypes.NUMBER,
                description="Daily fee for renting the book.",
                required=True,
            ),
        ],
        description="Create a new book."
    ),
)
book_detail_view_schema = extend_schema_view(
    get=extend_schema(
        description="Retrieve a specific book by ID.",
        responses={200: BookSerializer},
    ),
    put=extend_schema(
        request=BookSerializer,
        responses={200: BookSerializer},
        description="Update an existing book by ID."
    ),
    patch=extend_schema(
        request=BookSerializer,
        responses={200: BookSerializer},
        description="Partially update an existing book by ID."
    ),
    delete=extend_schema(
        description="Delete a specific book by ID.",
        responses={204: None},
    ),
)
