from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient

from book.models import Book


User = get_user_model()


class BaseBorrowingTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@user.com",
            password="123test1233",
            is_staff=False
        )
        self.admin = User.objects.create_superuser(
            email="admin@admin.com",
            password="123admin123"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="John Doe",
            cover="SOFT",
            inventory=3,
            daily_fee=3.55
        )
        self.client = APIClient()
