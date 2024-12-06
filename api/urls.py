from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewset
from schools.views import SchoolViewSet, SchoolBaseAnalyticsViewSet
from users.views import (
    verify_email,
    request_otp,
    password_verify_otp,
    password_request_reset,
)


router = DefaultRouter()
router.register(r"users", UserViewset, basename="user")
router.register(r"schools", SchoolViewSet, basename="school")
router.register(
    r"schools/baseanalytics",
    SchoolBaseAnalyticsViewSet,
    basename="school-base-analytics",
)

urlpatterns = [
    path("users/verify-email/", verify_email, name="verify-email"),
    path("users/request-otp/", request_otp, name="request_otp"),
    path(
        "users/password-request-reset/",
        password_request_reset,
        name="password-request-reset",
    ),
    path("users/password-verify-otp/", password_verify_otp, name="password-verify-otp"),
    path("", include(router.urls)),
    path("users/", include(("users.urls", "users"), namespace="users")),
    path("schools/", include("schools.urls", namespace="schools_api")),
    path(
        "notifications/",
        include(("notifications.urls", "notifications"), namespace="notifications"),
    ),
    path("search/", include(("search.urls", "search"), namespace="search")),
]
