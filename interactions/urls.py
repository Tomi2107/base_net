from django.urls import path
from . import views

app_name = "interactions"

urlpatterns = [
    path(
        "save/<str:model_name>/<int:item_id>/",
        views.save_item,
        name="save"
    ),
    path(
        "unsave/<str:model_name>/<int:item_id>/",
        views.unsave_item,
        name="unsave"
    ),
    path("saved/", views.saved_items_list, name="saved_items_list"),
    path("remove/<int:item_id>/", views.remove_store_item, name="remove"),

]