from django.test import TestCase
from decimal import Decimal
from borrowing.models import Book, Borrowing
from payment.payment_calculator import calculate_total_price, calculate_fine
from django.contrib.auth import get_user_model
from datetime import date, timedelta

User = get_user_model()


class PaymentCalculatorTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=Decimal("1.00"),
        )

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=date.today() + timedelta(days=7),
        )

    def test_calculate_total_price(self):
        total_price = calculate_total_price(self.borrowing)
        expected_price = Decimal("7.00")
        self.assertEqual(total_price, expected_price)

    def test_calculate_fine(self):
        self.borrowing.actual_return_date = (
            self.borrowing.expected_return_date + timedelta(days=3)
        )
        fine = calculate_fine(self.borrowing)
        expected_fine = Decimal("6.00")
        self.assertEqual(fine, expected_fine)
