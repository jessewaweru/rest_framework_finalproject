# from django.urls import path, include
# from . import views
# from .views import SchoolBaseAnalyticsViewSet, SchoolViewSet
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()

# router.register(
#     r"schools/baseanalytics",
#     SchoolBaseAnalyticsViewSet,
#     basename="school-base-analytics",
# )

# router2 = DefaultRouter()
# router2.register(r"schools", SchoolViewSet, basename="school")

# app_name = "schools"

# urlpatterns = [
#     # path(
#     #     "schools/list-create/", views.school_list_create_view, name="school_list_create"
#     # ),
#     # path("<int:pk>/update/", views.school_update_view, name="school_update"),
#     # path("<int:pk>/delete/", views.school_destroy_view, name="school_delete"),
#     # path("<int:pk>/detail/", views.school_detail_view, name="school_detail"),
#     path("<int:pk>/bookmark/", views.bookmark_view, name="bookmark_view"),
#     path("profile/", views.school_profile, name="school-profile"),
#     path("analytics/", views.school_analytics, name="school-analytics"),
#     path("schools/compare/", views.school_comparison_view, name="school-comparison"),
#     path(
#         "complete-profile",
#         views.complete_school_profile,
#         name="complete-school-profile",
#     ),
#     path("", include(router.urls)),
#     path("api/", include(router2.urls)),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # SchoolBaseAnalyticsViewSet,
    SchoolViewSet,
    # bookmark_view,
    # school_profile,
    # school_analytics,
    # school_comparison_view,
    # complete_school_profile,
)


router = DefaultRouter()
# router.register(
# r"schools/baseanalytics",
# SchoolBaseAnalyticsViewSet,
# basename="school-base-analytics",
# )
router.register(r"schools", SchoolViewSet, basename="school")

app_name = "schools"

urlpatterns = [
    # path("<int:pk>/bookmark/", bookmark_view, name="bookmark_view"),
    # path("profile/", school_profile, name="school-profile"),
    # path("analytics/", school_analytics, name="school-analytics"),
    # path("schools/compare/", school_comparison_view, name="school-comparison"),
    # path("complete-profile", complete_school_profile, name="complete-school-profile"),
    path("", include(router.urls)),
]

# # Add the router's URLs
# urlpatterns += router.urls
