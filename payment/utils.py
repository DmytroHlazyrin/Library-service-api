import stripe
from django.conf import settings
from decimal import Decimal
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_session_for_borrowing(borrowing):
    # Calculate the total price for the borrowing
    # This example assumes you have a way to calculate the total price, here it's set as a fixed value for demonstration
    total_price = Decimal("10.00")  # Replace this with your actual price calculation logic

    try:
        # Create Stripe session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': borrowing.book.title,
                    },
                    'unit_amount': int(total_price * 100),  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://your-domain.com/success',  # Change to your actual success URL
            cancel_url='https://your-domain.com/cancel',    # Change to your actual cancel URL
        )

        # Create and save a Payment instance
        payment = Payment.objects.create(
            status=Payment.PaymentStatus.PENDING,
            payment_type=Payment.PaymentType.PAYMENT,
            borrowing_id=borrowing,
            session_url=session.url,
            session_id=session.id,
            money_to_pay=total_price
        )
        return payment
    except Exception as e:
        print(f"Error creating Stripe session: {e}")
        return None
