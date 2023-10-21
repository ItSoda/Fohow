from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=Order)
def order_post_save(instance, **kwargs):
    if instance.status == 1:
        subjects = f'Fohow | Успешная оплата заказа на аккаунте {instance.initiator.email}'
        message = 'Поздравляем, вы успешно оплатили заказ на нашем сайте \n Fohow'
        send_mail(
            subject=subjects,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.initiator.email],
            fail_silently=False,
        )

    if instance.status == 3:
        subjects = f'Fohow | Ваш заказ доставлен {instance.initiator.email}'
        message = 'Скорее забирайте ваш заказ. Время бесплатного хранения на складе 2 недели \n Fohow'
        send_mail(
            subject=subjects,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.initiator.email],
            fail_silently=False,
        )
