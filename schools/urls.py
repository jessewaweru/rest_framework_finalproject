from django.urls import path, include
from . import views
from .views import SchoolBaseAnalyticsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    r"schools/baseanalytics",
    SchoolBaseAnalyticsViewSet,
    basename="school-base-analytics",
)

urlpatterns = [
    path("", views.school_list_create_view, name="school_list_create"),
    path("<int:pk>/update/", views.school_update_view, name="school_update"),
    path("<int:pk>/delete/", views.school_destroy_view, name="school_delete"),
    path("<int:pk>/", views.school_detail_view, name="school_detail"),
    path("<int:pk>/", views.bookmark_view, name="bookmark_view"),
    path("profile/", views.school_profile, name="school-profile"),
    path("analytics/", views.school_analytics, name="school-analytics"),
    path("", include(router.urls)),
    # path("<int:pk>/", views.school_views_view, name="school_views"),
    # path("<int:pk>/", views.bookmark_count, name="bookmark_count"),
    # path("<int:pk>/", views.engagement_metrics, name="engagement_metrics"),
    # path("<int:pk>/", views.recent_reviews, name="recent_reviews"),
]
