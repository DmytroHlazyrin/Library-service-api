import pathlib
import uuid

from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


def book_image_path(instance: "Book", filename: str) -> pathlib.Path:
    """
    Generates a unique file path for a book image upload.
    """
    filename = (f"{slugify(instance.title)}-{uuid.uuid4()}.jpg"
                + pathlib.Path(filename).suffix)
    return pathlib.Path("uploads/books") / pathlib.Path(filename)


class Book(models.Model):
    """Book model."""

    class Covers(models.TextChoices):
        """Book cover options."""

        HARD = "HARD"
        SOFT = "SOFT"

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=255, choices=Covers.choices)
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to=book_image_path, null=True)

    def __str__(self) -> str:
        """Returns the title of the book."""
        return self.title

    def can_be_deleted(self) -> bool:
        """
        Checks if the book can be deleted.

        Returns True if no active borrowings exist.
        """
        return not self.borrowing.filter(
            actual_return_date__isnull=True
        ).exists()

    def delete(self, using=None, keep_parents=False) -> None:
        """
        Deletes the book if no active borrowings exist;
        otherwise, raises a ValidationError.
        """
        if not self.can_be_deleted():
            raise ValidationError(
                "Cannot delete the book "
                "because it is currently borrowed by someone."
            )

        super().delete(using=using, keep_parents=keep_parents)
