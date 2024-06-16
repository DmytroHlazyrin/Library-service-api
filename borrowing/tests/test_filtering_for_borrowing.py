from django.urls import reverse
from rest_framework import status

from borrowing.models import Borrowing
from borrowing.tests.test_base import BaseBorrowingTest


class BorrowingFilteringTests(BaseBorrowingTest):
    def setUp(self):
        super().setUp()
        self.borrowing1 = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date="2024-06-10",
            expected_return_date="2024-06-20",
            actual_return_date="2024-06-20",
        )
        self.borrowing2 = Borrowing.objects.create(
            user=self.admin,
            book=self.book,
            borrow_date="2024-06-11",
            expected_return_date="2024-06-21",
            actual_return_date=None

        )
        self.borrowing3 = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            borrow_date="2024-06-22",
            expected_return_date="2024-06-23",
            actual_return_date=None
        )

    def test_user_can_only_see_their_own_borrowing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("borrowing-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], self.borrowing1.id)

    def test_user_can_filter_their_own_active_borrowings(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("borrowing-list-create") + "?is_active=true"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing3.id)

    def test_user_can_filter_their_own_inactive_borrowings(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("borrowing-list-create") + "?is_active=false"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.borrowing1.id)

    def test_admin_can_filter_all_active_borrowings(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("borrowing-list-create") + "?is_active=true"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_admin_can_filter_all_inactive_borrowings(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("borrowing-list-create") + "?is_active=false"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_admin_can_filter_by_user_id(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(
            reverse("borrowing-list-create") + f"?user_id={self.user.id}"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["user_email"], self.user.email)

    def test_user_cannot_filter_by_user_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("borrowing-list-create") + f"?user_id={self.admin.id}"
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data[0]["user_email"], self.admin.email)
