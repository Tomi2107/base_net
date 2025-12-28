from django.urls import path
from .views import GroupListView, create_group

app_name = "groups"

urlpatterns = [
    path("", GroupListView.as_view(), name="list"),
    path("create/", create_group, name="create"),
]
