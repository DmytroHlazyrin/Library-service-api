from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

from book.models import Book
from borrowing.models import Borrowing
from payment.models import Payment
from payment.services import create_stripe_session_for_borrowing

User = get_user_model()


class CreateStripeSessionForBorrowingTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.Covers.HARD,
            inventory=10,
            daily_fee=Decimal("1.00"),
        )

        self.borrowing = Borrowing.objects.create(
            user=self.user, book=self.book, expected_return_date="2024-01-10"
        )

        self.factory = APIRequestFactory()
        self.request = self.factory.get(reverse("borrowing-list-create"))
        self.request.user = self.user

        settings.STRIPE_SECRET_KEY = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

    @patch("stripe.checkout.Session.create")
    def test_create_stripe_session_for_borrowing_success(
        self, mock_stripe_session_create
    ):
        mock_stripe_session_create.return_value = MagicMock(
            id="session_123", url="https://checkout.stripe.com/pay/session_123"
        )

        total_price = Decimal("10.00")
        payment_type = Payment.PaymentType.PAYMENT
        session = create_stripe_session_for_borrowing(
            self.borrowing, self.request, total_price, payment_type
        )

        self.assertIsNotNone(session)
        self.assertEqual(session.id, "session_123")
        self.assertEqual(session.url, "https://checkout.stripe.com/pay/session_123")

        payment = Payment.objects.get(borrowing_id=self.borrowing)
        self.assertEqual(payment.status, Payment.PaymentStatus.PENDING)
        self.assertEqual(payment.payment_type, payment_type)
        self.assertEqual(payment.session_id, "session_123")
        self.assertEqual(
            payment.session_url, "https://checkout.stripe.com/pay/session_123"
        )
        self.assertEqual(payment.money_to_pay, total_price)

    @patch("stripe.checkout.Session.create")
    def test_create_stripe_session_for_borrowing_failure(
        self, mock_stripe_session_create
    ):
        mock_stripe_session_create.side_effect = Exception(
            "Stripe session creation failed"
        )

        total_price = Decimal("10.00")
        payment_type = Payment.PaymentType.PAYMENT
        session = create_stripe_session_for_borrowing(
            self.borrowing, self.request, total_price, payment_type
        )

        self.assertIsNone(session)

        payments = Payment.objects.filter(borrowing_id=self.borrowing)
        self.assertEqual(payments.count(), 0)
