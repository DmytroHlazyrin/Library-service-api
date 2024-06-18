from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from book.models import Book
from book.serializers import BookSerializer
from user.models import User


class BookListViewTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            first_name="admin",
            last_name="user",
            password="password",
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="user",
            last_name="user",
            password="password",
        )
        self.client.force_authenticate(user=self.admin_user)
        self.book1 = Book.objects.create(
            title="Test Book 1",
            author="Author A, B",
            cover="SOFT",
            inventory=5,
            daily_fee=1,
        )
        self.book2 = Book.objects.create(
            title="Test Book 2",
            author="Author C, D",
            cover="HARD",
            inventory=15,
            daily_fee=2,
        )
        self.list_url = reverse("book:book-list-create")

    def test_get_book_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_book_by_title(self):
        response = self.client.get(self.list_url, {"title": "Test Book 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_filter_book_by_author(self):
        response = self.client.get(self.list_url, {"author": "Author A, B"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_invalid_filter(self):
        response = self.client.get(self.list_url, {"cover": "HARD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_book_as_admin(self):
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 2,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New Book",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 2,
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2)


class BookDetailViewTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            first_name="admin",
            last_name="user",
            password="password",
        )
        self.user = User.objects.create_user(
            email="user@example.com",
            first_name="user",
            last_name="user",
            password="password",
        )
        self.client.force_authenticate(user=self.admin_user)
        self.book = Book.objects.create(
            title="Test Book 1",
            author="Author A, B",
            cover="SOFT",
            inventory=5,
            daily_fee=1,
        )
        self.detail_url = reverse("book:book-detail", kwargs={"pk": self.book.pk})

    def test_get_book_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book.title)
        self.assertEqual(response.data["author"], self.book.author)
        self.assertEqual(response.data["cover"], self.book.cover)
        self.assertEqual(response.data["inventory"], self.book.inventory)

    def test_update_book_as_admin(self):
        payload = {
            "title": "Updated Book 1",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 2,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book 1")

    def test_update_book_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New updated Book 1",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 2,
        }
        response = self.client.put(self.detail_url, payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.book.refresh_from_db()
        self.assertNotEqual(self.book.title, "New updated Book 1")

    def test_delete_book_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_delete_book_as_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(id=self.book.id).exists())


class BookSerializerTestCase(APITestCase):

    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "John Doe",
            "cover": "SOFT",
            "inventory": 10,
            "daily_fee": 2.50,
        }

    def test_valid_serializer(self):
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_negative_daily_fee(self):
        self.book_data["daily_fee"] = -2.50
        serializer = BookSerializer(data=self.book_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {"daily_fee"})
        self.assertEqual(
            serializer.errors["daily_fee"][0], "This field cannot be negative."
        )

    def test_invalid_author_characters(self):
        self.book_data["author"] = "John Doe 123"
        serializer = BookSerializer(data=self.book_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(set(serializer.errors.keys()), {"author"})
        self.assertEqual(
            serializer.errors["author"][0],
            "The author's name can only contain latin symbols and -.,'",
        )
