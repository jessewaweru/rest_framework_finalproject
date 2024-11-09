from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import User, UserProfile
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_school:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, created, **kwargs):
    instance.userprofile.save()


@receiver(post_delete, sender=User)
def confirm_delete(sender, instance, **kwargs):
    print(f"User {instance.username} and all related fields have been deleted.")


# @receiver(post_save, sender=User)
# def welcome_user(sender, instance, created, **kwargs):
#     if created:
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
