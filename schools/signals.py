from django.db.models.signals import post_save
from django.dispatch import receiver
from schools.models import School


@receiver(post_save, sender=School)
def created_school(sender, instance, created, **kwargs):  # Added **kwargs
    if created:
        print("New school was added successfully.")


@receiver(post_save, sender=School)
def updated_school(sender, instance, created, **kwargs):  # Added **kwargs
    if not created:
        print("School profile updated successfully.")
