from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Image, Product
from products.serializers import ProductSerializer


class ProductsTestCase(APITestCase):
    def setUp(self):
        cat = Category.objects.create(name="cat1")
        img = Image.objects.create(
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
        self.product.categories.add(cat)
        self.product.images.add(img)

    def test_product_list(self):
        url = reverse("products:products-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
