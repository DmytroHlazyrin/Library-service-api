from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from borrowing.models import Borrowing, Book
from borrowing.serializers import BorrowingSerializer
from django.utils import timezone


class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if is_active:
            is_active = is_active.lower() in ("true", "1")
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def create(self, request, *args, **kwargs):
        book_id = request.data.get("book")
        book = Book.objects.get(id=book_id)
        if book.inventory < 1:
            return Response(
                {"error": "Book not available"},
                status=status.HTTP_400_BAD_REQUEST
            )

        book.inventory -= 1
        book.save()

        return super().create(request, *args, **kwargs)


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer


@api_view(["POST"])
def return_borrowing(request, pk):
    try:
        borrowing = Borrowing.objects.get(pk=pk)
    except Borrowing.DoesNotExist:
        return Response(
            {"error": "Borrowing not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if not borrowing.is_active:
        return Response(
            {"error": "Borrowing already returned"},
            status=status.HTTP_400_BAD_REQUEST
        )

    borrowing.actual_return_date = timezone.now().date()
    borrowing.is_active = False
    borrowing.save()

    book = borrowing.book
    book.inventory += 1
    book.save()

    return Response(
        {"status": "Return date set and inventory updated"},
        status=status.HTTP_200_OK
    )
