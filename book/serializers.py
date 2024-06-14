import re

from rest_framework import serializers

from book.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")

    def validate_daily_fee(self, value):
        if value < 0:
            raise serializers.ValidationError("This field cannot be negative.")
        return value

    def validate_author(self, value):
        if not re.match(r"^[a-zA-Z\s\-.,']+$", value):
            raise serializers.ValidationError("Name of author can contain only latin symbols and -., '")
        return value
