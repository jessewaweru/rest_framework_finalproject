from django.contrib import admin
from django.urls import path, include

# from django.conf.urls.static import static
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# from config.views import index


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     # path("", index),
#     path("api/", include("api.urls")),
#     path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
# ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # API root URLs
    # path(
    #     "api/schools/", include("schools.urls", namespace="schools")
    # ),  # Add schools URLs
    # path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
