# tasks.py
# from celery import shared_task
from django.utils import timezone
from .models import Payment

# @shared_task
def check_stripe_sessions():
    now = timezone.now()
    expired_payments = Payment.objects.filter(
        status=Payment.PaymentStatus.PENDING,
        session_expiry__lt=now
    )

    for payment in expired_payments:
        payment.status = Payment.PaymentStatus.EXPIRED
        payment.save()
