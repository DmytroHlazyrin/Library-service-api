from rest_framework import generics
from rest_framework.response import Response

from book.schemas import book_list_view_schema, book_detail_view_schema
from book.models import Book
from book.permissions import IsAdminOrReadOnly

from book.serializers import BookSerializer


@book_list_view_schema
class BookListView(generics.ListCreateAPIView):
    """View for listing and creating books."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        """
        Optionally restricts the returned books to a given title or author,
        by filtering against query parameters in the URL.
        """
        queryset = super().get_queryset()
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if author:
            queryset = queryset.filter(author__icontains=author)

        return queryset


@book_detail_view_schema
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating, and deleting a book."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)
