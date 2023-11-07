from products.models import Basket


# MODELS METHODS
# Order
def update_after_success_payments(self):
    baskets = Basket.objects.filter(user=self.initiator)
    self.status = self.PAID
    purchased_item = []
    total_price = 0.0

    for basket in baskets:
        purchased_item.append(basket.de_json())
        total_price += basket.product_sum()

    self.basket_history = {
        "purchased_item": purchased_item,
        "total_price": total_price,
    }
    baskets.delete()
    self.save()


def update_after_canceled_payments(self):
    baskets = Basket.objects.filter(user=self.initiator)
    self.status = self.NOT_PAID
    baskets.delete()
    self.save()


# Views
def order_queryset_filter_initiator(queryset, self):
    return queryset.filter(initiator=self.request.user)


def serializer_valid(request):
    from .serializers import OrderSerializer

    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        return serializer, True
    return serializer, False


def create_order_with_payment(self, request, serializer):
    from django.conf import settings
    from yookassa import Configuration, Payment

    # Сохраните заказ
    order = serializer.save(initiator=request.user)
    # Здесь получите необходимые параметры для создания платежа
    # Например, сумму платежа и описание
    baskets = Basket.objects.filter(user=self.request.user)
    order_id = order.id
    order_products = [basket.product.name for basket in baskets]
    order_price = Basket.basketmanager.total_sum()

    # Настройте ключи доступа
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY
    # Создайте объект платежа
    payment = Payment.create(
        {
            "amount": {
                "value": str(order_price),
                "currency": "RUB",
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.YOOKASSA_REDIRECT_URL,
            },
            "capture": True,
            "save_payment_method": True,
            "description": f"Order #{order_id}",
            "metadata": {
                "order_id": order_id,
                "order_products": ", ".join(order_products),
            },
        }
    )
    return payment.confirmation.confirmation_url, order_price


def order_metadata_id(notification):
    from orders.models import Order

    order_id = notification.object.metadata.get("order_id")
    return Order.objects.get(id=order_id)
