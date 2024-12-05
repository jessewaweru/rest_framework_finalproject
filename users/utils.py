from random import randint
from django.core.mail import send_mail
from .models import OTP
from django.utils.timezone import now
from .models import User
from datetime import timedelta
import random


# def send_otp_email(user, otp):
#     code = f"{randint(100000,999999)}"
#     expiration_time = now() + timedelta(minutes=10)
#     OTP.objects.update_or_create(
#         user=user,
#         defaults={"code": code, "created_at": now(), "expires_at": expiration_time},
#     )
#     try:
#         send_mail(
#             subject="Your OTP code",
#             message=f"Your OTP code is {code}. It's valid for 10 minutes.",
#             from_email="no-reply@yourproject.com",
#             recipient_list=[user.email],
#         )
#         print(f"OTP email sent to {user.email}:{code}")
#     except Exception as e:
#         print(f"failed to send OTP email:{e}")


def send_otp_email(user, otp=None, expires_at=None):
    """
    Sends an OTP email to the user. Generates a new OTP if not provided.

    """
    if not otp or not expires_at:
        # Generate a new OTP if not provided
        otp_code = str(random.randint(100000, 999999))
        expires_at = now() + timedelta(minutes=10)

        OTP.objects.update_or_create(
            user=user,
            defaults={"code": otp_code, "created_at": now(), "expires_at": expires_at},
        )
        otp = otp_code

    # Sending email logic
    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}. It's valid for 10 minutes."

    try:
        send_mail(
            subject,
            message,
            "no-reply@example.com",  # Replace with your actual sender email
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send OTP email: {e}")


def generate_new_otp(user):
    """
    Generates a new OTP for a given user upon request . Deletes expired OTPs if necessary.
    """

    # Remove expired OTP if it exists
    existing_otp = OTP.objects.filter(user=user).first()
    if existing_otp and existing_otp.expires_at < now():
        existing_otp.delete()

    # Generate new OTP
    otp_code = str(random.randint(100000, 999999))
    new_otp, created = OTP.objects.update_or_create(
        user=user,
        defaults={
            "code": otp_code,
            "created_at": now(),
            "expires_at": now() + timedelta(minutes=10),
        },
    )
    return new_otp, created
