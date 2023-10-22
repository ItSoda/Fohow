import json
import logging

from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationFactory

from Fohow.permissions import IsAdminOrReadOnly
from orders.models import Order
from orders.serializers import OrderSerializer
from products.models import Basket

logger = logging.getLogger(__name__)


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = None

    def get_queryset(self):
        queryset =  super(OrderModelViewSet, self).get_queryset()
        return queryset.filter(initiator=self.request.user)
    
    
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderCreateView(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
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
            payment = Payment.create({
                'amount': {
                    'value': str(order_price),
                    'currency': 'RUB',
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': settings.YOOKASSA_REDIRECT_URL
                },
                "capture": True,
                "save_payment_method": True,
                'description': f'Order #{order_id}',
                'metadata': {
                    'order_id': order_id,
                    'order_products': ', '.join(order_products),
                },
            })

            # Перенаправьте пользователя на страницу оплаты Юкассы
            return Response({'payment_url': payment.confirmation.confirmation_url, 'order_price': order_price})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YookassaWebhookView(APIView):
    def post(self, request):
        event_json = json.loads(request.body.decode("utf-8"))

        try:
            logger.info(f'Responce: {event_json}')
            notification = WebhookNotificationFactory().create(event_json)
            logger.info('Webhook is create')
            # Получаем айди заказа из метаданных уведомления
            order_id = notification.object.metadata.get('order_id')
            order = Order.objects.get(id=order_id)
            # Проверяем статус платежа
            if notification.object.status == 'succeeded':
                logger.info('good')
                order.update_after_success_payments()
                # Обновляем статус заказа
            elif notification.object.status == 'canceled':
                logger.info('bad')
                order.update_after_canceled_payments()
                # Обновляем статус заказа
        except Exception as e:
            logger.info('Ошибка создания вебхука %s', str(e))
                    # Обработка ошибок при разборе уведомления
        return HttpResponse(status=200)
