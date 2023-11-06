from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now


def send_verification_email(user_email, code):
    link = reverse("users:email_verify", kwargs={"email": user_email, "code": code})
    full_link = f"{settings.DOMAIN_NAME}{link}"
    subjects = f"Подтверждение учетной записи для {user_email}"
    message = "Для подтверждения электронной почты {} перейдите по ссылке: {}.".format(
        user_email,
        full_link,
    )
    send_mail(
        subject=subjects,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )


def is_expired(self):
    if now() >= self.expiration:
        self.delete()
        self.save()
        return True
    return False
