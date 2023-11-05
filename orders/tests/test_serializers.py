from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from orders.models import Order
from orders.serializers import OrderSerializer
from users.models import User


class OrderSerializers(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.access_token = str(RefreshToken.for_user(self.superuser).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Создаем новые заказы
        url = reverse("orders:orders-list")
        self.order1 = Order.objects.create(
            first_name="Nikitasdfa",
            last_name="Shchegolskiiy",
            email=self.superuser.email,
            address="moscow",
            initiator=self.superuser,
        )

        self.order_sr_data = OrderSerializer(self.order1).data

    def test_order_serializer(self):
        expected_data = {
            "id": self.order1.id,
            "first_name": "Nikitasdfa",
            "last_name": "Shchegolskiiy",
            "email": self.superuser.email,
            "address": "moscow",
            "initiator": self.superuser.email,
            "status": "Создан",
            "created": self.order_sr_data["created"],
            "basket_history": dict(),
        }

        self.assertEqual(self.order_sr_data, expected_data)
