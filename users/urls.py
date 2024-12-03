from django.urls import path, include
from . import views
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
    path("add-review/", views.review_create_view, name="add-review"),
    path("profile/", views.user_profile_update, name="user-profile"),
    path("dashboard/", views.user_dashboard, name="user-dashboard"),
    path("", include(router.urls)),
]
