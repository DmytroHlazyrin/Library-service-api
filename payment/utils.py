import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session_for_borrowing(borrowing):
    # Assuming each borrowing has a single payment amount to be paid
    payment = borrowing.payments.first()  # Assuming there's at least one payment

    if not payment:
        raise ValueError("No payment found for this borrowing")

    amount_to_pay = payment.money_to_pay

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': borrowing.book.title,
                    },
                    'unit_amount': int(amount_to_pay * 100),  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://your-domain.com/success',  # Change to your actual success URL
            cancel_url='https://your-domain.com/cancel',    # Change to your actual cancel URL
        )
        return session
    except Exception as e:
        print(f"Error creating Stripe session: {e}")
        return None
