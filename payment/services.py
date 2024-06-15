from decimal import Decimal
from typing import Optional

import stripe
from django.conf import settings
from rest_framework.request import Request
from rest_framework.reverse import reverse
from stripe.api_resources.checkout import Session

from borrowing.models import Borrowing
from payment.models import Payment


def create_stripe_session_for_borrowing(
        borrowing: Borrowing,
        request: Request,
        total_price: Decimal,
        payment_type: str
) -> Optional[Session]:
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        success_url = request.build_absolute_uri(reverse('payment:payment-success'))
        cancel_url = request.build_absolute_uri(reverse('payment:payment-cancel'))

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': borrowing.book.title,
                    },
                    'unit_amount': int(total_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'{success_url}?session_id={{CHECKOUT_SESSION_ID}}',
            cancel_url=cancel_url,
        )

        Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            payment_type=payment_type,
            borrowing_id=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=total_price
        )

        return session

    except Exception as e:
        print(f"Error creating Stripe session: {e}")
        return None
