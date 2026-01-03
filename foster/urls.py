from django.urls import path
from .views import FosterListView

app_name = "foster"

urlpatterns = [
    path("", FosterListView.as_view(), name="list"),
]
