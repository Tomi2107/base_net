from django.urls import path
from .views import LostFoundFeedView

app_name = "lost_found"

urlpatterns = [
    path("", LostFoundFeedView.as_view(), name="feed"),
]
