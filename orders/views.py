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
from orders.services import (create_order_with_payment, order_metadata_id,
                             order_queryset_filter_initiator, serializer_valid)
from products.models import Basket

logger = logging.getLogger(__name__)


class OrderModelViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

    def get_queryset(self):
        queryset = super(OrderModelViewSet, self).get_queryset()
        return order_queryset_filter_initiator(queryset, self)

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer, valid = serializer_valid(request)
        if valid:
            payment_url, order_price = create_order_with_payment(
                self, request, serializer
            )
            # Перенаправьте пользователя на страницу оплаты Юкассы
            return Response(
                {
                    "payment_url": payment_url,
                    "order_price": order_price,
                }
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YookassaWebhookView(APIView):
    def post(self, request):
        event_json = json.loads(request.body.decode("utf-8"))

        try:
            logger.info(f"Responce: {event_json}")
            notification = WebhookNotificationFactory().create(event_json)
            logger.info("Webhook is create")
            # Получаем айди заказа из метаданных уведомления
            order = order_metadata_id(notification)
            # Проверяем статус платежа
            if notification.object.status == "succeeded":
                logger.info("good")
                order.update_after_success_payments()
                # Обновляем статус заказа
            elif notification.object.status == "canceled":
                logger.info("bad")
                order.update_after_canceled_payments()
                # Обновляем статус заказа
        except Exception as e:
            logger.info("Ошибка создания вебхука %s", str(e))
            # Обработка ошибок при разборе уведомления
        return HttpResponse(status=200)
