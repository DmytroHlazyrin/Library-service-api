from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from borrowing.models import Borrowing
from borrowing.tests.test_base import BaseBorrowingTest


class BorrowingDetailTests(BaseBorrowingTest):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date=timezone.now().date(),
            expected_return_date=(timezone.now() + timedelta(days=7)).date()
        )

    def test_get_borrowing_detail(self):
        url = reverse(
            "borrowing-detail",
            kwargs={"pk": self.borrowing.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_borrowing_detail(self):
        url = reverse(
            "borrowing-detail",
            kwargs={"pk": 9999}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
