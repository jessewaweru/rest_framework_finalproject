from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserViewset
from . import views

router = DefaultRouter()
router.register(r"users", UserViewset, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    # path("/api/v1/user/<int:id>/", views.get_user_by_id, name="get_user_by_id"),
    # path("api/v1/user/<int:id>/", views.get_user_by_id, name="get_user_by_id"),
    path("users/", include("users.urls")),
    path("schools/", include("schools.urls")),
    # path("v1/users/get/", get_user_by_id, name="get_user_by_id"),
]
