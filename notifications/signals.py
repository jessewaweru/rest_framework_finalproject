from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Review
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings
from schools.models import School, Bookmark
from users.utils import send_otp_email


@receiver(post_save, sender=User)
def send_otp(instance, created, **kwargs):
    if created:
        try:
            send_otp_email(instance)
            print("OTP email sent successfully")
        except Exception as e:
            print(f"Failed to send OTP email: {e}")


@receiver(post_save, sender=Review)
def new_review_notice(instance, created, **kwargs):
    if created:
        school_user = instance.school.profile
        message = f"Your school just got a new review"
        Notification.objects.create(user=school_user, message=message)


@receiver(post_save, sender=Bookmark)
def new_bookmark_notice(instance, created, **kwargs):
    if created:
        school_user = instance.school.profile
        message = f"Your school was just bookmarked"
        Notification.objects.create(user=school_user, message=message)


@receiver(post_save, sender=School)
def new_update_notice(instance, created, **kwargs):
    if created:
        message = f"Your school profile has just been updates"
        Notification.objects.create(user=instance.profile, message=message)
