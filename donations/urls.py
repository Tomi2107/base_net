from django.urls import path
from .views import donate_view

app_name = "donations"

urlpatterns = [
    path("dona/", donate_view, name="donate"),
]
