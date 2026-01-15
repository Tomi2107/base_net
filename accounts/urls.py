from django.urls import path

from .views import UserProfileView, EditProfile, AddFollower, RemoveFollower, ListFollowers, delete_opinion

from . import views  # <- importa todo desde views

app_name="accounts"

urlpatterns = [
    path('delete/', views.account_delete, name='account_delete'),
    
    path('profile/edit', EditProfile, name="edit-profile"),

    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
	path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),

    path('profile/<int:pk>/followers/',ListFollowers.as_view(), name='followers-list'),
    
    path('opinion/delete/<int:opinion_id>/', delete_opinion, name='delete-opinion'),
    path('<username>/', UserProfileView, name="profile"),

]
