import urllib.request

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from products.models import Category, Image, Product
from products.serializers import CategorySerializer, ProductSerializer
from users.models import User


class ProductsTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            email="nik140406@gmail.com", password="nik140406"
        )
        self.client.force_authenticate(user=self.superuser)

        self.cat = Category.objects.create(name="cat1")
        self.cat2 = Category.objects.create(name="cat2")
        self.img = Image.objects.create(
            img="https://img.freepik.com/free-photo/young-adult-enjoying-yoga-in-nature_23-2149573175.jpg"
        )

        self.product = Product.objects.create(
            name="product1",
            description="product1_desc",
            price="9999.00",
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
            price="9999.00",
            product_composition="product2_pr_cm",
            packaging_standard="product2_packaging",
            expiration_date="product2_ex",
            method_of_application="product2_moa",
        )
        # if field is MtM
        self.product2.categories.add(self.cat)
        self.product2.images.add(self.img)

        self.pr_serializer = ProductSerializer(self.product)
        self.ct_serializer = CategorySerializer(self.cat)

    def test_product_list(self):
        # Отправляем GET на url
        url = reverse("products:products-list")
        response = self.client.get(url)
        expected_data_length = 2

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)
        self.assertContains(response, self.pr_serializer.data["name"])

    def test_product_detail(self):
        url = f"{settings.DOMAIN_NAME}/api/products/{self.product.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), 1)
        self.assertContains(response, self.pr_serializer.data["name"])

    def test_product_create(self):
        url = reverse("products:categories-list")
        data = {"name": "Regular"}
        # data = {'name': "product23",
        #         'description': "product23_desc",
        #         'price': "9999.00",
        #         'product_composition': "product23_pr_cm",
        #         'packaging_standard': "product32_packaging",
        #         'expiration_date': "product23_ex",
        #         'method_of_application': "product23_moa",
        #         'categories': 'cat1',
        #         'images': [{'img': image}]
        #         }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Regular")

    def test_category_list(self):
        # Отправляем GET запрос
        url = reverse("products:categories-list")
        response = self.client.get(url)
        expected_data_length = 2

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), expected_data_length)

    def test_category_detail(self):
        url = f"{settings.DOMAIN_NAME}/api/categories/{self.cat.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len([response.data]), 1)
        self.assertContains(response, self.ct_serializer.data["name"])
