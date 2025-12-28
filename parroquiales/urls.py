from django.urls import path
from .views import (
    ParroquialesListView,
    ParroquialPostCreateView
)

app_name = "parroquiales"

urlpatterns = [
    path("", ParroquialesListView.as_view(), name="list"),
    path("crear/", ParroquialPostCreateView.as_view(), name="create"),
]
