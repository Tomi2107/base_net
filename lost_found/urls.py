from django.urls import path
from . import views

app_name = "lost_found"

urlpatterns = [
    path("", views.feed, name="feed"),
]
