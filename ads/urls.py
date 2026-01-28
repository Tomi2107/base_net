from django.urls import path
from . import views

app_name = "ads"

urlpatterns = [
    path("click/<int:ad_id>/", views.ad_click, name="click"),
    path("my/", views.my_ads, name="my_ads"),
    path("create/", views.create_ad, name="create"),
    # path("<int:pk>/edit/", views.edit_ad, name="edit"),
    path("<int:pk>/activate/", views.activate_ad, name="activate"),
    path("admin/dashboard/", views.admin_ads_dashboard, name="admin_dashboard"),
    path("admin/<int:pk>/approve/", views.approve_ad, name="approve"),
    path("admin/<int:pk>/reject/", views.reject_ad, name="reject"),



]
