from django.urls import path
from .views import school_search_view

urlpatterns = [path("schools/", school_search_view, name="school_search")]
