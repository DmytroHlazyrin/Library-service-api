from django.db import models
from decimal import Decimal


class Payment(models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'

    class PaymentType(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment'
        FINE = 'FINE', 'Fine'

    status = models.CharField(
        max_length=7,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    payment_type = models.CharField(
        max_length=7,
        choices=PaymentType.choices
    )
    borrowing_id = models.IntegerField()  # Borrowing model's ID
    session_url = models.URLField()
    session_id = models.CharField(max_length=255)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f'{self.payment_type} - {self.status} - {self.money_to_pay}'

    class Meta:
        ordering = ['-id']
