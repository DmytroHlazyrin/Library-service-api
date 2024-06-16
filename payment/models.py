from datetime import timedelta

from django.db import models
from decimal import Decimal

from django.utils import timezone

from borrowing.models import Borrowing


class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid",
        EXPIRED = "EXPIRED", "Expired"

    class PaymentType(models.TextChoices):
        PAYMENT = "PAYMENT", "Payment"
        FINE = "FINE", "Fine"

    status = models.CharField(
        max_length=7, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    payment_type = models.CharField(max_length=7, choices=PaymentType.choices)
    borrowing_id = models.ForeignKey(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(max_length=500, blank=True, null=True)
    session_id = models.CharField(max_length=500, blank=True, null=True)
    money_to_pay = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    session_expiry = models.DateTimeField(default=timezone.now() + timedelta(hours=24))

    def __str__(self):
        return f"{self.payment_type} - {self.status} - {self.money_to_pay}"

    class Meta:
        ordering = ["-id"]
