from tempfile import NamedTemporaryFile
from urllib.request import urlopen

from django.core.files import File
from rest_framework import fields, serializers

from .models import Basket, Category, Image, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


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
        fields = ("img",)


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True, slug_field="name", read_only=True
    )
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    # Методы корзины
    sum = fields.FloatField(
        required=False
    )  # required  отвечает за то что это поле обязательное
    total_sum = fields.SerializerMethodField()

    class Meta:
        model = Basket
        fields = (
            "id",
            "product",
            "quantity",
            "sum",
            "total_sum",
            "created_timestamp",
        )
        read_only_fields = ("created_timestamp",)

    def get_total_sum(self, obj):
        return Basket.basketmanager.filter(user_id=obj.user.id).total_sum()
