from rest_framework import serializers
from schools.models import School
from .models import Event
from users.serializers import ReviewSerializer
from rest_framework.validators import UniqueValidator
from .validators import (
    validate_name,
    validate_description,
    validate_website,
    validate_contact,
    validate_rating,
    # validate_performance_file,
)
from .models import Bookmark
from django.db.models import Avg


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
        view_name="school-detail",
        lookup_field="pk",
    )
    name = serializers.CharField(
        validators=[
            validate_name,
            UniqueValidator(queryset=School.objects.all(), lookup="iexact"),
        ]
    )
    description = serializers.CharField(validators=[validate_description])
    rating = serializers.IntegerField(validators=[validate_rating])
    performance_data = serializers.SerializerMethodField()

    def get_performance_data(self, obj):
        return obj.performance_data

    website = serializers.URLField(validators=[validate_website])
    contact = serializers.CharField(validators=[validate_contact])

    class Meta:
        model = School
        fields = [
            "url",
            "profile",
            "name",
            "description",
            "location",
            "image",
            "school_status",
            "school_type",
            "boarding_status",
            "facility",
            "award",
            "rating",
            "performance_data",
            "contact",
            "website",
            "reviews",
            "events",
        ]


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
            "school_status",
            "school_type",
            "boarding_status",
            "facility",
            "award",
            "rating",
            "performance_file",
            "performance_data",
            "contact",
            "website",
            "reviews",
            "events",
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


class SchoolBaseAnalyticsSerializer(serializers.ModelSerializer):
    views = serializers.IntegerField()
    bookmark_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()
    recent_reviews = ReviewSerializer(source="review_set", many=True)

    class Meta:
        model = School
        fields = [
            "views",
            "bookmark_count",
            "average_rating",
            "total_reviews",
            "recent_reviews",
        ]

    def get_bookmark_count(self, obj):
        return obj.bookmarked_by.count()

    def get_average_rating(self, obj):
        return obj.review_set.aggregate(Avg("rating"))["rating__avg"] or 0

    def get_total_reviews(self, obj):
        return obj.review_set.count()


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
