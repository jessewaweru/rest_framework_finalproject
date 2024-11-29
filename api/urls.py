from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewset
from schools.views import SchoolViewSet, SchoolBaseAnalyticsViewSet


router = DefaultRouter()
router.register(r"users", UserViewset, basename="user")
router.register(r"schools", SchoolViewSet, basename="school")
router.register(
    r"schools/baseanalytics",
    SchoolBaseAnalyticsViewSet,
    basename="school-base-analytics",
)

urlpatterns = [
    path("", include(router.urls)),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("schools/", include("schools.urls", namespace="schools_api")),
    path(
        "notifications/",
        include(("notifications.urls", "notifications"), namespace="notifications"),
    ),
    path("search/", include(("search.urls", "search"), namespace="search")),
]
