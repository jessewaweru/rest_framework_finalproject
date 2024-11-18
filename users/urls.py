from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserInteractionsViewset, HistoryViewSet

router = DefaultRouter()

router.register(
    r"user-Interactions",
    UserInteractionsViewset,
    basename="userinteractionsviewset",
)
router2 = DefaultRouter()
router2.register(r"history", HistoryViewSet, basename="history")

urlpatterns = [
    path("add-review/", views.review_create_view, name="add-review"),
    path("", include(router.urls)),
    path("", include(router2.urls)),
    path("profile/", views.user_profile_update, name="user-profile"),
    path("dashboard/", views.user_dashboard, name="user-dashboard"),
]
