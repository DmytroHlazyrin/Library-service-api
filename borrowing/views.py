from decimal import Decimal

from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from borrowing.models import Borrowing, Book
from borrowing.permissions import IsAdminOrOwner
from borrowing.serializers import BorrowingSerializer
from payment.models import Payment
from payment.services import create_stripe_session_for_borrowing


def calculate_total_price(borrowing: Borrowing) -> Decimal:
    delta = borrowing.expected_return_date - borrowing.borrow_date
    days_borrowed = delta.days
    total_price = days_borrowed * borrowing.book.daily_fee
    return Decimal(total_price)


def calculate_fine(borrowing: Borrowing) -> Decimal:
    FINE_MULTIPLIER = 2
    days_overdue = (borrowing.actual_return_date - borrowing.expected_return_date).days
    daily_fee = borrowing.book.daily_fee
    fine_amount = days_overdue * daily_fee * FINE_MULTIPLIER
    return Decimal(fine_amount)


class BorrowingListCreateAPIView(generics.ListCreateAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
    permission_classes = (IsAuthenticated, IsAdminOrOwner)

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get("user_id")
        is_active = self.request.query_params.get("is_active")

        if user_id:
            queryset = queryset.filter(user=user_id)

        if is_active is not None:
            is_active = is_active.lower() in ("true", "1")
            if is_active:
                queryset = queryset.filter(actual_return_date__isnull=True)
            else:
                queryset = queryset.filter(actual_return_date__isnull=False)

        return queryset

    def create(self, request, *args, **kwargs) -> Response:
        book_id = request.data.get("book")
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {"error": "Book not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        book.inventory -= 1
        book.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        borrowing = serializer.save()

        total_price = calculate_total_price(borrowing)
        payment_type = Payment.PaymentType.PAYMENT
        session = create_stripe_session_for_borrowing(borrowing, request, total_price, payment_type)

        # потрібно прописати якусь логіку на те щоб коли payment не пройшов, то rollback borrowing
        if session:
            return redirect(session.url, code=303)
        else:
            # Rollback book inventory update if payment creation fails
            book.inventory += 1
            book.save()
            return Response(
                {"error": "Error creating payment session"},
                status=status.HTTP_400_BAD_REQUEST
            )


class BorrowingDetailAPIView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer
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
            {"error": "Borrowing not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if borrowing.actual_return_date is not None:
        return Response(
            {"error": "Borrowing already returned"},
            status=status.HTTP_400_BAD_REQUEST
        )

    session = None
    with transaction.atomic():
        borrowing.actual_return_date = timezone.now().date()
        borrowing.save()

        book = borrowing.book
        book.inventory += 1
        book.save()

        if borrowing.expected_return_date < borrowing.actual_return_date:
            fine_amount = calculate_fine(borrowing)
            payment_type = Payment.PaymentType.FINE
            session = create_stripe_session_for_borrowing(borrowing, request, fine_amount, payment_type)
            if session:
                return redirect(session.url, code=303)

    return Response(
        {"status": "Return date set and inventory updated"},
        status=status.HTTP_200_OK
    )
