from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import EmailVerification, User
from users.serializers import UserSerializer


class UserTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.access_token = str(RefreshToken.for_user(self.superuser).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.user = User.objects.create_user(
            email="kokokola@gmail.com", password="nik140406"
        )

    def test_create_account(self):
        url = f"{settings.DOMAIN_NAME}/auth/users/"
        data = {"email": "lolchik@gmail.com", "password": "testpaswword"}
        response = self.client.post(url, data)
        user_sr_data = UserSerializer(data).data
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.count(), 3
        )  # 3 пользователей, так как суперпользователь и тестовый уже созданы
        self.assertEqual(EmailVerification.objects.count(), 3)
        self.assertEqual(user_sr_data["email"], response.data["email"])

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

    def test_user_list(self):
        url = reverse("users:users-list")
        response = self.client.get(url)
        expected_data_length = 2

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)
