from datetime import timedelta
from decimal import Decimal

from celery import shared_task
from django.db.models import Sum, Count
from django.utils import timezone
from payment.models import Payment
from botSend import send_message


@shared_task
def check_stripe_sessions():
    """
    Update the status of expired Stripe payment sessions.
    """
    now = timezone.now()
    Payment.objects.filter(
        status=Payment.PaymentStatus.PENDING,
        session_expiry__lt=now
    ).update(status=Payment.PaymentStatus.EXPIRED)


@shared_task
def daily_payment_report():
    """
       Retrieve payments created today, calculate the total amount and count,
       and return a formatted string.
       """
    today = timezone.now().date()

    aggregate_data = Payment.objects.filter(
        status=Payment.PaymentStatus.PAID,
        created_at__date=today
    ).aggregate(
        total=Sum('money_to_pay'),
        count=Count('id')
    )

    total_amount = aggregate_data.get('total', '0.00')
    total_count = aggregate_data.get('count', 0)
    message = (
        f"Payments per day: {Decimal(total_count, )}\n"
        f"Amount: {total_amount}"
    )
    send_message(message)


@shared_task
def monthly_payment_report():
    """
    Retrieve payments created in the previous month,
    calculate the total amount and count,
    send a message to the Telegram bot.
    """
    # Get the first day of the previous month
    today = timezone.now()
    previous_month = today.replace(day=1) - timedelta(days=1)
    previous_month_start = previous_month.replace(day=1)

    # Get the last day of the previous month
    if previous_month.month == 12:
        previous_month_end = previous_month.replace(day=31)
    else:
        previous_month_end = (
                previous_month.replace(
                    month=previous_month.month + 1, day=1
                ) - timedelta(days=1)
        )

    # Retrieve payments created in the previous month
    payments_previous_month = Payment.objects.filter(
        status=Payment.PaymentStatus.PAID,
        created_at__gte=previous_month_start,
        created_at__lte=previous_month_end,
    )

    # Calculate the total amount and count of payments
    total_payments = payments_previous_month.count()
    total_amount = sum(
        payment.money_to_pay for payment in payments_previous_month
    )

    # Send a message to the Telegram bot
    message = (
        f"Monthly amount for "
        f"{previous_month.strftime('%B %Y')}: {total_amount}\n"
        f"Payments per month: {total_payments}"
    )
    send_message(message)
