from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Basket, Category, Image, Product
from products.serializers import (BasketSerializer, CategorySerializer,
                                  ImageSerializer, ProductCreateSerializer,
                                  ProductSerializer)
from users.models import User


class ProductSerializerTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.user = User.objects.create_user(
            email="nik1404006@gmail.com", password="nik1404006"
        )

        self.access_token = str(RefreshToken.for_user(self.superuser).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.cat = Category.objects.create(name="cat1")
        self.img = Image.objects.create(
            img="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg"
        )

        self.product = Product.objects.create(
            name="product",
            description="product1_desc",
            price=10000.00,
            product_composition="product1_pr_cm",
            packaging_standard="product1_packaging",
            expiration_date="product1_ex",
            method_of_application="product1_moa",
        )
        # if field is MtM
        self.product.categories.add(self.cat)
        self.product.images.add(self.img)

        self.product1 = Product.objects.create(
            name="product1",
            description="product1_desc",
            price=5000.00,
            product_composition="product1_pr_cm",
            packaging_standard="product1_packaging",
            expiration_date="product1_ex",
            method_of_application="product1_moa",
        )
        # if field is MtM
        self.product.categories.add(self.cat)
        self.product.images.add(self.img)

        self.product2 = Product.objects.create(
            name="product2",
            description="product1_desc",
            price=5000.00,
            product_composition="product1_pr_cm",
            packaging_standard="product1_packaging",
            expiration_date="product1_ex",
            method_of_application="product1_moa",
        )
        # if field is MtM
        self.product.categories.add(self.cat)
        self.product.images.add(self.img)

        # Формирование корзины
        self.basket1 = Basket.objects.create(
            product=self.product, user=self.superuser, quantity=1
        )

        url = reverse("products:baskets-list")
        data = {"product": self.product.id}
        self.basket2 = self.client.post(url, data).data

        self.product_create_sr_data = ProductCreateSerializer(self.product).data
        self.product_sr_data = ProductSerializer(self.product).data

        self.categories_sr_data = CategorySerializer(self.cat).data
        self.images_sr_data = ImageSerializer(self.img).data

        self.basket_sr_data = BasketSerializer(self.basket1).data

    def test_product_create_serializer(self):
        expected_data = {
            "id": self.product.id,
            "name": "product",
            "description": "product1_desc",
            "price": "10000.00",
            "product_composition": "product1_pr_cm",
            "packaging_standard": "product1_packaging",
            "expiration_date": "product1_ex",
            "method_of_application": "product1_moa",
            "quantity": 0,
        }

        self.assertEqual(self.product_create_sr_data, expected_data)

    def test_product_serializer(self):
        expected_data = {
            "id": self.product.id,
            "name": "product",
            "description": "product1_desc",
            "price": "10000.00",
            "product_composition": "product1_pr_cm",
            "packaging_standard": "product1_packaging",
            "expiration_date": "product1_ex",
            "method_of_application": "product1_moa",
            "quantity": 0,
            "categories": self.product_sr_data["categories"],
            "images": self.product_sr_data["images"],
        }

        self.assertEqual(self.product_sr_data, expected_data)

    def test_categories_serializer(self):
        expected_data = {"id": self.cat.id, "name": self.cat.name}

        self.assertEqual(self.categories_sr_data, expected_data)

    def test_images_serializer(self):
        expected_data = {"id": self.img.id, "img": self.images_sr_data["img"]}

        self.assertEqual(self.images_sr_data, expected_data)

    def test_basket_serializer(self):
        expected_data = {
            "id": self.basket1.id,
            "product": self.basket_sr_data["product"],
            "quantity": 1,
            "created_timestamp": self.basket_sr_data["created_timestamp"],
            "product_sum": 10000.0,
            "total_sum": 20000,
        }

        self.assertEqual(expected_data, self.basket_sr_data)
