from django.db import transaction, IntegrityError
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from borrowing.models import Borrowing, Book
from borrowing.permissions import IsAdminOrOwner
from borrowing.serializers import (
    BorrowingSerializer,
    BorrowingCreateSerializer,
    BorrowingDetailSerializer,
)
from payment.models import Payment
from payment.payment_calculator import calculate_total_price, calculate_fine
from payment.services import create_stripe_session_for_borrowing


class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.select_related("user", "book")
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            queryset = super().get_queryset()
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user=user_id)
        else:
            queryset = super().get_queryset().filter(user=user)

        is_active = self.request.query_params.get("is_active")

        if is_active is not None:
            is_active = is_active.lower() in ("true", "1")
            if is_active:
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BorrowingCreateSerializer
        return self.serializer_class

    def create(self, request: Request, *args, **kwargs) -> Response:
        if Payment.objects.filter(
            Q(status=Payment.PaymentStatus.PENDING)
            | Q(status=Payment.PaymentStatus.EXPIRED),
            borrowing_id__user=request.user,
        ).exists():
            raise ValidationError(
                "User has pending payments and cannot borrow new books."
            )

        book_id = request.data.get("book")
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if book.inventory < 1:
            return Response(
                {"error": "Book is not available"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            with transaction.atomic():
                book.inventory -= 1
                book.save()

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                borrowing = serializer.save(user=request.user)

                total_price = calculate_total_price(borrowing)
                payment_type = Payment.PaymentType.PAYMENT

                session = create_stripe_session_for_borrowing(
                    borrowing, request, total_price, payment_type
                )

                if not session:
                    raise IntegrityError("Error creating payment session")

                return redirect(session.url, code=303)

        except IntegrityError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("user", "book")
    serializer_class = BorrowingDetailSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)


@api_view(["POST", "GET"])
def return_borrowing(request: Request, pk: int) -> Response:
    """
    Handle the return of a borrowed book.
    """
    try:
        borrowing = Borrowing.objects.get(pk=pk)
    except Borrowing.DoesNotExist:
        return Response(
            {"error": "Borrowing not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if borrowing.actual_return_date is not None:
        return Response(
            {"error": "Borrowing already returned"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            borrowing.actual_return_date = timezone.now().date()
            borrowing.save()

            book = borrowing.book
            book.inventory += 1
            book.save()

            if borrowing.expected_return_date < borrowing.actual_return_date:
                fine_amount = calculate_fine(borrowing)
                payment_type = Payment.PaymentType.FINE
                session = create_stripe_session_for_borrowing(
                    borrowing, request, fine_amount, payment_type
                )
                if session:
                    return redirect(session.url, code=303)
                raise IntegrityError("Error creating payment session for fine")
        return Response(
            {"status": "Return date set and inventory updated"},
            status=status.HTTP_200_OK,
        )
    except IntegrityError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
