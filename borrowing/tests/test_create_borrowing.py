from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from borrowing.tests.test_base import BaseBorrowingTest


class CreateBorrowingTests(BaseBorrowingTest):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(self.user)
        self.url = reverse("borrowing-list-create")

    def test_create_borrowing(self):
        data = {
            "book": self.book.id,
            "borrow_date": timezone.now().date(),
            "expected_return_date": (timezone.now() + timedelta(days=7)).date()
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertIn("Location", response)

    def test_create_borrowing_book_not_available(self):
        self.book.inventory = 0
        self.book.save()

        url = reverse("borrowing-list-create")
        data = {
            "book": self.book.id,
            "borrow_date": timezone.now().date(),
            "expected_return_date": (timezone.now() + timedelta(days=7)).date()
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
