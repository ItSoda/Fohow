from rest_framework.test import APITestCase

from users.models import User
from users.serializers import UserSerializer


class UserSerializersTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="nikita@gmail.com", password="nik140406"
        )
        self.user2 = User.objects.create_user(
            email="nikitaaa@gmail.com", password="nik14040666"
        )

    def test_user_serializer(self):
        data = UserSerializer([self.user1, self.user2], many=True).data
        expected_data = [
            {
                "id": self.user1.id,
                "email": "nikita@gmail.com",
                "password": self.user1.password,
            },
            {
                "id": self.user2.id,
                "email": "nikitaaa@gmail.com",
                "password": self.user2.password,
            },
        ]
        self.assertEqual(expected_data, data)
