from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from .managers import CustomUserManager


# User Model
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified_email = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь {self.email} | {self.first_name}"


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse(
            "users:email_verify", kwargs={"email": self.user.email, "code": self.code}
        )
        full_link = f"{settings.DOMAIN_NAME}{link}"
        subjects = f"Подтверждение учетной записи для {self.user.email}"
        message = (
            "Для подтверждения электронной почты {} перейдите по ссылке: {}.".format(
                self.user.email,
                full_link,
            )
        )
        send_mail(
            subject=subjects,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        if now() >= self.expiration:
            self.delete()
            self.save()
            return True
        return False
