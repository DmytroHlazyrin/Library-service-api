from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from book.models import Book
from borrowing.models import Borrowing
from payment.models import Payment

User = get_user_model()


class PaymentViewsTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="password"
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

        self.payment = Payment.objects.create(
            payment_type=Payment.PaymentType.PAYMENT,
            borrowing_id=self.borrowing,
            session_url="https://example.com/session",
            session_id="session123",
            money_to_pay=Decimal("10.00"),
        )

        self.user_token = RefreshToken.for_user(self.user).access_token
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token

    def test_payment_list_view_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get(reverse("payment:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_list_view_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(reverse("payment:payment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_detail_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")
        response = self.client.get(
            reverse("payment:payment-detail", args=[self.payment.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.payment.id)

    @patch("stripe.checkout.Session.retrieve")
    @patch("stripe.PaymentIntent.retrieve")
    def test_payment_success_view(
        self, mock_retrieve_payment_intent, mock_retrieve_session
    ):
        mock_retrieve_session.return_value = SimpleNamespace(payment_intent="pi_12345")
        mock_retrieve_payment_intent.return_value = SimpleNamespace(status="succeeded")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.user_token}")

        url = reverse("payment:payment-success")
        print(f"URL: {url}")
        print(f"Session ID: {self.payment.session_id}")

        response = self.client.get(url, {"session_id": self.payment.session_id})

        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Payment was successful")

        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, Payment.PaymentStatus.PAID)

    def test_payment_cancel_view(self):
        response = self.client.get(reverse("payment:payment-cancel"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Something went wrong!", response.data["detail"])

    def tearDown(self):
        self.client.credentials()
