from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps
from schools.models import School


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ("parent", "Parent"),
        ("teacher", "Teacher"),
        ("student", "Student"),
        ("other", "Other"),
    ]
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="parent"
    )
    is_school = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_school_profile(self):
        """Returns the associated School instance for this user, if it exists."""
        try:
            return School.objects.get(profile=self)
        except ObjectDoesNotExist:
            return None

    def get_user_by_id(id):
        return School.objects.get(id=id)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=200, default="Kenya")
    county = models.CharField(max_length=200, default="Kenya")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def delete_related_data(self):
        self.reviews.all().delete()
        self.bookmarks.all().delete()
        self.notifications.all().delete()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(
        "schools.School",  # Reference the model by its app label and model name as a string
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} for {self.school.name}"
