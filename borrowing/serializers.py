from rest_framework import serializers

from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    user_email = serializers.CharField(source='user.email', read_only=True)

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
