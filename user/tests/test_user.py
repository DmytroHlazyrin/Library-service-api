from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


User = get_user_model()


class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "First",
            "last_name": "Last",
        }
        response = self.client.post(reverse("user:create"), payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)
        self.assertEqual(response.data["first_name"], payload["first_name"])
        self.assertEqual(response.data["last_name"], payload["last_name"])

    def test_create_user_with_existing_email(self):
        """Test creating a user with an existing email fails"""
        payload = {
            "email": "test@example.com",
            "password": "testpass123",
            "first_name": "First",
            "last_name": "Last",
        }
        User.objects.create_user(**payload)

        response = self.client.post(reverse("user:create"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_short_password(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            "email": "test@example.com",
            "password": "pw",
            "first_name": "First",
            "last_name": "Last",
        }
        response = self.client.post(reverse("user:create"), payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        response = self.client.get(reverse("user:manage"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="First",
            last_name="Last",
        )
        self.client.force_authenticate(user=user)

        response = self.client.get(reverse("user:manage"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
            },
        )

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="First",
            last_name="Last",
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(reverse("user:manage"), {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123",
            first_name="First",
            last_name="Last",
        )
        self.client.force_authenticate(user=user)
        payload = {
            "password": "newpassword123",
            "first_name": "NewFirst",
            "last_name": "NewLast",
        }

        response = self.client.patch(reverse("user:manage"), payload)

        user.refresh_from_db()
        self.assertTrue(user.check_password(payload["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], user.email)
        self.assertEqual(response.data["first_name"], payload["first_name"])
        self.assertEqual(response.data["last_name"], payload["last_name"])
        self.assertNotIn("password", response.data)
