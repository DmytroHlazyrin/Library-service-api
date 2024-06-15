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

    def has_active_borrowing(self) -> bool:
        """
        Checks if there are active borrowings (book is currently borrowed).

        Returns:
            bool: True if there are active borrowings, False otherwise.
        """
        return self.borrowing_set.filter(actual_return_date__isnull=True).exists()

    def clean(self) -> None:
        """
        Performs model validation.

        Raises:
            ValidationError: If there are active borrowings, prevents saving the book.
        """
        if self.has_active_borrowing():
            raise ValidationError(
                "Cannot delete the book because it is currently borrowed by someone."
            )

        super().clean()

    def delete(self, using=None, keep_parents=False) -> None:
        """
        Deletes the book if there are no active borrowings.

        Args:
            using (str, optional): The database alias to use. Defaults to None.
            keep_parents (bool, optional): If True, keep the parent link. Defaults to False.

        Raises:
            ValidationError: If there are active borrowings, prevents deletion of the book.
        """
        if self.has_active_borrowing():
            raise ValidationError(
                "Cannot delete the book because it is currently borrowed by someone."
            )

        super().delete(using=using, keep_parents=keep_parents)
