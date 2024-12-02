from rest_framework import generics
from schools.models import School
from schools.serializers import SchoolSerializer
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Bookmark, School
from django.contrib.auth import get_user_model
from django.db.models import Avg
from users.serializers import ReviewSerializer
from .serializers import (
    SchoolProfileSerializer,
    SchoolAnalyticsSerializer,
    SchoolCompareSerializer,
    SchoolBaseAnalyticsSerializer,
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from api.permissions import IsStaffOrAccOwner
from rest_framework.parsers import MultiPartParser
from io import StringIO
from django.db import transaction
from users.models import History
from django.utils import timezone
import pandas as pd

User = get_user_model()

logger = logging.getLogger(__name__)


class SchoolViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a specific school by its ID.

    list:
    Return a list of all schools.

    create:
    Create a new school profile.

    update:
    Update an existing school profile.

    delete:
    Delete a school profile.

    """

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsStaffOrAccOwner]
    lookup_field = "pk"
    parser_classes = [MultiPartParser]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(
                f"School created successfully: {response.data.get('name', 'unknown')},"
                f"created by user:{request.user.username}"
            )
            return response
        except ValidationError as e:
            logger.error(f"Validation error during school creation: {e.detail}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error occurred in school creation: {e}")
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    #  Tied to creating History for the current user
    def retrieve(self, request, *args, **kwargs):
        school = self.get_object()
        if request.user.is_authenticated:
            History.objects.create(
                user=request.user, school=school, viewed_at=timezone.now()
            )
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        school = self.get_object()
        school.delete()
        logger.info(f"School deleted successfully: {school.name}")
        return Response(
            {"message": "School successfully deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

    def parse_file(file):
        """
        Parse an uploaded file (CSV or Excel) into a list of dictionaries.
        """
        try:
            file_extension = file.name.split(".")[-1].lower()
            if file_extension == "csv":
                df = pd.read_csv(
                    StringIO(file.read().decode("utf-8-sig", errors="ignore"))
                )
            elif file_extension in ["xls", "xlsx"]:
                df = pd.read_excel(file)
            else:
                raise ValidationError(
                    "Unsupported file format.Kindly upload a CSV or Excel file"
                )
            logger.info(f"File parsed successfully:{file.name}")
            return df.to_dict(orient="records")
        except Exception as e:
            raise ValidationError(f"error reading the file:{e}")

    def upload_performance(self, request, pk=None):
        """
        Handle file upload, validate it, and parse CSV for school performance.
        """
        school = self.get_object()
        file = request.FILES.get("performance_data")  # Retrieve the uploaded file
        if not file:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_peformance_file(file)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        try:
            parsed_data = self.parse_file(file)
        except ValidationError as e:
            return Response(
                {"error": f"Failed to parse file:{str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            with transaction.atomic():
                school.performance_file = file
                school.performance_data = parsed_data
                school.save()
                return Response(
                    {
                        "message": "Performance data has been uploaded successfully",
                        "data": parsed_data,
                    },
                    status=status.HTTP_200_OK,
                )
        except Exception as e:
            return Response(
                {"error:Failed to save performance data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_school:
            return SchoolProfileSerializer
        return SchoolSerializer


""" Views handling the analytics dashboard for the school profile through the school model """


# SchoolProfileView displays the profile of a single school linked to the currently authenticated user
class SchoolProfileView(APIView):

    def get(self, request):
        school = get_object_or_404(School, user=request.user)
        serializer = SchoolProfileSerializer(school)
        return Response(serializer.data)


school_profile = SchoolProfileView.as_view()


class SchoolAnalyticsView(APIView):

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
        serializer = SchoolBaseAnalyticsSerializer(school)
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
This is the API handling the redeirection to school profile accounts 
that are tied to their users who created them. Associated function in class User
 i.e. get_school_profile.

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
