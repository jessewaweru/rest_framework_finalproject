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
            raise PermissionError("School users cannot access a user profile.")
        return user


user_profile_update = UserProfileRetriveUpdateView.as_view

# User-Specific Recommendations:
# @action(detail=False, methods=['get'])
# def recommended_schools(self, request):
#     user = request.user
#     # Assuming a recommendation logic exists
#     queryset = School.objects.filter(location=user.preferred_location)
#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)


# Recently Visited Schools:
# @action(detail=False, methods=['get'])
# def recently_viewed(self, request):
#     user = request.user
#     queryset = user.recent_views.order_by('-viewed_at')[:10]
#     serializer = SchoolSerializer(queryset, many=True)
#     return Response(serializer.data)


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


review_create_view = ReviewCreateAPIView.as_view()
