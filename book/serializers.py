import re

from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    """Serializer for the Book model."""

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "cover",
            "inventory",
            "daily_fee",
            "image"
        )

    def validate_daily_fee(self, value: float) -> float:
        """Validate that the daily fee is not negative."""
        if value < 0:
            raise serializers.ValidationError(
                "This field cannot be negative."
            )
        return value

    def validate_author(self, value: str) -> str:
        """Validate the author's name to contain only allowed characters."""
        if not re.match(r"^[a-zA-Z\s\-.,']+$", value):
            raise serializers.ValidationError(
                "The author's name can only contain latin symbols and -.,'"
            )
        return value
