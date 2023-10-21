from rest_framework import serializers
from .models import Order
from users.models import User


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display", read_only=True)
    initiator = serializers.SlugRelatedField(
        queryset = User.objects.all(),
        slug_field='id'
    )
    class Meta:
        model = Order
        fields = '__all__'