from django.db import models
from rest_framework.exceptions import ValidationError


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

    class Meta:
        ordering = ["-id"]
