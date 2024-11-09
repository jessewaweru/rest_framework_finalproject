from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserInteractionsViewset

router = DefaultRouter()

router.register(
    r"User-Interactions-Viewset",
    UserInteractionsViewset,
    basename="userinteractionsviewset",
)

urlpatterns = [
    path("", views.review_create_view, name="add-review"),
    path("", include(router.urls)),
    path("profile/", views.user_profile_update, name="user-profile"),
]
