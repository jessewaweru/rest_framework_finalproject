from random import randint
from django.core.mail import send_mail
from .models import OTP


def send_otp_email(user):
    code = f"{randint(100000,999999)}"
    OTP.objects.update_or_create(user=user, defaults={"code": code})

    send_mail(
        subject="Your OTP code",
        message=f"Your OTP code is {code}. It's valid for 5 minutes.",
        from_email="blake@gmail.com",
        recipient_list=[user.email],
    )
