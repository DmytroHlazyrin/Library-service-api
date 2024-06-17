from rest_framework import generics, mixins
from rest_framework.response import Response

from book.schema import book_list_view_schema, book_detail_view_schema
from book.models import Book
from book.permissions import IsAdminOrReadOnly

from book.serializers import BookSerializer


@book_list_view_schema
class BookListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    """View for listing and creating books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request.

        Returns a list of all books
        with optional filtering by title and author.
        """
        title = request.query_params.get("title")
        author = request.query_params.get("author")

        queryset = self.get_queryset()

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(
            page if page is not None else queryset, many=True
        )
        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST request.

        Creates a new book with provided data.
        """
        return self.create(request, *args, **kwargs)


@book_detail_view_schema
class BookDetailView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """View for retrieving, updating, and deleting a book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request.

        Returns the details of a single book.
        """
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs) -> Response:
        """
        Handle PUT request.

        Updates a book with provided data.
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs) -> Response:
        """
        Handle PATCH request.

        Partially updates a book with provided data.
        """
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs) -> Response:
        """
        Handle DELETE request.

        Deletes a book.
        """
        return self.destroy(request, *args, **kwargs)
