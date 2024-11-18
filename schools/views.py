from rest_framework import generics
from schools.models import School
from schools.serializers import SchoolSerializer
from api.mixins import IsStaffPermissionMixin
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Bookmark, School
from django.contrib.auth import get_user_model
from users.models import Review
from django.db.models import Avg
from users.serializers import ReviewSerializer
from .serializers import (
    SchoolProfileSerializer,
    SchoolAnalyticsSerializer,
    SchoolCompareSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from users.models import History
from django.utils import timezone

User = get_user_model()

logger = logging.getLogger(__name__)


class SchoolListCreateAPIView(IsStaffPermissionMixin, generics.ListCreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(
                f"School created successfully:{response.data.get('name','unknown')}"
            )
            return response
        except ValidationError as e:
            logger.error(f"Validation error during school creation:{e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # logger.error(" An unexpected error occured during school creation")
            logger.error(f"Unexpected error occured in school creation:{e}")
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


school_list_create_view = SchoolListCreateAPIView.as_view()


class SchoolDetailAPIView(IsStaffPermissionMixin, generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        school = self.get_object()
        if request.user.is_authenticated:
            # Log the history entry for the viewed school
            History.objects.create(
                user=request.user, school=school, viewed_at=timezone.now()
            )
        # Call the parent class's `get` method to continue with the usual response
        return super().get(request, *args, **kwargs)


school_detail_view = SchoolDetailAPIView.as_view()


class SchoolUpdateAPIView(IsStaffPermissionMixin, generics.UpdateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    lookup_field = "pk"


school_update_view = SchoolUpdateAPIView.as_view()


class SchoolDestroyAPIView(IsStaffPermissionMixin, generics.DestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


school_destroy_view = SchoolDestroyAPIView.as_view()

""" Views handling the analytics dashboard for the school profile through the school model """


# SchoolProfileView displays the profile of a single school linked to the currently authenticated user
class SchoolProfileView(APIView):
    permission_classes = [IsStaffPermissionMixin]

    def get(self, request):
        school = get_object_or_404(School, user=request.user)
        serializer = SchoolProfileSerializer(school)
        return Response(serializer.data)


school_profile = SchoolProfileView.as_view()


class SchoolAnalyticsView(APIView):
    permission_classes = [IsStaffPermissionMixin]

    def get(self, request):
        school = get_object_or_404(School, user=request.user)
        serializer = SchoolAnalyticsSerializer(school)
        return Response(serializer.data)


school_analytics = SchoolAnalyticsView.as_view()


class BookmarkAPIView(APIView):
    def post(self, request, pk):
        """I am adding a bookmark for a school"""
        user = request.user
        if user.is_school:
            return Response(
                {"detail": "Only non-school profile accounts can bookmark a school"},
                status=status.HTTP_403_FORBIDDEN,
            )
        school = get_object_or_404(School, id=pk)
        bookmark, created = Bookmark.objects.get_or_create(user=user, school=school)
        if created:
            return Response(
                {"detail": "School has been successfully bookmarked"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"detail": "School is already bookmarked"}, status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        """Deleting a school bookmark"""
        user = request.user
        if user.is_school:
            return Response(
                {"detail": "Only non-school profile accounts can bookmark a school"},
                status=status.HTTP_403_FORBIDDEN,
            )
        school = get_object_or_404(School, id=pk)
        try:
            bookmark = Bookmark.objects.get(user=user, school=school)
            bookmark.delete()
            return Response(
                {"detail": "Bookmark was successfully removed"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Bookmark.DoesNotExist:
            return Response(
                {"detail": "Bookmark not found"}, status=status.HTTP_404_NOT_FOUND
            )


bookmark_view = BookmarkAPIView.as_view()


"""ViewSet for retrieving various analytics on a school profile."""


class SchoolBaseAnalyticsViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        school = get_object_or_404(School, pk=pk)
        serializer = SchoolAnalyticsSerializer(school)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def views(self, request, pk=None):
        """Return and increment the views count for a school"""
        school = get_object_or_404(School, pk=pk)
        school.views += 1
        school.save(update_fields=["views"])
        return Response({"views": school.views})

    @action(detail=True, methods=["get"])
    def bookmarks(self, request, pk=None):
        """Return the bookmark count for a school"""
        school = get_object_or_404(School, pk=pk)
        bookmark_count = school.bookmarked_by.count()
        return Response({"bookmark_count": bookmark_count})

    @action(detail=True, methods=["get"])
    def engagement_metrics(self, request, pk=None):
        """Calculate and return engagement metrics for a school"""
        school = get_object_or_404(School, pk=pk)
        reviews = school.review_set.all()
        average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
        total_reviews = reviews.count()

        return Response(
            {"average_rating": average_rating, "total_reviews": total_reviews}
        )

    @action(detail=True, methods=["get"])
    def recent_reviews(self, request, pk=None):
        """Return the 5 most recent reviews for a school"""
        school = get_object_or_404(School, pk=pk)
        recent_reviews = school.review_set.order_by("-created_at")[:5]
        serializer = ReviewSerializer(recent_reviews, many=True)
        return Response(serializer.data)


"""
API view for comparing up to 3 schools based on various attributes.
"""


class SchoolComparisonAPIView(APIView):
    def post(self, request):
        # Extract school IDs from request data and remove duplicates
        school_ids = list(set(request.data.get("schools_ids", [])))

        if not school_ids:
            return Response(
                {"error": "Please provide school IDs to compare."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(school_ids) > 3:
            return Response(
                {
                    "error": "Only a maximum of three schools can be compared against each other."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        schools = get_list_or_404(School, id__in=school_ids)
        serializer = SchoolCompareSerializer(schools, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


school_comparison_view = SchoolComparisonAPIView.as_view()


"""
This is the API handling the redeirection of school profile accounts 
that are tied to their users who created them

"""


class CompleteSchoolProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

    def get(self, request, *args, **kwargs):
        school = get_object_or_404(School, profile=request.user)
        if not school.name and school.location:
            return Response(
                {"detail": "Please provide details for the school profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(SchoolSerializer(school).data)

    def update(self, request, *args, **kwargs):
        school = get_object_or_404(School, profile=request.user)
        serializer = self.get_serializer(school, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


complete_school_profile = CompleteSchoolProfileAPIView.as_view()

# # Visitor Analytics- get stats for number of school page views by a normal user
# class SchoolViewsAPIView(APIView):
#     def get(self, request, pk):
#         """Increases the views count for the schools and returns the data"""
#         school = get_object_or_404(School, pk=pk)
#         school.views = school.views + 1
#         school.save(update_fields="views")
#         return Response({"views": school.views}, status=status.HTTP_200_OK)


# school_views_view = SchoolViewsAPIView.as_view()


# class BookmarkCountAPIView(APIView):
#     def bookmark_count(self, request, pk):
#         school = get_object_or_404(School, pk=pk)
#         bookmark_count = school.bookmarks.count()
#         return Response({"Bookmark count": bookmark_count})


# bookmark_count = BookmarkCountAPIView.as_view()


# class EngagementMetricsAPIView(APIView):
#     def engagement_metrics(self, request, pk):
#         school = get_object_or_404(School, pk=pk)
#         reviews = school.reviews.all()
#         average_rating = reviews.aggregate(Avg("rating")["rating_avg"] or 0)
#         total_reviews = reviews.count()

#         return Response(
#             {"average_rating": average_rating}, {"total_reviews": total_reviews}
#         )


# engagement_metrics = EngagementMetricsAPIView.as_view()


# class RecentReviewsAPIView(APIView):
#     def recent_reviews(self, request, pk):
#         school = get_object_or_404(School, pk=pk)
#         recent_reviews = school.reviews.order_by("created_at")[:5]
#         serializer = ReviewSerializer(recent_reviews, many=True)

#         return Response(serializer.data)


# recent_reviews = RecentReviewsAPIView.as_view()
