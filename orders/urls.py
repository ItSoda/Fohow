from django.conf import settings
from django.urls import include, path
from rest_framework import routers

from .views import OrderCreateView, OrderModelViewSet, YookassaWebhookView

app_name = "orders"

router = routers.DefaultRouter()
router.register(r"orders", OrderModelViewSet, basename="orders")


urlpatterns = [
    path("", include(router.urls)),
    path("order/create/", OrderCreateView.as_view(), name="order_create"),
    path("yookassa/webhook/", YookassaWebhookView.as_view(), name="yookassa_webhook"),
]
