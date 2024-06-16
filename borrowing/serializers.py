from rest_framework import serializers

from book.serializers import BookSerializer
from borrowing.models import Borrowing
from payment.serializers import PaymentSerializer
from user.serializers import UserSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user_email",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "book", "expected_return_date")


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer()
    user = UserSerializer()
    payments = PaymentSerializer(many=True)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "payments"
        )
