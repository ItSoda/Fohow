from rest_framework import fields, serializers

from .models import Basket, Category, Image, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name",)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ("img",)


class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    images = ImageSerializer(many=True)

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
