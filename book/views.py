from rest_framework import generics, mixins
from rest_framework.response import Response

from book.models import Book
from book.serializers import BookSerializer


class BookListView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    """View for listing and creating books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs) -> Response:
        """
        Handle GET request.

        Returns a list of all books.
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle POST request.

        Creates a new book with provided data.
        """
        return self.create(request, *args, **kwargs)


class BookDetailView(
    generics.GenericAPIView,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin
):
    """View for retrieving, updating, and deleting a book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

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
