from django.db import models


class Admin(models.Model):
    UUID = models.CharField(max_length=50)

    class Meta:
        verbose_name = "админа"
        verbose_name_plural = "ТГ бот - админы"

    def __str__(self) -> str:
        return f"{self.UUID}"


class UserBot(models.Model):
    """БД для хранения данных о пользователях"""

    user_id = models.BigIntegerField(verbose_name="USER ID", unique=True)

    username = models.CharField(max_length=256, null=True, blank=True)

    first_name = models.CharField(
        verbose_name="Name",
        max_length=256,
    )

    last_name = models.CharField(max_length=256, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "тг-юзер"
        verbose_name_plural = "тг-юзеры"


class News(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    photo = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = "новость"
        verbose_name_plural = "Новости"

    def __str__(self) -> str:
        return f"{self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)