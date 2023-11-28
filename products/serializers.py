from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from rest_framework import serializers
from users.models import User

from users.serializers import UserSerializer

from .models import Category, Image, Product, Reviews
from .services import product_instance, review_instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class ImageFieldFromURL(serializers.ImageField):
    def to_internal_value(self, data):
        # Проверяем, если data - это URL
        if data.startswith("http") or data.startswith("https"):
            # Открываем URL и читаем его содержимое
            response = urlopen(data)
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.read())
            img_temp.flush()
            # Создаем объект File из временного файла
            img = File(img_temp)
            # Возвращаем его как значение поля
            return img
        return super().to_internal_value(data)


class ImageSerializer(serializers.ModelSerializer):
    img = ImageFieldFromURL()

    class Meta:
        model = Image
        fields = (
            "id",
            "name",
            "img",
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    categories = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    images = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        categories_ids = validated_data.pop("categories")
        images_ids = validated_data.pop("images")
        return product_instance(categories_ids, images_ids, **validated_data)


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    images = ImageSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True)
    product = serializers.IntegerField(write_only=True)

    class Meta:
        model = Reviews
        fields = "__all__"

    def create(self, validated_data):
        user_id = validated_data.pop("user")
        product_id = validated_data.pop("product")
        return review_instance(user_id=user_id, product_id=product_id, **validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Reviews
        fields = "__all__"