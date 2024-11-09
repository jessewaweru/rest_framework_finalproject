from django.db import models
from django.conf import settings
from django.db.models import Avg, Count
from datetime import datetime, timedelta

# from Users.models import SchoolUserProfile
from django.apps import apps


class School(models.Model):
    profile = models.OneToOneField(
        "users.User",  # Reference the model by its app label and model name as a string
        on_delete=models.CASCADE,
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
    image = models.ImageField(upload_to="schools/images/", null=True, blank=True)
    award = models.CharField(max_length=300, blank=True)
    facility = models.TextField(blank=True)
    contact = models.CharField(max_length=15, blank=True)
    website = models.URLField(blank=True)

    @property
    def total_reviews(self):
        return self.reviews.count()

    @property
    def average_rating(self):
        avg_rating = self.reviews.aggregate(Avg("rating"["rating_avg"]))
        return avg_rating if avg_rating else "No average ratings"

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
