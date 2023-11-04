from rest_framework.test import APITestCase
from .models import Order
from users.models import User
from django.urls import reverse
from rest_framework import status
from users.models import EmailVerification


# class OrderTests(APITestCase):
#     def setUp(self):
#         self.superuser = User.objects.create_superuser(
#             email="nik140406@gmail.com", password="nik140406"
#         )
#         self.user = User.objects.create_user(
#             email="nik1404067@gmail.com", password="nik1404067"
#         )
#         self.client.force_authenticate(user=self.superuser)
        
#         self.order = Order.objects.create(
#             first_name = "Nikita",
#             last_name = 'Shchegolskiy',
#             email = self.superuser.email,
#             address = "moscow",
#             initiator = self.user,
#         )

#         self.order1 = Order.objects.create(
#             first_name = "Nisdkita",
#             last_name = 'Shchesdgolskiy',
#             email = self.user.email,
#             address = "moscdsow",
#             initiator = self.user,
#         )

#     def test_order_list(self):
#         url = reverse("orders:orders-list")
#         response = self.client.get(url)
#         expected_data_length = 2
#         print(response.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len([response.data]), expected_data_length)
    
    # def test_order_create(self):
    #     url = reverse("orders:orders-list")
    #     data = {
    #         "first_name": "Nikitaa",
    #         "last_name": 'Shchegolskiiy',
    #         "email": self.user.email,
    #         "address": "moscow",
    #         "initiator": self.user.id,
    #     }
    #     response = self.client.post(url, data)
    #     expected_data_length = 3

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(len([response.data]), expected_data_length)
    #     # self.assertEqual(EmailVerification.objects.count(), expected_data_length)
        