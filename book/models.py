from django.db import models


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
