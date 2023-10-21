from django.urls import path, include
from django.conf import settings

from rest_framework import routers
from .views import OrderModelViewSet, OrderCreateView, YookassaWebhookView


app_name = 'orders'

router = routers.DefaultRouter()
router.register(r'orders', OrderModelViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path("order/create/", OrderCreateView.as_view(), name='order_create'),
    path("yookassa/webhook/", YookassaWebhookView.as_view(), name='yookassa_webhook'),
]