from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Basket, Category, Image, Product
from users.models import User


class ProductsTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.client.force_authenticate(user=self.superuser)

        self.cat = Category.objects.create(name="cat1")
        self.img = Image.objects.create(
            img="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg"
        )

        self.product = Product.objects.create(
            name="product1",
            description="product1_desc",
            price="10000.00",
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
            description="product2_desc",
            price="5000.00",
            product_composition="product2_pr_cm",
            packaging_standard="product2_packaging",
            expiration_date="product2_ex",
            method_of_application="product2_moa",
        )
        # if field is MtM
        self.product2.categories.add(self.cat)
        self.product2.images.add(self.img)

    def test_product_list(self):
        # Отправляем GET на url
        url = reverse("products:products-list")
        response = self.client.get(url)
        expected_data_length = 2

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)

    def test_product_create(self):
        url = reverse("products:products-list")
        data = {
            "name": "product23",
            "description": "product23_desc",
            "price": "9999.00",
            "product_composition": "product23_pr_cm",
            "packaging_standard": "product32_packaging",
            "expiration_date": "product23_ex",
            "method_of_application": "product23_moa",
            "categories": [self.cat.id],
            "images": [self.img.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_product_detail(self):
        url = f"{settings.DOMAIN_NAME}/api/products/{self.product.id}/"
        response = self.client.get(url)
        expected_data_length = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), expected_data_length)

    def test_product_partial_update(self):
        url = f"{settings.DOMAIN_NAME}/api/products/{self.product.id}/"
        data = {"name": "product_1"}
        response = self.client.patch(url, data)
        expected_data_length = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), expected_data_length)
        self.assertEqual(response.data["name"], "product_1")

    def test_product_destroy(self):
        url = f"{settings.DOMAIN_NAME}/api/products/{self.product.id}/"
        response = self.client.delete(url)
        expected_data_length = 1

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), expected_data_length)


class CategoryTests(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.client.force_authenticate(user=self.superuser)
        self.cat1 = Category.objects.create(name="cat1")
        self.cat2 = Category.objects.create(name="cat2")

    def test_category_list(self):
        # Отправляем GET запрос
        url = reverse("products:categories-list")
        response = self.client.get(url)
        expected_data_length = 2

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)

    def test_category_create(self):
        url = reverse("products:categories-list")
        data = {"name": "Regular"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Regular")

    def test_category_detail(self):
        url = f"{settings.DOMAIN_NAME}/api/categories/{self.cat1.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), 1)

    def test_category_partial_update(self):
        url = f"{settings.DOMAIN_NAME}/api/categories/{self.cat1.id}/"
        data = {"name": "cat_1"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "cat_1")

    def test_category_destroy(self):
        url = f"{settings.DOMAIN_NAME}/api/categories/{self.cat1.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)


class BasketTests(APITestCase):
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
        url = reverse("products:baskets-list")
        data = {"product": self.product1.id}
        self.basket1 = self.client.post(url, data).data

        url = reverse("products:baskets-list")
        data = {"product": self.product.id}
        self.basket2 = self.client.post(url, data).data

    def test_basket_create(self):
        url = reverse("products:baskets-list")
        data = {"product": self.product2.id}
        response = self.client.post(url, data)
        expected_data = 1
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len([response.data]), expected_data)
        self.assertEqual(response.data["product_sum"], 5000.00)

    def test_basket_list(self):
        url = reverse("products:baskets-list")
        response = self.client.get(url)
        expected_data = 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data)
        self.assertEqual(response.data[-2]["total_sum"], 15000.00)

    def test_basket_detail(self):
        url = f"{settings.DOMAIN_NAME}/api/baskets/{self.basket1['id']}/"
        response = self.client.get(url)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), expected_data)
        self.assertEqual(response.data["product_sum"], 5000.00)
        self.assertEqual(response.data["total_sum"], 15000.00)
        self.assertEqual(response.data["product"]["name"], "product1")

    def test_basket_partial_update(self):
        url = f"{settings.DOMAIN_NAME}/api/baskets/{self.basket1['id']}/"
        data = {"quantity": 2}
        response = self.client.patch(url, data)
        expected_data = 1

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), expected_data)
        self.assertEqual(response.data["product_sum"], 10000.00)
        self.assertEqual(response.data["total_sum"], 20000.00)

    def test_basket_partial_destroy(self):
        url = f"{settings.DOMAIN_NAME}/api/baskets/{self.basket1['id']}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Basket.objects.count(), 1)
