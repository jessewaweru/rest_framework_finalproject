from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Review
from .models import Notification
from django.core.mail import send_mail
from django.conf import settings
from schools.models import School, Bookmark


# @receiver(post_save, sender=User)
# def welcome_user_notification(instance, created, **kwargs):
#     if created:
#         message = f"Welcome,{instance.username}!Profile was created successfully."
#         Notification.objects.create(user=instance, message=message)
#         try:
#             send_mail(
#                 subject="Welcome to Amarock Schools.",
#                 message="Thank you for registering with us.",
#                 from_email=settings.EMAIL_HOST_USER,
#                 recipient_list=[instance.email],
#                 fail_silently=True,
#             )
#         except Exception as e:
#             print(f"Failed to send email:{e}")


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
