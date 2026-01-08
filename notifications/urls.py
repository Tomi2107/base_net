# notifications/urls.py
from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("go/<int:pk>/", views.go_notification, name="go"),
]
