from django.urls import path, include
from . import views
from .views import verify_email, request_otp
from rest_framework.routers import DefaultRouter
from .views import UserInteractionsViewset, HistoryViewSet


router = DefaultRouter()

router.register(
    r"user-interactions",
    UserInteractionsViewset,
    basename="user-interactions",
)

router.register(
    r"history",
    HistoryViewSet,
    basename="history",
)

# Define the URL patterns
urlpatterns = [
    path("verify-email/", verify_email, name="verify-email"),
    path("request-otp/", request_otp, name="request_otp"),
    path("add-review/", views.review_create_view, name="add-review"),
    path("profile/", views.user_profile_update, name="user-profile"),
    path("dashboard/", views.user_dashboard, name="user-dashboard"),
    path("", include(router.urls)),
]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     verify_email,
#     UserInteractionsViewset,
#     HistoryViewSet,
# )
# from api.views import UserViewset
# from . import views


# router = DefaultRouter()

# router.register(
#     r"user-interactions",
#     UserInteractionsViewset,
#     basename="user-interactions",
# )

# router.register(
#     r"history",
#     HistoryViewSet,
#     basename="history",
# )

# # Define explicit URLs for UserViewset to avoid conflicts
# user_viewset_urls = [
#     path("<str:pk>/", UserViewset.as_view({"get": "retrieve"}), name="user-detail"),
#     path("", UserViewset.as_view({"get": "list", "post": "create"}), name="user-list"),
# ]

# # Define the URL patterns
# urlpatterns = [
#     path("verify-email/", verify_email, name="verify-email"),  # Explicit path
#     path("add-review/", views.review_create_view, name="add-review"),
#     path("profile/", views.user_profile_update, name="user-profile"),
#     path("dashboard/", views.user_dashboard, name="user-dashboard"),
#     path(
#         "request-reset-password/",
#         views.request_reset_password,
#         name="request-reset-password",
#     ),
#     path("reset-password/", views.reset_password, name="reset-password"),
#     path("users/", include(user_viewset_urls)),  # Explicit UserViewSet URLs
#     path("", include(router.urls)),  # Dynamic URLs come last
# ]
