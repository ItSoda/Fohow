from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import Order
from users.models import User


class OrderTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.user = User.objects.create_user(
            email="nik1404067@gmail.com", password="nik1404067"
        )
        self.access_token = str(RefreshToken.for_user(self.superuser).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Создаем новые заказы
        url = reverse("orders:orders-list")
        data1 = {
            "first_name": "Nikitasdfa",
            "last_name": "Shchegolskiiy",
            "email": self.superuser.email,
            "address": "moscow",
            "initiator": self.superuser.email,
        }
        data2 = {
            "first_name": "Nikitasdfsdfa",
            "last_name": "Shchegolskiiy",
            "email": self.superuser.email,
            "address": "moscow",
            "initiator": self.superuser.email,
        }

        self.order1 = self.client.post(url, data1).data
        self.order2 = self.client.post(url, data2).data

    def test_order_create(self):
        url = reverse("orders:orders-list")
        data = {
            "first_name": "Nikitaa",
            "last_name": "Shchegolskiiy",
            "email": self.user.email,
            "address": "moscow",
            "initiator": self.user.email,
        }
        response = self.client.post(url, data)
        expected_data_length = 1

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len([response.data]), expected_data_length)

    def test_order_list(self):
        url = reverse("orders:orders-list")
        response = self.client.get(url)
        expected_data_length = 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)

    def test_order_detail(self):
        url = f"{settings.DOMAIN_NAME}/api/orders/{self.order1['id']}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), 1)
        self.assertEqual("nik140406@gmail.com", response.data["email"])

    def test_order_partial_update(self):
        url = f"{settings.DOMAIN_NAME}/api/orders/{self.order1['id']}/"
        data = {"address": "Moscow Pushkin 17"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), 1)
        self.assertEqual("Moscow Pushkin 17", response.data["address"])

    def test_order_destroy(self):
        url = f"{settings.DOMAIN_NAME}/api/orders/{self.order1['id']}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.filter(initiator=self.superuser).count(), 1)
