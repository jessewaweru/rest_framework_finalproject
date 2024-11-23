from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import User, UserProfile
from django.core.mail import send_mail
from django.conf import settings
from schools.models import School


@receiver(post_save, sender=User)
def manage_user_and_school_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the user is a school
        if instance.is_school:
            School.objects.create(profile=instance)
            print("School profile created for school user.")
        else:
            UserProfile.objects.create(user=instance)
            print("User profile created for regular user.")

    else:
        # Update the UserProfile if it exists for non-school users
        if not instance.is_school:
            user_profile, _ = UserProfile.objects.update_or_create(user=instance)
            user_profile.save()


@receiver(post_save, sender=School)
def prompt_school_profile_completion(sender, instance, created, **kwargs):
    if created:
        print("Redirecting to school profile completion page.")


@receiver(post_delete, sender=User)
def confirm_delete(sender, instance, **kwargs):
    print(f"User {instance.username} and all related fields have been deleted.")


@receiver(post_save, sender=User)
def welcome_user(sender, instance, created, **kwargs):
    if created:
        try:
            send_mail(
                subject="Welcome to Amarock Schools.",
                message="Thank you for registering with us.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Failed to send email:{e}")
