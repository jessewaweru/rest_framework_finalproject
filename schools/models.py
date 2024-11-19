from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from datetime import datetime, timedelta
from django.core.validators import FileExtensionValidator
from rest_framework.validators import ValidationError

# from Users.models import SchoolUserProfile
from django.apps import apps


class Event(models.Model):
    """Its a model for the events section for a school profile
    where schools can showcase their announcements"""

    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    target_audience = models.CharField(
        max_length=200,
        choices=[
            ("parents", "Parents"),
            ("teachers", "Teachers"),
            ("public", "Public"),
        ],
        default="public",
    )
    announcement = models.TextField()
    image = models.ImageField(upload_to="schools/events/images/", null=True, blank=True)

    def __str__(self):
        return f"{self.title}for{self.school.name}"


class School(models.Model):
    profile = models.OneToOneField(
        "users.User",  # Reference the model by its app label and model name as a string
        on_delete=models.CASCADE,
        related_name="profile",
    )
    views = models.PositiveIntegerField(default=0)
    name = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=200, default="Kenya")
    county = models.CharField(max_length=200, default="Kenya")
    PUBLIC = "public"
    PRIVATE = "private"
    SCHOOL_STATUS_CHOICES = [(PUBLIC, "public"), (PRIVATE, "private")]
    school_status = models.CharField(
        max_length=7, choices=SCHOOL_STATUS_CHOICES, default=PUBLIC
    )
    KINDERGARTEN = "kindergarten"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    SCHOOL_TYPE_CHOICE = [
        (KINDERGARTEN, "Kindergarten"),
        (PRIMARY, "Primary"),
        (SECONDARY, "Secondary"),
    ]
    school_type = models.CharField(
        max_length=12,
        choices=SCHOOL_TYPE_CHOICE,
        default=PRIMARY,
    )
    BOARDING = "boarding"
    NON_BOARDING = "non_boarding"
    BOARDING_STATUS = [
        (BOARDING, "Boarding"),
        (NON_BOARDING, "Non-boarding"),
    ]
    boarding_status = models.CharField(
        max_length=12,
        choices=BOARDING_STATUS,
        default=NON_BOARDING,
    )
    video = models.FileField(
        upload_to="schools/videos",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi"]),
        ],
    )
    image = models.ImageField(upload_to="schools/images/", null=True, blank=True)
    award = models.CharField(max_length=300, blank=True)
    facility = models.TextField(blank=True)
    contact = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)

    @property
    def total_reviews(self):
        return self.reviews.count()

    # @property
    # def average_rating(self):
    #     avg_rating = self.reviews.aggregate(Avg("rating"["rating_avg"]))
    #     return avg_rating if avg_rating else "No average ratings"
    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(Avg("rating"))  # Correcting the syntax here
        return (
            avg_rating["rating__avg"]
            if avg_rating["rating__avg"] is not None
            else "No average ratings"
        )

    @property
    def total_bookmarks(self):
        return self.bookmarked_by.count()

    @property
    def monthly_reviews(self):
        return self.reviews.filter(created_at=datetime.now().month).count()

    @property
    def recent_reviews(self):
        return self.reviews.order_by("-created_at")[:5]

    @property
    def engagement_trend(self):
        last_month = datetime.now() - timedelta(days=30)
        recent_bookmarks = self.bookmarked_by.filter(created_at__gte=last_month).count()
        recent_reviews = self.reviews.filter(created_at__gte=last_month).count()
        return {"recent_bookmarks": recent_bookmarks, "recent_reviews": recent_reviews}

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.profile.is_school:
            raise ValueError(
                "School Profile can only be created by school account holders."
            )
        # Ensure profile is set before saving
        if not self.profile:
            raise ValueError("School profile must be linked to a valid user profile.")
        super().save(*args, **kwargs)

    # applied to the video field
    def clean(self, *args, **kwargs):
        super().clean()
        if self.video and self.video.size > settings.MAX_VIDEO_UPLOAD_SIZE:
            raise ValidationError(
                "The video file is too large. Maximum size allowed is 50 MB."
            )

    def __str__(self):
        return f"School:{self.name}"


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks"
    )
    school = models.ForeignKey(
        "School", on_delete=models.CASCADE, related_name="bookmarked_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "school")

    def __str__(self):
        return f"{self.user.username}bookmarked{self.school.name}"
