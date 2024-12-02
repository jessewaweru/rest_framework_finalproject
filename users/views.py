from rest_framework import generics
from users.models import Review
from users.serializers import ReviewSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from schools.models import School
from schools.serializers import SchoolSerializer
from django.db.models import Avg
from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework.views import APIView
from schools.models import Bookmark
from django.core.exceptions import PermissionDenied
from .models import Review
from .serializers import ReviewSerializer
from .serializers import HistorySerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from .models import History, User, OTP
from rest_framework import status
from .utils import send_otp_email


class UserInteractionsViewset(viewsets.ViewSet):
    @action(detail=False, methods=["get"])
    def top_rated(self, request):
        queryset = School.objects.annotate(avg_rating=Avg("reviews__rating")).order_by(
            ("-avg_rating")
        )[:10]
        serializer = SchoolSerializer(queryset, many=True)
        return Response(serializer.data)


class UserProfileRetriveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        if user.is_school:
            raise PermissionDenied("School users cannot access a user profile.")
        return user


user_profile_update = UserProfileRetriveUpdateView.as_view


class UserDashboardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            # "number_of_bookmarked_schools": self.get_bookmarked_schools_count(user),
            "top_rated_schools": self.get_top_rated_schools(),
            "recently_reviewed_schools": self.get_recently_reviewed_schools(user),
            "activity_feed": self.get_activity_feed(user),
            "average_rating_of_bookmarked_schools": self.get_average_rating_of_bookmarked_schools(
                user
            ),
            "personalized_recommendations": self.get_personalized_recommendations(user),
            # "engagement_insights": self.get_engagement_insights(user),
        }
        return Response(data)

    def get_bookmarked_schools_count(self, user):
        return Bookmark.objects.filter(user=user).count()

    def get_top_rated_schools(self):
        top_schools = School.objects.annotate(
            avg_rating=Avg("reviews__rating")
        ).order_by("-avg_rating")[:5]
        return SchoolSerializer(top_schools, many=True).data

    def get_recently_reviewed_schools(self, user):
        recent_reviews = Review.objects.filter(school__bookmark__user=user).order_by(
            "-created_at"
        )[:5]
        return ReviewSerializer(recent_reviews, many=True).data

    def get_activity_feed(self, user):
        bookmarks = Bookmark.objects.filter(user=user).order_by("-created_by")[:5]
        reviews = Review.objects.filter(user=user).order_by("-created_by")[:5]
        return {
            "recent_bookmarks": [
                {"school": bookmark.school.name, "date": bookmark.created_at}
                for bookmark in bookmarks
            ],
            "recent_reviews": [
                {
                    "school": review.school.name,
                    "rating": review.rating,
                    "date": review.created_at,
                }
                for review in reviews
            ],
        }

    def get_average_rating_of_bookmarked_schools(self, user):
        bookmarked_schools_ids = Bookmark.objects.filter(user=user).values_list(
            "school_id", flat=True
        )
        avg_rating = Review.objects.filter(
            school_id__in=bookmarked_schools_ids
        ).aggregate(Avg("rating"))
        return avg_rating["rating__avg"]

    def get_personalized_recommendations(self, user):
        bookmarked_schools_ids = Bookmark.objects.filter(user=user).values_list(
            "school_id", flat=True
        )
        recommended_schools = (
            School.objects.exclude(pk__in=bookmarked_schools_ids)
            .annotate(avg_rating=Avg("reviews__rating"))
            .order_by("-avg_rating")[:5]
        )
        return SchoolSerializer(recommended_schools, many=True).data


user_dashboard = UserDashboardAPIView.as_view()


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


review_create_view = ReviewCreateAPIView.as_view()


# filter user history based on a specified period- retrive function in SchoolViewSet
class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        days = self.request.query_params.get("days", 1)
        try:
            days = int(days)
        except ValueError:
            days = 1

        time_threshold = timezone.now() - timedelta(days=days)
        return History.objects.filter(user=user, viewed_at__gte=time_threshold)


""" Views for handling OTP for user loging and resetting of passwords """


class Verify_EmailView(APIView):
    def post(self, request):
        user = request.user
        otp = request.data.get("otp")

        if not user.otp.is_valid():
            return Response(
                {"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        if user.otp.code == otp:
            user.email_verified = True
            user.save()
            return Response(
                {"message": "Email verified successfully"}, status=status.HTTP_200_OK
            )
        return Response({"error": "Invalid code"}, status=status.HTTP_200_OK)


class RequestResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            send_otp_email(user)
            return Response(
                {"message": "OTP sent to your email"}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        try:
            user = User.objects.get(email=email)
            if user.otp.is_valid() and user.otp.code == otp:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"message": "Password has been reset successfully"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email doesn't exisit"},
                status=status.HTTP_400_BAD_REQUEST,
            )
