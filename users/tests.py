from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.user = User.objects.create_user(
            email="kokokola@gmail.com", password="nik140406"
        )

    def test_create_account(self):
        url = f"{settings.DOMAIN_NAME}/auth/users/"
        data = {"email": "lolchik@gmail.com", "password": "testpaswword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.count(), 3
        )  # 3 пользователей, так как суперпользователь и тестовый уже созданы

    def test_login_account(self):
        url = reverse("token_obtain_pair")
        data = {"email": self.user.email, "password": "nik140406"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout_account(self):
        url = reverse("token_blacklist")
        self.refresh_token = str(RefreshToken.for_user(self.user))
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        data = {"refresh": self.refresh_token}
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        invalid_response = self.client.post(reverse("token_blacklist"), data)
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
