from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SchoolBaseAnalyticsViewSet,
    SchoolViewSet,
    bookmark_view,
    school_profile,
    school_analytics,
    school_comparison_view,
    complete_school_profile,
)

# router = DefaultRouter()
# router.register(
#     r"schools/baseanalytics",
#     SchoolBaseAnalyticsViewSet,
#     basename="school-base-analytics",
# )
# router.register(r"", SchoolViewSet, basename="school")

app_name = "schools"

urlpatterns = [
    path("<int:pk>/bookmark/", bookmark_view, name="bookmark_view"),
    path("profile/", school_profile, name="school-profile"),
    path("analytics/", school_analytics, name="school-analytics"),
    path("compare/", school_comparison_view, name="school-comparison"),
    path("complete-profile", complete_school_profile, name="complete-school-profile"),
    # path("", include(router.urls)),
]
