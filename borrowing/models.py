from django.db import models

from book.models import Book
from library_service import settings
from .tasks import my_task, another_task

User = settings.AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="borrowing"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="borrowing"
    )

    def save(self, *args, **kwargs):
        my_task.delay()
        super().save(*args, **kwargs)
        another_task.delay()

    def __str__(self):
        return f"{self.user} borrowed {self.book} ({self.borrow_date})"
