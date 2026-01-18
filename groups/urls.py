from django.urls import path
from .views import GroupListView, create_group, group_profile, join_group, group_requests, approve_request, reject_request, create_group_post, leave_group, follow_group, unfollow_group

app_name = "groups"

urlpatterns = [
    path("", GroupListView.as_view(), name="list"),
    path("create/", create_group, name="create"),
    path("<int:pk>/", group_profile, name="profile"),  # 👈 NUEVO
    path("<int:group_id>/join/", join_group, name="join"),
    path("<int:group_id>/requests/", group_requests, name="requests"),
    path("requests/<int:membership_id>/approve/", approve_request, name="approve"),
    path("requests/<int:membership_id>/reject/", reject_request, name="reject"),
    path("<int:pk>/leave/", leave_group, name="leave"),

    path("groups/<int:group_id>/post/", create_group_post, name="create_group_post"),
    
    # FOLLOW / UNFOLLOW 👇
    path("<int:pk>/follow/", follow_group, name="follow"),
    path("<int:pk>/unfollow/", unfollow_group, name="unfollow"),



]
