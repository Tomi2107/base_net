from django.urls import path
from .views import StoreListView, create_item

app_name = "store"

urlpatterns = [
    path("", StoreListView.as_view(), name="list"),
    path("create/", create_item, name="create"),
]
