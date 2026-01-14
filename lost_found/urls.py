from django.urls import path
from . import views

app_name = "lost_found"

urlpatterns = [
    path("", views.lost_found_feed, name="feed"),
    path('remove/<int:pet_id>/', views.remove_lost_post, name='remove_lost'),

]
