from django.urls import path
from .views import ReelListView, create_reel

app_name = "reels"

urlpatterns = [
    path("", ReelListView.as_view(), name="list"),
    path("create/", create_reel, name="create"),  # 👈 ESTA FALTABA
]
