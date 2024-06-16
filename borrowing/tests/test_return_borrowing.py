from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from borrowing.models import Borrowing
from borrowing.tests.test_base import BaseBorrowingTest


class ReturnBorrowingTests(BaseBorrowingTest):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.borrowing = Borrowing.objects.create(
            user=self.user, book=self.book,
            borrow_date=timezone.now().date(),
            expected_return_date=(timezone.now() + timedelta(days=8)).date()
        )

    def test_return_borrowing(self):
        url = reverse(
            "return-borrowing",
            kwargs={"pk": self.borrowing.pk}
        )
        response = self.client.post(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_return_already_returned_borrowing(self):
        self.borrowing.actual_return_date = timezone.now().date()
        self.borrowing.save()

        url = reverse('return-borrowing', kwargs={'pk': self.borrowing.pk})
        response = self.client.post(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
