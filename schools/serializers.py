from rest_framework import serializers
from schools.models import School
from users.serializers import ReviewSerializer
from rest_framework.validators import UniqueValidator
from django.urls import reverse
from .validators import (
    validate_name,
    validate_description,
    validate_website,
    validate_contact,
    validate_award,
)
from .models import Bookmark, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "created_at",
            "target_audience",
            "announcement",
            "image",
        ]


class SchoolSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    events = EventSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name="school_detail", lookup_field="pk"
    )
    name = serializers.CharField(
        validators=[
            validate_name,
            UniqueValidator(queryset=School.objects.all(), lookup="iexact"),
        ]
    )
    description = serializers.CharField(validators=[validate_description])
    website = serializers.URLField(validators=[validate_website])
    contact = serializers.CharField(validators=[validate_contact])
    award = serializers.ListField(
        child=serializers.CharField(), validators=[validate_award]
    )

    class Meta:
        model = School
        fields = [
            "url",
            "profile",
            "name",
            "description",
            "location",
            "image",
            "award",
            "school_status",
            "school_type",
            "boarding_status",
            "facility",
            "contact",
            "website",
            "reviews",
            "events",
        ]


# # Example function to get the fully qualified URL for a school
# def get_school_url(school):
#     return reverse("school_detail", kwargs={"pk": school.pk})
class SchoolProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "url",
            "profile",
            "name",
            "description",
            "location",
            "video",
            "image",
            "award",
            "school_status",
            "school_type",
            "boarding_status",
            "facility",
            "contact",
            "website",
            "reviews",
        ]


class SchoolAnalyticsSerializer(serializers.ModelSerializer):
    total_reviews = serializers.ReadOnlyField()
    average_rating = serializers.ReadOnlyField()
    total_bookmarks = serializers.ReadOnlyField()
    monthly_reviews = serializers.ReadOnlyField()
    recent_reviews = serializers.SerializerMethodField()
    engagement_trend = serializers.ReadOnlyField()

    class Meta:
        model = School
        fields = [
            "total_reviews",
            "average_rating",
            "total_bookmarks",
            "monthly_reviews",
            "recent_reviews",
            "engagement_trend",
        ]

    def get_recent_reviews(self, obj):
        return [
            {
                "user": review.user.username,
                "comment": review.comment,
                "rating": review.rating,
            }
            for review in obj.recent_reviews
        ]


class SchoolCompareSerializer(serializers.ModelSerializer):
    average_rating = serializers.ReadOnlyField()
    total_reviews = serializers.ReadOnlyField()
    total_bookmarks = serializers.ReadOnlyField()

    class Meta:
        model = School
        fields = [
            "name",
            "location",
            "city",
            "county",
            "school_type",
            "boarding_status",
            "description",
            "average_rating",
            "total_reviews",
            "facilities",
            "website",
            "contact",
            "award",
            "total_bookmarks",
        ]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = [
            "id",
            "user",
            "school",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]
