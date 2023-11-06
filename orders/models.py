from django.db import models

from products.models import Basket
from users.models import User

from .services import (update_after_canceled_payments,
                       update_after_success_payments)


class Order(models.Model):
    NOT_PAID = -1
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (NOT_PAID, "Не оплачен"),
        (CREATED, "Создан"),
        (PAID, "Оплачен"),
        (ON_WAY, "В пути"),
        (DELIVERED, "Доставлен"),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order #{self.id} | {self.first_name} {self.last_name}"

    def update_after_success_payments(self):
        update_after_success_payments(self)

    def update_after_canceled_payments(self):
        update_after_canceled_payments(self)
